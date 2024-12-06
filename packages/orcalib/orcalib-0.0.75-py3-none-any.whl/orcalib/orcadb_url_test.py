import pytest

from orcalib.orcadb_url import (
    OrcaFileLocation,
    OrcaServerLocation,
    is_url,
    parse_orcadb_url,
)


def test_parse_file_uri():
    location = parse_orcadb_url("file:./temp/local.db#airline_sentiment")
    assert isinstance(location, OrcaFileLocation)
    assert location.path == "./temp/local.db"
    assert location.table == "airline_sentiment"
    assert location.url == "file:./temp/local.db#airline_sentiment"


def test_parse_server_uri():
    location = parse_orcadb_url("https://asdjfb:iapdsbf@docs-e04c4fecfc.us-east1.gcp.orcadb.cloud/wiki#samples")
    assert isinstance(location, OrcaServerLocation)
    assert location.host == "docs-e04c4fecfc.us-east1.gcp.orcadb.cloud"
    assert location.api_key == "asdjfb"
    assert location.secret_key == "iapdsbf"
    assert location.database == "wiki"
    assert location.table == "samples"
    assert location.base_url == "https://docs-e04c4fecfc.us-east1.gcp.orcadb.cloud/"
    assert location.url == "https://docs-e04c4fecfc.us-east1.gcp.orcadb.cloud/wiki#samples"
    assert (
        location.url_with_credentials == "https://asdjfb:iapdsbf@docs-e04c4fecfc.us-east1.gcp.orcadb.cloud/wiki#samples"
    )


def test_parse_localhost_uri():
    location = parse_orcadb_url("http://my_api_key:my_secret_key@localhost:1583/default")
    assert isinstance(location, OrcaServerLocation)
    assert location.host == "localhost:1583"
    assert location.api_key == "my_api_key"
    assert location.secret_key == "my_secret_key"
    assert location.database == "default"
    assert location.table is None
    assert location.base_url == "http://localhost:1583/"
    assert location.url == "http://localhost:1583/default"
    assert location.url_with_credentials == "http://my_api_key:my_secret_key@localhost:1583/default"


def test_parse_from_env_vars(monkeypatch):
    monkeypatch.setenv("ORCADB_URL", "http://abc:def@instance.ocradb.cloud/hi")
    location = parse_orcadb_url()
    assert isinstance(location, OrcaServerLocation)
    assert location.host == "instance.ocradb.cloud"
    assert location.api_key == "abc"
    assert location.secret_key == "def"
    assert location.database == "hi"
    assert location.table is None
    assert location.base_url == "http://instance.ocradb.cloud/"
    assert location.url == "http://instance.ocradb.cloud/hi"
    assert location.url_with_credentials == "http://abc:def@instance.ocradb.cloud/hi"


def test_parse_from_env_var_with_overwrites(monkeypatch):
    monkeypatch.setenv("ORCADB_URL", "http://abc:def@instance.ocradb.cloud")
    location = parse_orcadb_url(None, database="test_db", table="test_table")
    assert isinstance(location, OrcaServerLocation)
    assert location.database == "test_db"
    assert location.table == "test_table"
    assert location.api_key == "abc"
    assert location.secret_key == "def"


def test_parse_default():
    location = parse_orcadb_url()
    assert isinstance(location, OrcaServerLocation)
    assert location.host == "localhost:1583"
    assert location.api_key == "my_api_key"
    assert location.secret_key == "my_secret_key"
    assert location.database == "default"
    assert location.table is None
    assert location.base_url == "http://localhost:1583/"
    assert location.url == "http://localhost:1583/default"
    assert location.url_with_credentials == "http://my_api_key:my_secret_key@localhost:1583/default"


def test_parse_server_explicit_params():
    location = parse_orcadb_url(
        "https://instance.ocradb.cloud",
        database="default",
        table="samples",
        api_key="abc",
        secret_key="def",
    )
    assert isinstance(location, OrcaServerLocation)
    assert location.host == "instance.ocradb.cloud"
    assert location.api_key == "abc"
    assert location.secret_key == "def"
    assert location.database == "default"
    assert location.table == "samples"
    assert location.url == "https://instance.ocradb.cloud/default#samples"


def test_parse_without_uri_with_explicit_params():
    location = parse_orcadb_url(
        None,
        database="memoryset_test_db",
        api_key="abc",
        secret_key="def",
        table="test_table",
    )
    assert isinstance(location, OrcaServerLocation)
    assert location.api_key == "abc"
    assert location.secret_key == "def"
    assert location.base_url == "http://localhost:1583/"
    assert location.database == "memoryset_test_db"
    assert location.table == "test_table"


def test_invalid_scheme():
    with pytest.raises(ValueError):
        parse_orcadb_url("ftp://invalid_scheme")


def test_invalid_credentials():
    with pytest.raises(ValueError):
        parse_orcadb_url("http://my_api_key@localhost:1583/default")


def test_missing_credentials():
    with pytest.raises(ValueError):
        parse_orcadb_url("http://localhost:1583/")


def test_invalid_table_name():
    with pytest.raises(ValueError):
        parse_orcadb_url("file:./temp/local.db#table_name=something")
    with pytest.raises(ValueError):
        parse_orcadb_url("file:./temp/local.db#123table")
    with pytest.raises(ValueError):
        parse_orcadb_url("http://my_api_key:my_secret_key@localhost:1583/#table_name=bad_table")


def test_invalid_database_name():
    with pytest.raises(ValueError):
        parse_orcadb_url("http://my_api_key:my_secret_key@localhost:1583/123database_name")
    with pytest.raises(ValueError):
        parse_orcadb_url("http://my_api_key:my_secret_key@localhost:1583/database%^&")
    with pytest.raises(ValueError):
        parse_orcadb_url("http://my_api_key:my_secret_key@localhost:1583/database/name")


def test_duplicate_non_matching_database_name():
    with pytest.raises(ValueError):
        parse_orcadb_url("file:./temp/local.db/not_default#airline_sentiment", database="default")
    with pytest.raises(ValueError):
        parse_orcadb_url("http://my_api_key:my_secret_key@localhost:1583/not_default", database="default")


def test_duplicate_table_name():
    with pytest.raises(ValueError):
        parse_orcadb_url("file:./temp/local.db#airline_sentiment", table="airline_sentiment")
    with pytest.raises(ValueError):
        parse_orcadb_url("http://my_api_key:my_secret_key@localhost:1583/default#samples", table="samples")


def test_is_url():
    assert is_url("file:./temp/local.db#airline_sentiment")
    assert is_url("https://asdjfb:iapdsbf@docs-e04c4fecfc.us-east1.gcp.orcadb.cloud/wiki#samples")
    assert is_url("http://my_api_key:my_secret_key@localhost:1583/default")
    assert is_url("ftp://invalid_scheme")
    assert not is_url("airline_sentiment")
    assert not is_url("default")
    assert not is_url(None)
