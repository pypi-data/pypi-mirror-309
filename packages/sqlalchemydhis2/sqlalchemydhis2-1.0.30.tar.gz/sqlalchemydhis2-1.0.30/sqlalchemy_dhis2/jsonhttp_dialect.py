from types import ModuleType
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy import types, __version__ as sqlalchemy_version, pool, select, sql, text, util
from sqlalchemy.engine.reflection import cache

import requests
import polars as pd
import duckdb
from duckdb_engine import DuckDBIdentifierPreparer
from typing import Any, Dict, Optional, Tuple
import sqlalchemy_dhis2 as module

duckdb_version: str = duckdb.__version__
supports_attach: bool = duckdb_version >= "0.7.0"
supports_user_agent: bool = duckdb_version >= "0.9.2"

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
    scheme = "http"
    driver = "rest"
    supports_statement_cache = False
    identifier_preparer: DuckDBIdentifierPreparer
    
    @classmethod
    # pylint: disable=method-hidden
    def dbapi(cls) -> ModuleType:
        return module
    
    def create_connect_args(self, url):
        #
        # Parse the connection URL to extract credentials and JSON endpoint.
        #
        opts = url.translate_connect_args()
        opts.update(url.query)
        return ([], opts)

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
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_table")
        conn.unregister("temp_table")

        return conn

    def execute(self, cursor, statement, parameters, context=None):
        """
        Override execute to handle fetching JSON and saving to DuckDB.
        """
        print(f"####FG{statement}###{parameters}")
        conn = context["dialect"].execute_json_query(
            url=parameters["url"],
            auth=parameters["auth"],
            duckdb_path=parameters["duckdb_path"],
            table_name=parameters["table_name"],
        )
        return conn.execute(statement)
    
    def do_ping(self,conn: Any ) -> bool:
        return True

    @cache  # type: ignore[call-arg]
    def get_table_names(self, connection: "Connection", schema=None, **kw: "Any"):  # type: ignore[no-untyped-def]
        """
        Return unquoted database_name.schema_name unless either contains spaces or double quotes.
        In that case, escape double quotes and then wrap in double quotes.
        SQLAlchemy definition of a schema includes database name for databases like SQL Server (Ex: databasename.dbo)
        (see https://docs.sqlalchemy.org/en/20/dialects/mssql.html#multipart-schema-names)
        """

        if not supports_attach:
            return super().get_table_names(connection, schema, **kw)

        s = """
            SELECT database_name, schema_name, table_name
            FROM duckdb_tables()
            WHERE schema_name NOT LIKE 'pg\\_%' ESCAPE '\\'
            """
        sql, params = self._build_query_where(schema_name=schema)
        s += sql
        rs = connection.execute(text(s), params)

        return [
            table
            for (
                db,
                sc,
                table,
            ) in rs
        ]


    @cache  # type: ignore[call-arg]
    def get_schema_names(self, connection: "Connection", **kw: "Any"):  # type: ignore[no-untyped-def]
        """
        Return unquoted database_name.schema_name unless either contains spaces or double quotes.
        In that case, escape double quotes and then wrap in double quotes.
        SQLAlchemy definition of a schema includes database name for databases like SQL Server (Ex: databasename.dbo)
        (see https://docs.sqlalchemy.org/en/20/dialects/mssql.html#multipart-schema-names)
        """

        if not supports_attach:
            return super().get_schema_names(connection, **kw)

        s = """
            SELECT database_name, schema_name AS nspname
            FROM duckdb_schemas()
            WHERE schema_name NOT LIKE 'pg\\_%' ESCAPE '\\'
            ORDER BY database_name, nspname
            """
        rs = connection.execute(text(s))

        qs = self.identifier_preparer.quote_schema
        return [qs(".".join(nspname)) for nspname in rs]
    
    def _build_query_where(
        self,
        table_name: Optional[str] = None,
        schema_name: Optional[str] = None,
        database_name: Optional[str] = None,
    ) -> Tuple[str, Dict[str, str]]:
        sql = ""
        params = {}

        # If no database name is provided, try to get it from the schema name
        # specified as "<db name>.<schema name>"
        # If only a schema name is found, database_name will return None
        if database_name is None and schema_name is not None:
            database_name, schema_name = self.identifier_preparer._separate(schema_name)

        if table_name is not None:
            sql += "AND table_name = :table_name\n"
            params.update({"table_name": table_name})

        if schema_name is not None:
            sql += "AND schema_name = :schema_name\n"
            params.update({"schema_name": schema_name})

        if database_name is not None:
            sql += "AND database_name = :database_name\n"
            params.update({"database_name": database_name})

        return sql, params