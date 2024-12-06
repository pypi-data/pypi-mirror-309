import logging
import os
import re
from typing import Literal
from urllib.parse import ParseResult, urlparse

logger = logging.getLogger(__name__)


class OrcaFileLocation:
    path: str
    table: str | None = None

    def __init__(self, parsed_url: ParseResult, table: str | None = None):
        if not parsed_url.path:
            raise ValueError("file URL must contain a path")
        self.path = parsed_url.path

        if table and parsed_url.fragment:
            raise ValueError("cannot pass table explicitly and in URL fragment")
        self.table = table or parsed_url.fragment or None
        if self.table and not re.fullmatch("^[a-zA-Z_]+[a-zA-Z0-9_]*$", self.table):
            raise ValueError(f"Invalid table name {self.table}")

    @property
    def url(self) -> str:
        return f"file:{self.path}#{self.table}"

    def __str__(self):
        return self.url


class OrcaServerLocation:
    scheme: Literal["http", "https"]
    host: str
    api_key: str
    secret_key: str
    database: str
    table: str | None = None

    def __init__(
        self,
        parsed_url: ParseResult,
        api_key: str | None = None,
        secret_key: str | None = None,
        database: str | None = None,
        table: str | None = None,
    ):
        if parsed_url.scheme not in ("http", "https"):
            raise ValueError(f"Invalid scheme: {parsed_url.scheme}")
        self.scheme = parsed_url.scheme

        if "@" in parsed_url.netloc:
            credentials, self.host = parsed_url.netloc.split("@")
            if ":" not in credentials:
                raise ValueError(f"Invalid credentials: {credentials}")
            self.api_key, self.secret_key = credentials.split(":")
        else:
            self.host = parsed_url.netloc
            if api_key is None or secret_key is None:
                raise ValueError("api_key and secret_key must both be provided if they are not encoded in the URL")
            self.api_key = api_key
            self.secret_key = secret_key

        if database and parsed_url.path.lstrip("/") and database != parsed_url.path.lstrip("/"):
            raise ValueError("cannot pass different database names (explicitly and in URL path)")
        self.database = database or parsed_url.path.lstrip("/") or "default"
        if not re.fullmatch("^[a-zA-Z_]+[a-zA-Z0-9_]*$", self.database):
            raise ValueError(f"Invalid database name {self.database}")

        if table and parsed_url.fragment:
            raise ValueError("cannot pass table explicitly and in URL fragment")
        self.table = table or parsed_url.fragment or None
        if self.table and not re.fullmatch("^[a-zA-Z_]+[a-zA-Z0-9_]*$", self.table):
            raise ValueError(f"Invalid table name {self.table}")

    @property
    def base_url(self) -> str:
        return f"{self.scheme}://{self.host}/"

    @property
    def url(self) -> str:
        return f"{self.base_url}{self.database}" + (f"#{self.table}" if self.table else "")

    @property
    def url_with_credentials(self) -> str:
        return f"{self.scheme}://{self.api_key}:{self.secret_key}@{self.host}/{self.database}" + (
            f"#{self.table}" if self.table else ""
        )

    def __str__(self):
        return self.url + " (+ credentials)" if self.api_key and self.secret_key else self.url


def is_url(url: str | None) -> bool:
    """Check if a string is a URL."""
    return bool(url and urlparse(url).scheme)


class OrcaDBURLParser:
    _using_localhost_warning_logged = False
    _using_env_var_warning_logged = False

    @classmethod
    def parse_orcadb_url(
        cls,
        url: str | None = None,
        *,
        api_key: str | None = None,
        secret_key: str | None = None,
        database: str | None = None,
        table: str | None = None,
    ) -> OrcaFileLocation | OrcaServerLocation:
        """
        Parse an OrcaDB URL

        Args:
            url: The URL to parse. If not provided, the `ORCADB_URL` environment variable is used.
            api_key: API key to use (will override the api key in the URL)
            secret_key: Secret key to use (will override the secret key in the URL)
            database: The database to use.
            table: The table to use.
        """
        if url:
            parsed_url = urlparse(url)
            if parsed_url.scheme == "file":
                if database:
                    raise ValueError("Cannot pass database for file URL")
                return OrcaFileLocation(parsed_url, table)
            elif parsed_url.scheme == "http" or parsed_url.scheme == "https":
                return OrcaServerLocation(
                    parsed_url,
                    api_key or os.getenv("ORCADB_API_KEY"),
                    secret_key or os.getenv("ORCADB_SECRET_KEY"),
                    database,
                    table,
                )
            else:
                raise ValueError(f"Invalid scheme: {parsed_url.scheme}")
        url_env_var = os.getenv("ORCADB_URL")
        if url_env_var:
            if not cls._using_env_var_warning_logged:
                logger.info("Using ORCADB_URL environment variable to connect to OrcaDB.")
                if api_key and os.getenv("ORCADB_API_KEY"):
                    logger.warning("explicitly provided api_key is overriding ORCADB_API_KEY environment variable")
                if secret_key and os.getenv("ORCADB_SECRET_KEY"):
                    logger.warning(
                        "explicitly provided secret_key is overriding ORCADB_SECRET_KEY environment variable"
                    )
                cls._using_env_var_warning_logged = True
            return cls.parse_orcadb_url(
                url_env_var,
                database=database,
                table=table,
                api_key=api_key or os.getenv("ORCADB_API_KEY"),
                secret_key=secret_key or os.getenv("ORCADB_SECRET_KEY"),
            )
        if not cls._using_localhost_warning_logged:
            logger.warning(
                "No url was passed and no ORCADB_URL environment variable was found, defaulting to localhost:1583."
            )
            cls._using_localhost_warning_logged = True

        return OrcaServerLocation(
            urlparse("http://localhost:1583/"), api_key or "my_api_key", secret_key or "my_secret_key", database, table
        )


# reference the class method instead of the standalone function
parse_orcadb_url = OrcaDBURLParser.parse_orcadb_url
