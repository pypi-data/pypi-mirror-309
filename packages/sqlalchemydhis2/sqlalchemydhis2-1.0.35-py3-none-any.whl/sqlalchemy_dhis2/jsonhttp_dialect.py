from types import ModuleType
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy import types, __version__ as sqlalchemy_version, pool, select, sql, text, util
from sqlalchemy.engine.reflection import cache

import requests
import polars as pd
import duckdb
from duckdb_engine import DuckDBIdentifierPreparer, Dialect
from typing import Any, Dict, Optional, Tuple, Type
import sqlalchemy_dhis2 as module
from sqlalchemy_dhis2.connection import add_authorization
from sqlalchemy_dhis2.constants import _HEADER
from sqlalchemy_dhis2.exceptions import DatabaseHTTPError

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
    
class JSONHTTPDialect(Dialect):
    name = "dhis2"
    scheme = "http"
    driver = "duckdb_engine"
    supports_statement_cache = False
    identifier_preparer: DuckDBIdentifierPreparer
    
    #def __init__(self, *args: Any, **kwargs: Any) -> None:
    #    kwargs["use_native_hstore"] = False
    #    super().__init__(*args, **kwargs)
        
    @classmethod
    # pylint: disable=method-hidden
    def dbapi(cls) -> ModuleType:
        return module
        
    #@staticmethod
    #def dbapi(**kwargs: Any) -> Type[DBAPI]:
    #    return DBAPI
    
    #@classmethod
    #def import_dbapi(cls: Type["Dialect"]) -> Type[DBAPI]:
    #    return cls.dbapi()
    
    def create_connect_args(self, url):
        #
        # Parse the connection URL to extract credentials and JSON endpoint.
        #
        opts = url.translate_connect_args()
        opts.update(url.query)
        opts['path'] = opts.get('database','')
        opts1 = url.translate_connect_args(database="database")
        opts["url_config"] = dict(url.query)
        user = opts["url_config"].pop("user", None)
        if user is not None:
            opts["database"] += f"?user={user}"
        print(f"###OPT:::{ opts }####{opts1}")
        #return ([], opts)
        return (),opts

    def connect(self, *cargs: Any, **cparams: Any) -> Any:
        print(f"####{cargs}###::::{cparams}")
        host = cparams.get('host')
        database = cparams.get('path')
        collection= cparams.get('collection','resources')
        port=cparams.get('port',443)
        username=cparams.get('username'),
        password=cparams.get('password'),
        use_ssl= True,
        verify_ssl=None,
        token=None,
        auth=None,
        duckdb_path=":memory:",
        session = requests.Session()        
        # Save to DuckDB
        conn = duckdb.connect(duckdb_path)
        
        # by default session.verify is set to True
        if verify_ssl is not None and verify_ssl in ["False", "false"]:
            session.verify = False

        if use_ssl in ["True", "true",True]:
            proto = "https://"
        else:
            proto = "http://"
        if collection is not None:
            local_url = f"/api/{collection}"
            if database is not None:
                local_url = f"/{database}/api/{collection}"

            add_authorization(session, username, password, token)
            response = session.get(
                f"{proto}{host}:{port}{local_url}",
                headers=_HEADER,
            )
            if response.status_code != 200:
                raise DatabaseHTTPError(response.text, response.status_code)
                # Convert to Pandas DataFrame
            df = pd.DataFrame(response.json())


            conn.register("temp_table", df)
            conn.execute(f"DROP TABLE IF EXISTS {collection}")
            conn.execute(f"CREATE TABLE { collection } AS SELECT * FROM temp_table")
            conn.unregister("temp_table")

        return super().connect(*cargs, **cparams)

    def on_connect(self) -> None:
        pass
    
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
    """
    def execute(self, cursor, statement, parameters, context=None):
        
        Override execute to handle fetching JSON and saving to DuckDB.
        
        print(f"####FG{statement}###{parameters}")
        conn = context["dialect"].execute_json_query(
            url=parameters["url"],
            auth=parameters["auth"],
            duckdb_path=parameters["duckdb_path"],
            table_name=parameters["table_name"],
        )
        return conn.execute(statement)
    """
        
    def do_ping(self,conn: Any ) -> bool:
        return True

    @cache  # type: ignore[call-arg]
    def get_table_names(self, connection: "Connection", schema=None, **kw: "Any"):  # type: ignore[no-untyped-def]
        return super().get_table_names(connection, schema, **kw)


    @cache  # type: ignore[call-arg]
    def get_schema_names(self, connection: "Connection", **kw: "Any"):  # type: ignore[no-untyped-def]
       return super().get_schema_names(connection, **kw)