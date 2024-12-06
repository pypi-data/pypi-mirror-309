import json
import logging
import os
import time
from dataclasses import asdict, dataclass
from importlib.metadata import version
from typing import IO, Any, Literal, TypedDict
from uuid import UUID

import msgpack
import orjson
import requests
import torch
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from orca_common import (
    EXACT_MATCH_THRESHOLD,
    CatchupStatus,
    ColumnName,
    EmbeddingModel,
    Order,
    OrderByColumns,
    RowDict,
    TableCreateMode,
)
from orcalib.client_data_model import (
    ApiFilter,
    SimpleTableQueryRequest,
    TableSelectResponse,
    decode_ndarray,
)
from orcalib.exceptions import (
    OrcaBadRequestException,
    OrcaException,
    OrcaNotFoundException,
    OrcaUnauthenticatedException,
    OrcaUnauthorizedException,
)
from orcalib.index_handle import IndexHandle
from orcalib.orca_types import CustomSerializable, OrcaTypeHandle

OrcaMetadataDict = dict[str, str | int | float | bool | list[str] | list[int] | list[float] | list[bool] | None]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PagedResponse(TypedDict):
    """
    The response from a paged query

    Attributes:
        page_index: The index of the current page
        page_size: The size of the current page
        total_size: The total number of items
        num_pages: The total number of pages
        has_next: If there is a next page
        items: The items on the current page
    """

    page_index: int
    page_size: int
    total_size: int
    num_pages: int
    has_next: bool
    items: list[Any]


@dataclass
class ColumnSpec:
    """
    Schema of a column in a table

    Attributes:
        name: The name of the column
        notnull: If the column is allowed to contain null values
        unique: If each value in the column must be unique
        dtype: The data type of the column
    """

    name: str
    notnull: bool
    unique: bool
    dtype: str


def _prepare_file_list(files: list[tuple[str, IO[bytes]]]) -> list[tuple[str, tuple[str, IO[bytes]]]]:
    """Prepare the file list for a multipart request

    Args:
        files: The list of files to prepare

    Returns:
        The prepared file list

    NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
    """
    return [("files", (file_name, file_bytes)) for file_name, file_bytes in files]


class OrcaClient:
    """The OrcaClient class is used to make requests to the Orca web service"""

    # The api key to use for the session locally (should not store in code, use environment variables or similar instead)
    API_KEY = "my_api_key"
    # The secret key to use for the session locally (should not store in code, use environment variables or similar instead)
    SECRET_KEY = "my_secret_key"
    # The base url for the local web service
    BASE_URL = "http://localhost:1583/"
    # The default server version indicating unreleased
    SERVER_VERSION: str = "0.0.0"
    # The version of the client
    CLIENT_VERSION: str = version("orcalib")
    # Class variable for tracking if the version check warning has been logged
    _skipping_version_check_warning_logged = False

    @staticmethod
    def set_credentials(*, api_key: str, secret_key: str, base_url: str | None = None) -> None:
        """
        Set the api and secret key for the session

        Args:
            api_key: The api key for the OrcaDB instance
            secret_key: The secret key for the OrcaDB instance
            base_url: The base url of the OrcaDB instance
        """
        OrcaClient.API_KEY = api_key
        OrcaClient.SECRET_KEY = secret_key
        if base_url:
            OrcaClient.BASE_URL = base_url
        OrcaClient.SERVER_VERSION = OrcaClient.get_server_version() or "0.0.0"
        OrcaClient.check_version_compatibility()

    @classmethod
    def check_version_compatibility(cls) -> bool | None:
        """
        Check if the OrcaLib version is compatible with the OrcaDB instance version and log a warning if not.

        Returns:
            True if the versions match, False if they do not, None if the version check is skipped
        """
        if cls.SERVER_VERSION == "0.0.0":
            if not cls._skipping_version_check_warning_logged:
                logger.info(f"OrcaDB Instance version is '{cls.SERVER_VERSION}'. Skipping version check.")
                cls._skipping_version_check_warning_logged = True
        elif cls.CLIENT_VERSION == "0.0.0":
            if not cls._skipping_version_check_warning_logged:
                logger.info(f"OrcaLib version is '{cls.CLIENT_VERSION}'. Skipping version check.")
                cls._skipping_version_check_warning_logged = True
        elif cls.SERVER_VERSION != cls.CLIENT_VERSION:
            logger.warning(
                f"OrcaLib version {cls.CLIENT_VERSION} does not match OrcaDB instance version {cls.SERVER_VERSION}. Please ensure you use version {cls.SERVER_VERSION} of OrcaLib."
            )
            return False
        else:
            return True

    @staticmethod
    def _format_num_bytes(num: int, suffix: str = "B") -> str:
        """Format a number of bytes into a human readable string"""
        for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    @staticmethod
    def get_server_version() -> str | None:
        """
        Get the version of the OrcaDB server.

        Returns:
            the version string
        """
        try:
            healthcheck_data = OrcaClient.healthcheck()
            result = healthcheck_data.get("git_tag", "")
            return result[1:] if result.startswith("v") else result
        except Exception as e:
            logger.warning(f"Failed to get server version: {e}")

    @staticmethod
    def _server_version_gte(version_to_check: str) -> bool:
        OrcaClient.SERVER_VERSION
        # Check if the required version is less than the current server version
        if OrcaClient.SERVER_VERSION == "0.0.0":
            logger.warning(f"Server version is '{OrcaClient.SERVER_VERSION}'. Skipping version check.")
            return True

        # This will split both the versions by '.'
        version_to_check_arr = version_to_check.split(".")
        server_version_arr = OrcaClient.SERVER_VERSION.split(".")
        n = len(version_to_check_arr)
        m = len(server_version_arr)

        # converts to integer from string
        version_to_check_arr = [int(i) for i in version_to_check_arr]
        server_version_arr = [int(i) for i in server_version_arr]

        # compares which list is bigger and fills
        # smaller list with zero (for unequal delimiters)
        if n > m:
            for i in range(m, n):
                server_version_arr.append(0)
        elif m > n:
            for i in range(n, m):
                version_to_check_arr.append(0)

        # True if the server version is greater than or equal to the version to check
        # False is the server version is less than the version to check
        for i in range(len(version_to_check_arr)):
            if server_version_arr[i] > version_to_check_arr[i]:
                return True
            elif server_version_arr[i] < version_to_check_arr[i]:
                return False
        return True

    @staticmethod
    def _orca_request(
        method: str,
        url: str,
        request_params: dict[str, Any] | None = None,
        retries: int = 3,
        verbose: bool = False,
        file_path: str | None = None,
    ) -> requests.Response:
        """
        Perform the HTTP request to the web service with auth details

        Args:
            method: The http method to use
            url: The url to request
            request_params: The parameters to send with the request
            retries: The number of times to retry the request if it fails
            verbose: If True, print verbose output about the request
            file_path: The path to a file to upload

        Returns:
            The response from the web service

        Raises:
            OrcaNotFoundException: If the resource was not found
            OrcaUnauthenticatedException: If the request was not authenticated
            OrcaUnauthorizedException: If the request was not authorized
            OrcaBadRequestException: If the request was bad
            OrcaException: If the request failed for another reason
        """

        if request_params is None:
            request_params = {}

        if method == "GET":
            assert "json" not in request_params, "GET requests cannot have a body"

        if verbose:
            print(f"Orca request start: {method} {url}")

        start_time = time.time()

        request_params["headers"] = {
            **{
                "api-key": OrcaClient.API_KEY,
                "secret-key": OrcaClient.SECRET_KEY,
            },
            **request_params.get("headers", {}),
        }

        status_force_retry = [500, 502, 504]

        retry_config = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=0.3,
            status_forcelist=status_force_retry,
        )

        adapter = HTTPAdapter(max_retries=retry_config)
        with requests.Session() as session:
            session.mount(url, adapter)
            if verbose:
                print(f"Orca request params: {request_params}")
            # Needed because requests.request has issues with large file upload: ChunkedEncodingError
            if file_path:
                file = {"file": open(file_path, "rb")}
                resp = requests.post(url=url, files=file, **request_params)
            else:
                resp = requests.request(method=method, url=url, **request_params)

        end_time = time.time()

        elapsed_time_ms = int((end_time - start_time) * 1000)

        if verbose:
            content_length = OrcaClient._format_num_bytes(len(resp.content))
            print(f"Orca request end: {method} {url} {resp.status_code} {content_length} {elapsed_time_ms}ms")

        if not resp.ok:
            if resp.status_code == 404:
                raise OrcaNotFoundException(resp.content)
            elif resp.status_code == 401:
                raise OrcaUnauthenticatedException(resp.content)
            elif resp.status_code == 403:
                raise OrcaUnauthorizedException(resp.content)
            elif resp.status_code == 400:
                raise OrcaBadRequestException(resp.content)
            raise OrcaException(resp.content)

        return resp

    @staticmethod
    def create_database(db_name: str) -> None:
        """
        Create a new database on the instance

        Args:
            db_name: The name of the database
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/create_database")
        request_params = {"params": {"db_name": db_name}}
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def drop_database(db_name: str, ignore_db_not_found: bool = False) -> bool:
        """
        Drop a database from the instance

        Args:
            db_name: The name of the database
            ignore_db_not_found: If `True`, ignore the error if the database is not found

        Returns:
            `True` if the database was dropped, `False` if it was not found
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v1/drop/db/{db_name}")
        request_params = {"params": {"ignore_db_not_found": ignore_db_not_found}}
        res = OrcaClient._orca_request("DELETE", url, request_params)
        return res.json()["value"]

    @staticmethod
    def database_exists(db_name: str) -> bool:
        """
        Check if the database exists

        Args:
            db_name: The name of the database

        Returns:
            `True` if the database exists, `False` if it does not
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v1/exists/db/{db_name}")
        request_params = {"params": {}}
        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()["value"]

    @staticmethod
    def restore_backup(target_db_name: str, backup_name: str, checksum: str | None = None) -> None:
        """
        Restore a database from a backup

        Args:
            target_db_name: The name of the target database
            backup_name: The name of the backup
            checksum: The checksum of the backup file (optional)

        Returns:
            Restore database response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/restore_database")
        request_params = {
            "params": {
                "target_db_name": target_db_name,
                "backup_name": backup_name,
                "checksum": checksum,
            }
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def create_backup(db_name: str) -> requests.Response:
        """Create a backup of the database

        Args:
            db_name: The name of the database

        Returns:
            Create backup response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/backup_database")
        request_params = {"params": {"db_name": db_name}}
        res = OrcaClient._orca_request("POST", url, request_params)
        return res.json()

    @staticmethod
    def download_backup(backup_file: str, download_path: str = "./data", overwrite: bool = False) -> None:
        """
        Download a backup from the server and save it to a file

        Args:
            backup_file: The name of the backup file
            download_path: The path of the folder to save the backup file
            overwrite: If `True`, overwrite the file if it already exists
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/download_backup")
        request_params = {"params": {"backup_file": backup_file}}
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        download_file_location = f"{download_path}/{backup_file}"
        if not overwrite and os.path.exists(download_file_location):
            raise ValueError(f"{download_file_location} already exists")
        res = OrcaClient._orca_request("GET", url, request_params)
        with open(download_file_location, "wb") as f:
            f.write(res.content)

    @staticmethod
    def upload_backup(file_path: str) -> None:
        """
        Upload a backup to the server

        Args:
            file_path: The path to the backup file
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/upload_backup")
        OrcaClient._orca_request("POST", url, file_path=file_path)

    @staticmethod
    def delete_backup(backup_file_name: str) -> None:
        """
        Delete a backup from the server

        Args:
            backup_file_name: The name of the backup file
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/delete_backup")
        request_params = {"params": {"backup_file_name": backup_file_name}}
        OrcaClient._orca_request("DELETE", url, request_params)

    @staticmethod
    def list_databases() -> list[str]:
        """
        List all the databases on the server

        Returns:
            List of database names
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/list_databases")
        res = OrcaClient._orca_request("GET", url)
        return res.json()["databases"]

    @staticmethod
    def list_tables(db_name: str) -> list[str]:
        """
        List all the tables in the database

        Args:
            db_name: The name of the database

        Returns:
            List of table names
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/get_tables")
        request_params = {"params": {"db_name": db_name}}
        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()["tables"]

    @staticmethod
    def table_info(db_name: str, table_name: str) -> list[ColumnSpec]:
        """
        Get the information about a table

        Args:
            db_name: The name of the database
            table_name: The name of the table

        Returns:
            List with schema information for each column in the table
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/table_info")
        request_params = {"params": {"db_name": db_name, "table_name": table_name}}
        res = OrcaClient._orca_request("GET", url, request_params)
        return [ColumnSpec(**col) for col in res.json()]

    @staticmethod
    def healthcheck() -> dict[str, Any]:
        """Perform a healthcheck on the server

        Returns:
            Dictionary with healthcheck information
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/healthcheck")
        res = OrcaClient._orca_request("GET", url)
        return res.json()

    @staticmethod
    def create_table(
        db_name: str,
        table_name: str,
        table_schema: list[ColumnSpec],
        if_table_exists: TableCreateMode = TableCreateMode.ERROR_IF_TABLE_EXISTS,
    ) -> None:
        """Create a new table in the database

        Args:
            db_name: The name of the database
            table_name: The name of the table
            table_schema: The schema of the table
            if_table_exists: What to do if the table already exists
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/create_table")
        request_params = {
            "params": {
                "db_name": db_name,
                "table_name": table_name,
                "if_table_exists": if_table_exists,
            },
            "json": [asdict(col) for col in table_schema],
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def insert(
        db_name: str,
        table_name: str,
        rows: list[RowDict],
        files: list[tuple[str, IO[bytes]]],
    ) -> None:
        """
        Insert rows into the table

        Args:
            db_name: The name of the database
            table_name: The name of the table
            rows: The rows to insert
            files: The files to upload
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v2/db/insert/{db_name}/{table_name}")
        request_params = {
            "data": {"data": json.dumps({"rows": rows})},
            "files": _prepare_file_list(files),
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def update(
        db_name: str,
        table_name: str,
        row: RowDict,
        filter: Any,
        files: list[tuple[str, IO[bytes]]],
    ) -> None:
        """
        Update a row in the table

        Args:
            db_name: The name of the database
            table_name: The name of the table
            row: The row to update
            filter: The filter to apply
            files: The files to upload

        Returns:
            Update response
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v2/db/update/{db_name}/{table_name}")
        request_params = {
            "data": {"data": json.dumps({"row": row, "filter": filter})},
            "files": _prepare_file_list(files),
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def upsert(
        db_name: str,
        table_name: str,
        rows: list[RowDict],
        key_columns: list[str],
        files: list[tuple[str, IO[bytes]]],
    ) -> None:
        """
        Upsert rows into the table

        Args:
            db_name: The name of the database
            table_name: The name of the table
            rows: The rows to upsert
            key_columns: The key columns to use for the upsert
            files: The files to upload
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v2/db/upsert/{db_name}/{table_name}")
        request_params = {
            "data": {"data": json.dumps({"rows": rows, "key_columns": key_columns})},
            "files": _prepare_file_list(files),
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def delete(db_name: str, table_name: str, filter: Any) -> None:
        """
        Delete rows from the table

        Args:
            db_name: The name of the database
            table_name: The name of the table
            filter: The filter to apply
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/delete")
        request_params = {
            "params": {"db_name": db_name, "table_name": table_name},
            "json": filter,
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def count(db_name: str, table_name: str) -> int:
        """
        Count the number of rows in a table

        Args:
            db_name: The name of the database
            table_name: The name of the table

        Returns:
            The number of rows in the table
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v1/count/db/{db_name}/{table_name}")
        res = OrcaClient._orca_request("GET", url)
        return res.json()["row_count"]

    @staticmethod
    def add_column(
        db_name: str,
        table_name: str,
        new_col: list[str],
        dtype: list[str],
        notnull: list[bool],
        unique: list[bool],
    ) -> None:
        """
        Add a new column to the table

        Args:
            db_name: The name of the database
            table_name: The name of the table
            new_col: The name of the new column
            dtype: The data type of the new column
            notnull: If the new column is not null
            unique: If the new column is unique
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/add_column")
        request_params = {
            "params": {"db_name": db_name, "table_name": table_name},
            "json": {
                "new_col": new_col,
                "dtype": dtype,
                "notnull": notnull,
                "unique": unique,
            },
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def drop_column(
        db_name: str,
        table_name: str,
        col_names: list[str],
    ) -> None:
        """
        Drop a column from the table

        Args:
            db_name: The name of the database
            table_name: The name of the table
            col_names: The name of the column to drop
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/drop_column")
        request_params = {
            "params": {"db_name": db_name, "table_name": table_name},
            "json": col_names,
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def drop_table(db_name: str, table_name: str, error_if_not_exists: bool = True) -> None:
        """
        Drop a table from the database

        Args:
            db_name: The name of the database
            table_name: The name of the table
            error_if_not_exists: If True, raise an error if the table does not exist
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/drop_table")
        request_params = {
            "params": {
                "db_name": db_name,
                "table_name": table_name,
                "error_if_not_exists": error_if_not_exists,
            },
            "json": [],
        }
        OrcaClient._orca_request("DELETE", url, request_params)

    @staticmethod
    def drop_index(db_name: str, index_name: str) -> None:
        """
        Drop an index from the database

        Args:
            db_name: The name of the database
            index_name: The name of the index
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/drop_index")
        request_params = {
            "params": {"db_name": db_name, "index_name": index_name},
            "json": [],
        }
        OrcaClient._orca_request("DELETE", url, request_params)

    @staticmethod
    def select(
        table: "TableHandle",  # noqa: F821
        columns: list[ColumnName] | None = None,
        limit: int | None = None,
        filter: ApiFilter | None = None,
        order_by_columns: OrderByColumns | None = None,
        default_order: Order = Order.ASCENDING,
    ) -> TableSelectResponse:
        """
        Perform a select query on the table

        Args:
            table: The TableHandle for the table we're querying
            columns: The columns to select. If None, all columns are selected
            limit: The maximum number of rows to return
            filter: The filter to apply to the query
            order_by_columns: The columns to order by. If None, no order is applied.
            default_order: The default order to use if no order is specified. Defaults to ascending.

        Returns:
            The response from the select query
        """
        url = os.path.join(
            OrcaClient.BASE_URL,
            f"v2/select/db/{table.db_name}/{table.table_name}",
        )
        params = SimpleTableQueryRequest(
            columns=columns,
            limit=limit,
            filter=filter,
            order_by_columns=order_by_columns,
            default_order=default_order,
        )
        request = {
            "params": {},
            "json": params.dict(by_alias=True, exclude_unset=True),
        }

        response = OrcaClient._orca_request("POST", url, request)

        content = msgpack.unpackb(response.content, object_hook=decode_ndarray, raw=False)

        col_name_to_type = {
            col_name: OrcaTypeHandle.from_string(table.columns[col_name].dtype) for col_name in table.columns
        }

        for row in content["rows"]:
            OrcaClient._deserialize_column_value_dict(col_name_to_type, row["column_values"])

        return content

    @staticmethod
    def _deserialize_column_value(col_type: OrcaTypeHandle, value: Any) -> Any:
        """
        Deserialize a single column value using the column's data type

        Args:
            col_type: The column's data type
            value: The value to deserialize

        Returns:
            The deserialized value
        """
        if not isinstance(col_type, CustomSerializable) or value is None:
            return value
        assert isinstance(value, dict)
        return col_type.msgpack_deserialize(value)

    @staticmethod
    def _deserialize_column_value_dict(col_name_to_type: dict[ColumnName, OrcaTypeHandle], row_values: RowDict) -> None:
        """
        Deserialize a dictionary of column values using the given type dictionary

        Note:
            This updates the dictionary in place!!

        Args:
            col_name_to_type: A dictionary of column names to their data types
            row_values: The dictionary of column values to deserialize
        """
        for col_name, col_type in col_name_to_type.items():
            if col_name in row_values:
                row_values[col_name] = OrcaClient._deserialize_column_value(col_type, row_values[col_name])

    @staticmethod
    def _deserialize_column_value_list(ordered_type_list: list[OrcaTypeHandle], value_list: list[Any]) -> list[Any]:
        """
        Deserialize a list of column values using the given type list

        Args:
            ordered_type_list: A list of column data types
            value_list: The list of column values to deserialize

        Returns:
            The deserialized list of column values
        """
        assert len(ordered_type_list) == len(value_list)
        return [OrcaClient._deserialize_column_value(t, v) for t, v in zip(ordered_type_list, value_list)]

    @staticmethod
    def _create_index_v2(db_name: str, index_name: str, table_name: str, column: str, index_type: str) -> IndexHandle:
        url = os.path.join(OrcaClient.BASE_URL, "v2/create_index")
        request_params = {
            "params": {
                "index_type": index_type,
                "index_name": index_name,
                "db_name": db_name,
            },
            "json": [{"database": db_name, "table": table_name, "column": column}],
        }

        json = OrcaClient._orca_request("POST", url, request_params, verbose=False).json()
        json["column_type"] = OrcaTypeHandle.from_string(json["column_type"])
        embed_type = json.get("embedding_type", None)
        json["embedding_type"] = OrcaTypeHandle.from_string(embed_type) if embed_type else None
        return IndexHandle(**json)

    @staticmethod
    def _create_index_v3(
        db_name: str,
        index_name: str,
        table_name: str,
        column: str,
        index_type: str,
        ann_index_type: str,
        embedding_model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMER,
    ) -> IndexHandle:
        url = os.path.join(OrcaClient.BASE_URL, "v3/create_index")
        request_params = {
            "params": {
                "index_type": index_type,
                "index_name": index_name,
                "ann_index_type": ann_index_type,
                "db_name": db_name,
                "embedding_model": embedding_model.value,
            },
            "json": [{"database": db_name, "table": table_name, "column": column}],
        }

        json = OrcaClient._orca_request("POST", url, request_params, verbose=False).json()
        json["column_type"] = OrcaTypeHandle.from_string(json["column_type"])
        embed_type = json.get("embedding_type", None)
        json["embedding_type"] = OrcaTypeHandle.from_string(embed_type) if embed_type else None
        return IndexHandle(**json)

    @staticmethod
    def create_index(
        db_name: str,
        index_name: str,
        table_name: str,
        column: str,
        index_type: str,
        ann_index_type: str = "hnswlib",
        embedding_model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMER,
    ) -> IndexHandle:
        """
        Create a new index

        Args:
            db_name: The name of the database
            index_name: The name of the index
            table_name: The name of the table
            column: The name of the column to index
            index_type: The type of the index
            ann_index_type: The type of the approximate nearest neighbors index
            embedding_model: The name of the embedding model

        Returns:
            handle for the created index
        """
        if OrcaClient._server_version_gte("0.0.52"):
            return OrcaClient._create_index_v3(
                db_name, index_name, table_name, column, index_type, ann_index_type, embedding_model
            )
        else:
            return OrcaClient._create_index_v2(db_name, index_name, table_name, column, index_type)

    @staticmethod
    def get_index_status(db_name: str, index_name: str) -> CatchupStatus:
        """Get the status of an index

        Args:
            db_name: The name of the database
            index_name: The name of the index

        Returns:
            Get index status response
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v1/get_index_status/{db_name}/{index_name}")
        request_params = {"params": {}}
        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()

    @staticmethod
    def get_index(db_name: str, index_name: str) -> IndexHandle:
        """
        Get the details of an index

        Args:
            db_name: The name of the database
            index_name: The name of the index

        Returns:
            The index handle
        """
        api_version = "v3" if OrcaClient._server_version_gte("0.0.52") else "v2"
        url = os.path.join(OrcaClient.BASE_URL, f"{api_version}/db/index_info/{db_name}/{index_name}")
        json = OrcaClient._orca_request("GET", url, None, verbose=False).json()
        json["column_type"] = OrcaTypeHandle.from_string(json["column_type"])
        embed_type = json.get("embedding_type", None)
        json["embedding_type"] = OrcaTypeHandle.from_string(embed_type) if embed_type else None
        return IndexHandle(**json)

    @staticmethod
    def scan_index(
        db: "OrcaDatabase",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: list[str] | None = None,
        filter: str | None = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
    ) -> Any:
        """
        Scan an index

        Args:
            db: The OrcaDatabase object
            index_name: The name of the index
            query: The query to apply
            limit: The maximum number of rows to return
            columns: The columns to return (optional)
            filter: The filter to apply (optional)
            drop_exact_match: Drops the exact match from the results, if it's found
            exact_match_threshold: The minimum distance threshold for the exact match

        Returns:
            The response from the scan index query
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v2/db/scan_index/{db.name}/{index_name}")
        table = db._get_index_table(index_name)
        request_params = {
            "json": {
                "columns": columns,
                "filter": filter,
                "primary_table": table.table_name,
                "max_neighbor_count": limit,
                "index_query": query,
                "drop_exact_match": drop_exact_match,
                "exact_match_threshold": exact_match_threshold,
            },
        }
        response = OrcaClient._orca_request("POST", url, request_params)
        content = msgpack.unpackb(response.content, object_hook=decode_ndarray, raw=False)
        col_name_to_type = {
            col_name: OrcaTypeHandle.from_string(table.columns[col_name].dtype) for col_name in table.columns
        }
        for row_values in content:
            OrcaClient._deserialize_column_value_dict(col_name_to_type, row_values)

        return content

    @staticmethod
    def vector_scan_index(
        table: "TableHandle",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: list[str] | None = None,
        filter: str | None = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        curate_run_ids: list[int] | None = None,
        curate_layer_name: str | None = None,
    ) -> "BatchedScanResult":  # noqa: F821
        """
        Performs a vector scan index query

        Args:
            table: The TableHandle for the table we're querying
            index_name: The name of the index
            query: The query to apply
            limit: The maximum number of rows to return
            columns: The columns to return (optional)
            filter: The filter to apply (optional)
            drop_exact_match: The flag to drop exact matches
            exact_match_threshold: The threshold for exact matches
            curate_run_ids: The curate run ids to apply (optional)
            curate_layer_name: The curate layer name to apply (optional)

        Returns:
            The response from the scan index query
        """
        from orcalib.batched_scan_result import BatchedScanResult

        url = os.path.join(OrcaClient.BASE_URL, f"v3/db/vector_scan_index/{table.db_name}/{index_name}")
        request_params = {
            "json": {
                "columns": columns,
                "filter": filter,
                "primary_table": table.table_name,
                "max_neighbor_count": limit,
                "index_query": query,
                "curate_run_ids": curate_run_ids,
                "curate_layer_name": curate_layer_name,
                "drop_exact_match": drop_exact_match,
                "exact_match_threshold": exact_match_threshold,
            },
        }
        response = OrcaClient._orca_request("POST", url, request_params)
        content = msgpack.unpackb(response.content, object_hook=decode_ndarray, raw=False)
        column_dict = {
            col_name: OrcaTypeHandle.from_string(col_type) for col_name, col_type in content["columns"].items()
        }
        ordered_type_list = [col_type for col_type in column_dict.values()]
        data = content["data"]
        data = [
            [(*OrcaClient._deserialize_column_value_list(ordered_type_list, row),) for row in batch] for batch in data
        ]

        return BatchedScanResult(column_dict, data)

    @staticmethod
    def full_vector_memory_join(
        *,
        db_name: str,
        index_name: str,
        memory_index_name: str,
        num_memories: int,
        query_columns: list[str] | str,
        page_size: int = 100,
        page_index: int = 0,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        shuffle_memories: bool = False,
    ) -> PagedResponse:
        """
        Perform a full vector memory join

        Args:
            db_name: The name of the database
            index_name: The name of the index
            memory_index_name: The name of the memory index
            num_memories: The number of memory indexes
            query_columns: The columns to query (or a single column)
            page_size: The size of the page to return
            page_index: The index of the page to return

        Returns:
            The response from the full vector memory join query
        """
        if not isinstance(query_columns, list):
            query_columns = [query_columns]

        url = os.path.join(OrcaClient.BASE_URL, "v1/full_vector_memory_join")
        request_params = {
            "json": {
                "db_name": db_name,
                "index_name": index_name,
                "memory_index_name": memory_index_name,
                "num_memories": num_memories,
                "page_size": page_size,
                "page_index": page_index,
                "query_columns": query_columns,
                "drop_exact_match": drop_exact_match,
                "exact_match_threshold": exact_match_threshold,
                "shuffle_memories": shuffle_memories,
            },
        }
        res = OrcaClient._orca_request("POST", url, request_params)
        return orjson.loads(res.text)

    @staticmethod
    def get_index_values(db_name: str, index_name: str) -> dict[int, list[float]]:
        """Get the values of an index

        Args:
            db_name: The name of the database
            index_name: The name of the index

        Returns:
            The response from the get index values query
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/dump_index")
        request_params = {
            "params": {"db_name": db_name, "index_name": index_name},
        }

        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()

    @staticmethod
    def get_index_values_paginated(
        db_name: str,
        index_name: str,
        page_index: int = 0,
        page_size: int = 100,
    ) -> PagedResponse:
        """Get the values of an index paginated

        Args:
            db_name: The name of the database
            index_name: The name of the index
            page_index: The index of the page to return
            page_size: The size of the page to return

        Returns:
            A paged response with `dict[int, list[float]]`
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/dump_index_paginated")
        request_params = {
            "params": {
                "db_name": db_name,
                "index_name": index_name,
                "page_index": page_index,
                "page_size": page_size,
            },
        }

        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()

    @staticmethod
    def get_index_table(db_name: str, index_name: str) -> str:
        """
        Get the table of an index

        Args:
            db_name: The name of the database
            index_name: The name of the index

        Returns:
            The name of the table the index is associated with
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/get_index_table")
        request_params = {
            "params": {"db_name": db_name, "index_name": index_name},
        }

        return OrcaClient._orca_request("GET", url, request_params).json()

    @staticmethod
    def run_sql(db_name: str, query: str, params: list[None | int | float | bytes | str] = []) -> list[dict[str, Any]]:
        """
        Run a raw SQL select query

        Args:
            db_name: The name of the database
            query: The SQL query
            params: The parameters for the query

        Returns:
            The response from the SQL select query
        """
        url = os.path.join(OrcaClient.BASE_URL, "experimental/sql")
        request_params = {
            "params": {"db_name": db_name},
            "json": {"query": query, "params": params},
        }

        return OrcaClient._orca_request("POST", url, request_params).json()["rows"]

    @staticmethod
    def encode_text(
        strings: list[str], model: EmbeddingModel = EmbeddingModel.SENTENCE_TRANSFORMER
    ) -> list[list[float]]:
        """
        Encode a list of strings using the Roberta model

        Args:
            strings: The list of strings to encode

        Returns:
            A list of encoded strings with shape (`len(strings)`, `embedding_size`)
        """
        if model.value not in ["roberta", "sentence_transformer"]:
            raise ValueError(f"Unsupported model: {model.value}")
        url = os.path.join(OrcaClient.BASE_URL, f"experimental/encode/{model.value}")
        request_params = {
            "json": {"strings": strings},
        }
        return OrcaClient._orca_request("POST", url, request_params).json()

    @staticmethod
    def index_embed_text(
        db_name: str, index_name: str, strings: list[str], result_format: Literal["list", "pt"] = "pt"
    ) -> list[list[float]] | torch.Tensor:
        """Encode text values using the embedding model of a specific index.

        Args:
            db_name: The name of the database that the index belongs to
            index_name: The name of the index whose embedding will be used to encode the text
            strings: The list of strings to encode
            result_format: If `"list"`, return the results as a list of lists. If `"pt"`,
                return the results as a list of PyTorch tensors.

        Returns:
            * If `result_format` is `"list"`, this is a `list[list[float]]`
            * If `result_format` is `"pt"`, this is a Tensor with shape `(batch_size, mem_count, embedding_dim)`
        """
        url = os.path.join(
            OrcaClient.BASE_URL,
            f"experimental/index_encode/{db_name}/{index_name}",
        )
        request_params = {
            "json": {
                "strings": strings,
            },
        }
        results = OrcaClient._orca_request("POST", url, request_params).json()
        if result_format == "pt":
            import torch

            results = torch.tensor(results)
        return results

    @staticmethod
    def init_forward_pass(
        db_name: str,
        model_id: str,
        batch_size: int,
        model_version: str | None = None,
        seq_id: UUID | None = None,
        tags: set[str] | None = None,
        metadata: OrcaMetadataDict | None = None,
    ) -> list[int]:
        """
        Generate run ids for a batch of forward passes

        Args:
            db_name: The name of the database
            model_id: The id of the model
            batch_size: The batch size
            model_version: The version of the model (optional)
            seq_id: The sequence id for the forward pass (optional)
            tags: The tags for the forward pass (optional)
            metadata: The metadata for the forward pass (optional)

        Returns:
            The ids for the model runs
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/curate/init_forward_pass")
        request_params = {
            "json": {
                "db_name": db_name,
                "orca_model_id": model_id,
                "orca_model_version": model_version,
                "batch_size": batch_size,
                "seq_id": seq_id,
                "tags": list(tags),
                "metadata": metadata,
            },
        }
        return OrcaClient._orca_request("POST", url, request_params).json()

    @staticmethod
    def record_memory_weights(
        db_name: str,
        layer_name: str,
        run_ids: list[int],
        memory_ids: list[int],
        memory_weights: list[float],
    ) -> None:
        """
        Record the memory weights for a batch of forward passes

        Args:
            db_name: The name of the database
            run_ids: The ids of the model runs
            layer_name: The name of the lookup layer that the memory weights are for
            memory_weights: The memory weights for the model runs
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/curate/record_memory_weights")
        request_params = {
            "json": {
                "db_name": db_name,
                "layer_name": layer_name,
                "run_ids": run_ids,
                "memory_ids": memory_ids,
                "memory_weights": memory_weights,
            },
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def delete_model_runs(db_name: str, model_id: str, filters: list[ApiFilter]) -> None:
        """
        Delete curate tracking data for model runs

        Args:
            db_name: The name of the database
            model_id: The id of the model to delete runs for
            filters: Filters to select runs to delete
        """
        url = os.path.join(OrcaClient.BASE_URL, "/v1/curate/prune")
        request_params = {
            "params": {"db_name": db_name, "model_id": model_id},
            "json": {"filters": filters},
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def record_model_feedback(
        db_name: str,
        run_ids: list[int],
        values: list[float],
        name: str,
        kind: str,
    ) -> None:
        """
        Record model feedback

        Args:
            db_name: The name of the database
            run_ids: A list of the run ids
            values: A list of the feedback values - type should match the kind
            name: The name of the feedback - name and run_id combo must be unique
            kind: The kind of feedback as a string
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/curate/record_scores")
        request_params = {
            "json": {
                "db_name": db_name,
                "run_ids": run_ids,
                "scores": values,
                "name": name,
                "kind": kind,
            },
        }
        OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def record_model_input_output(
        db_name: str,
        run_ids: list[int],
        inputs: list[Any],
        outputs: list[Any],
    ) -> None:
        """Record input and output data for model runs

        Args:
            db_name: The name of the database
            run_ids: The ids of the model runs as returned by `init_forward_pass`
            inputs: The inputs for the model runs
            outputs: The outputs for the model runs
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/curate/record_model_in_out")
        request_params = {
            "json": {
                "db_name": db_name,
                "run_ids": run_ids,
                "inputs": inputs,
                "outputs": outputs,
            },
        }
        OrcaClient._orca_request("POST", url, request_params)
