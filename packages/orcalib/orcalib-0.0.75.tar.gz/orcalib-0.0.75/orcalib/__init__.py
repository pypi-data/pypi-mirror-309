import logging
from typing import Any

from pandas import DataFrame
from typing_extensions import deprecated

from orca_common import (
    EXACT_MATCH_THRESHOLD,
    CatchupStatus,
    ColumnName,
    ImageFormat,
    Order,
    RowDict,
    TableCreateMode,
)

__all__ = [
    "TableCreateMode",
    "ImageFormat",
    "CatchupStatus",
    "EXACT_MATCH_THRESHOLD",
    "ColumnName",
    "Order",
    "RowDict",
]

from orcalib.database import _with_default_database_method

from .batched_scan_result import BatchedScanResult, BatchedScanResultBuilder
from .client import OrcaClient
from .database import OrcaDatabase
from .exceptions import OrcaBadRequestException, OrcaException, OrcaNotFoundException
from .file_ingestor import (
    CSVIngestor,
    HFDatasetIngestor,
    JSONIngestor,
    JSONLIngestor,
    ParquetIngestor,
    PickleIngestor,
)
from .index_handle import IndexHandle
from .index_query import DefaultIndexQuery, VectorIndexQuery
from .memoryset import (
    EmbeddingFinetuningMethod,
    EmbeddingModel,
    EmbeddingTrainingArguments,
    LabeledMemory,
    LabeledMemoryLookup,
    LabeledMemoryset,
    LabeledMemorysetV2,
    LanceDBStorageBackend,
    Memory,
    MemoryLookup,
    MilvusStorageBackend,
    StorageBackend,
)
from .orca_chat import OrcaChat
from .orca_expr import ColumnHandle, OrcaExpr
from .orca_torch_mixins import ClassificationMode, DatabaseIndexName, ProjectionMode
from .orca_types import (  # BoolT,
    BFloat16T,
    DocumentT,
    EnumT,
    EnumTypeHandle,
    Float16T,
    Float32T,
    Float64T,
    FloatT,
    ImageT,
    Int8T,
    Int16T,
    Int32T,
    Int64T,
    IntT,
    NumericTypeHandle,
    OrcaTypeHandle,
    TextT,
    UInt8T,
    UInt16T,
    UInt32T,
    UInt64T,
    VectorT,
)
from .rac import (
    EvalResult,
    MCERHead,
    PredictionResult,
    RACHeadType,
    RACModel,
    RACModelConfig,
    RACModelV2,
    RACTrainingArguments,
    SimpleClassifier,
    SimpleMMOEHead,
    TrainingConfig,
)
from .table import TableHandle
from .temp_database import TemporaryDatabase, TemporaryTable

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@deprecated("Use set_orca_credentials instead.")
def set_credentials(*, api_key: str, secret_key: str, endpoint: str | None = None) -> None:
    OrcaClient.set_credentials(api_key=api_key, secret_key=secret_key, base_url=endpoint)


@deprecated("Pass credentials to OrcaDatabase constructor instead.")
def set_orca_credentials(
    *,
    api_key: str | None,  # this is optional to prevent type issues with os.getenv
    secret_key: str | None,  # this is optional to prevent type issues with os.getenv
    endpoint: str | None = None,
) -> None:
    """
    Set the credentials for the Orca client. This must be called before any other Orca functions.
    This can also be called multiple times to change the credentials.

    Args:
        api_key: API key
        secret_key: Secret key
        endpoint: Endpoint (optional)

    Examples:
        >>> dotenv.load_dotenv()
        >>> set_orca_credentials(
        ...     api_key=os.getenv("ORCADB_API_KEY"),
        ...     secret_key=os.getenv("ORCADB_SECRET_KEY"),
        ...     endpoint=os.getenv("ORCADB_ENDPOINT"),
        ... )
    """
    if not api_key or not secret_key:
        raise ValueError("API key and secret key must be provided.")
    OrcaClient.set_credentials(api_key=api_key, secret_key=secret_key, base_url=endpoint)


def check_orca_version_compatibility() -> bool | None:
    """
    Check if the OrcaLib version is compatible with the OrcaDB instance version and log a warning if not.

    Returns:
        True if the versions match, False if they do not, None if the version check is skipped

    Examples:
        >>> check_orca_version_compatibility()
    """
    return OrcaClient.check_version_compatibility()


# TODO: Remove the functions below, as they are just wrappers around the database methods


@_with_default_database_method
def create_table(
    db: OrcaDatabase,
    table_name: str,
    if_table_exists: TableCreateMode = TableCreateMode.ERROR_IF_TABLE_EXISTS,
    **columns: OrcaTypeHandle,
) -> TableHandle:
    """
    Create a table in the default database. This is a convenience function that calls `create_table`
    on the default db.

    Args:
        table_name: Name of the table
        if_table_exists: What to do if the table already exists
        **columns: Columns of the table (name -> type mapping)

    Returns:
        TableHandle

    Examples:
        >>> import orcalib as orca
        >>> orca.create_table("my_table", id=orca.Int64T, name=orca.TextT)
    """
    return db.create_table(table_name, if_table_exists, **columns)


@_with_default_database_method
def get_table(db: OrcaDatabase, table_name: str) -> TableHandle:
    """
    Get a table from the default database. This is a convenience function that calls `get_table` on the default db.

    Args:
        table_name: Name of the table

    Returns:
        TableHandle

    Examples:
        >>> import orcalib as orca
        >>> orca.get_table("my_table")
    """
    return db.get_table(table_name)


@_with_default_database_method
def list_tables(db: OrcaDatabase) -> list[str]:
    """
    List tables in the default database. This is a convenience function that calls `list_tables` on the default db.

    Returns:
        List of table names

    Examples:
        >>> import orcalib as orca
        >>> orca.list_tables()
    """
    return db.list_tables()


@_with_default_database_method
def backup(db: OrcaDatabase) -> tuple[str, str]:
    """
    Backup the default database. This is a convenience function that calls `backup` on the default db.

    Returns:
        Backup path and backup name

    Examples:
        >>> import orcalib as orca
        >>> orca.backup()
    """
    return db.backup()


@_with_default_database_method
def get_index(db: OrcaDatabase, index_name: str) -> IndexHandle:
    """
    Get an index from the default database. This is a convenience function that calls `get_index` on the default db.

    Args:
        index_name: Name of the index

    Returns:
        IndexHandle

    Examples:
        >>> import orcalib as orca
        >>> index_handle = orca.get_index("my_index")
    """
    return db.get_index(index_name)


@_with_default_database_method
def create_vector_index(
    db: OrcaDatabase,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
) -> None:
    """
    Create a vector index for default db. This is a convenience function that calls `create_vector_index` on the default db.

    Args:
        index_name: Name of the index
        table_name: Name of the table
        column: Name of the column
        error_if_exists: Whether to raise an error if the index already exists
    """
    db.create_vector_index(index_name, table_name, column, error_if_exists)


@_with_default_database_method
def create_document_index(
    db: OrcaDatabase,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
) -> None:
    """
    Create a document index for default db. This is a convenience function that calls `create_document_index` on the default db.

    Args:
        index_name: Name of the index
        table_name: Name of the table
        column: Name of the column
        error_if_exists: Whether to raise an error if the index already
            exists (default: True)

    Examples:
        >>> import orcalib as orca
        >>> orca.create_document_index("my_index", "my_table", "my_column")
    """
    db.create_document_index(index_name, table_name, column, error_if_exists)


@_with_default_database_method
def create_text_index(
    db: OrcaDatabase,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
) -> None:
    """
    Create a text index for default db. This is a convenience function that calls `create_text_index` on the default db.

    Args:
        index_name: Name of the index
        table_name: Name of the table
        column: Name of the column
        error_if_exists: Whether to raise an error if the index already
            exists (default: True)

    Examples:
        >>> import orcalib as orca
        >>> orca.create_text_index("my_index", "my_table", "my_column")
    """
    db.create_text_index(index_name, table_name, column, error_if_exists)


@_with_default_database_method
def create_btree_index(
    db: OrcaDatabase,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
) -> None:
    """
    Create a btree index for default db. This is a convenience function that calls `create_btree_index` on the default db.

    Args:
        index_name: Name of the index
        table_name: Name of the table
        column: Name of the column
        error_if_exists: Whether to raise an error if the index already exists

    Examples:
        >>> import orcalib as orca
        >>> orca.create_btree_index("my_index", "my_table", "my_column")
    """
    db.create_btree_index(index_name, table_name, column, error_if_exists)


@_with_default_database_method
def drop_index(db: OrcaDatabase, index_name: str, error_if_not_exists: bool = True) -> None:
    """
    Drop an index from the default database. This is a convenience function that calls `drop_index` on the default db.

    Args:
        index_name: Name of the index
        error_if_not_exists: Whether to raise an error if the index does not exist

    Examples:
        >>> import orcalib as orca
        >>> orca.drop_index("my_index")
    """
    db.drop_index(index_name, error_if_not_exists)


@_with_default_database_method
def drop_table(db: OrcaDatabase, table_name: str, error_if_not_exists: bool = True) -> None:
    """
    Drop a table from the default database. This is a convenience function that calls `drop_table` on the default db.

    Args:
        table_name: Name of the table
        error_if_not_exists: Whether to raise an error if the table does not exist

    Examples:
        >>> import orcalib as orca
        >>> orca.drop_table("my_table")
    """
    db.drop_table(table_name, error_if_not_exists)


@_with_default_database_method
def search_memory(
    db: OrcaDatabase,
    index_name: str,
    query: list[float],
    limit: int,
    columns: list[str] | None = None,
) -> Any:
    """
    Search memory for default db. This is a convenience function that calls `search_memory` on the default db.

    Args:
        index_name: Name of the index
        query: Query
        limit: Limit
        columns: Columns to return (optional)

    Examples:
        >>> import orcalib as orca
        >>> orca.search_memory("my_index", [1.0, 2.0], 10)
    """
    return db.search_memory(index_name, query, limit, columns)


@_with_default_database_method
def scan_index(
    db: OrcaDatabase,
    index_name: str,
    query: Any,
) -> DefaultIndexQuery:
    """
    Scan an index for default db. This is a convenience function that calls `scan_index` on the default db.

    Args:
        index_name: Name of the index
        query: Query

    Returns:
        DefaultIndexQuery

    Examples:
        >>> import orcalib as orca
        >>> orca.scan_index("my_index", orca.OrcaExpr("$EQ", (orca.ColumnHandle("my_table", "my_column"), 42)))
    """
    return db.scan_index(index_name, query)


@_with_default_database_method
def vector_scan_index(
    db: OrcaDatabase,
    index_name: str,
    query: Any,
) -> VectorIndexQuery:
    """
    Scan a vector index for default db. This is a convenience function that calls `vector_scan_index` on the default db.

    Args:
        index_name: Name of the index
        query: Query

    Returns:
        VectorIndexQuery

    Examples:
        >>> import orcalib as orca
        >>> orca.vector_scan_index("my_index", orca.OrcaExpr("$EQ", (orca.ColumnHandle("my_table", "my_column"), 42)))
    """
    return db.vector_scan_index(index_name, query)


@_with_default_database_method
def full_vector_memory_join(
    db: OrcaDatabase,
    *,
    index_name: str,
    memory_index_name: str,
    num_memories: int,
    query_columns: list[str],
    page_index: int,
    page_size: int,
) -> dict[str, list[tuple[list[float], Any]]]:
    """
    Join a vector index with a memory index for default db. This is a convenience function that calls `full_vector_memory_join` on the default db.

    Args:
        index_name: Name of the index
        memory_index_name: Name of the memory index
        num_memories: Number of memories
        query_columns: Query columns
        page_index: Page index
        page_size: Page size

    Returns:
        Results

    Examples:
        >>> import orcalib as orca
        >>> orca.full_vector_memory_join("my_index", "my_memory_index", 10, ["my_column"], 0, 10)
    """
    return db.full_vector_memory_join(index_name, memory_index_name, num_memories, query_columns, page_index, page_size)


@_with_default_database_method
def query(db: OrcaDatabase, query: str, params: list[None | int | float | bytes | str] = []) -> DataFrame:
    """
    Execute a raw SQL query. This is a convenience function that calls `query` on the default db.

    Args:
        query: Query
        params: Parameters

    Returns:
        the query result in a DataFrame

    Examples:
        >>> import orcalib as orca
        >>> orca.query("SELECT text, label FROM my_table")
        DataFrame(
            text    | label
            "hello" | 1
            "world" | 2
        )
    """
    return db.query(query, params)
