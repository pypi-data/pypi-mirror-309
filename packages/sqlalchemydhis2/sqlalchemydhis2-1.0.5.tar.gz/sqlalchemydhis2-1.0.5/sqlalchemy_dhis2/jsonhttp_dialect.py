from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy import types, __version__ as sqlalchemy_version
import requests
import polars as pd
import duckdb
from typing import Any

class DBAPI:
    paramstyle = "numeric_dollar" if sqlalchemy_version >= "2.0.0" else "qmark"
    apilevel = duckdb.apilevel
    threadsafety = duckdb.threadsafety

    # this is being fixed upstream to add a proper exception hierarchy
    Error = getattr(duckdb, "Error", RuntimeError)
    TransactionException = getattr(duckdb, "TransactionException", Error)
    ParserException = getattr(duckdb, "ParserException", Error)

    @staticmethod
    def Binary(x: Any) -> Any:
        return x
    
class JSONHTTPDialect(DefaultDialect):
    name = "dhis2"
    driver = "duckdb_engine"
    supports_statement_cache = False

    @classmethod
    # pylint: disable=method-hidden
    def dbapi(cls):
        return DBAPI
    
    def create_connect_args(self, url):
        """
        Parse the connection URL to extract credentials and JSON endpoint.
        """
        host = url.host
        username = url.username
        password = url.password
        endpoint = f"https://{host}" if not host.startswith("http") else host

        return (endpoint,), {
            "auth": (username, password),
            "duckdb_path": url.query.get("duckdb_path", ":memory:"),
        }

    def execute_json_query(self, url, auth, duckdb_path, table_name):
        """
        Fetch JSON data and save it into DuckDB.
        """
        # Fetch JSON data
        s = requests.Session()
        s.auth = auth
        response = s.get(url)
        response.raise_for_status()
        data = response.json()

        # Convert to Pandas DataFrame
        df = pd.DataFrame(data)

        # Save to DuckDB
        conn = duckdb.connect(duckdb_path)
        conn.register("temp_table", df)
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_table")
        conn.unregister("temp_table")

        return conn

    def execute(self, cursor, statement, parameters, context=None):
        """
        Override execute to handle fetching JSON and saving to DuckDB.
        """
        conn = context["dialect"].execute_json_query(
            url=parameters["url"],
            auth=parameters["auth"],
            duckdb_path=parameters["duckdb_path"],
            table_name=parameters["table_name"],
        )
        return conn.execute(statement)


