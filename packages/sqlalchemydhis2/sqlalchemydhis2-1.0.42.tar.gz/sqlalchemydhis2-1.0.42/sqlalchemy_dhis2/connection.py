import logging
from typing import Any, Optional, Tuple

from requests import Session
import polars as pd

from .table_reflect import SolrTableReflection
from . import type_map
from .constants import _HEADER
from .message_formatter import MessageFormatter
from .exceptions import ConnectionClosedException,ProgrammingError, DatabaseHTTPError, CursorClosedException, UninitializedResultSetError
import duckdb

apilevel = "2.0"  # pylint: disable=invalid-name
threadsafety = 3  # pylint: disable=invalid-name
paramstyle = "qmark"  # pylint: disable=invalid-name
default_storage_plugin = ""  # pylint: disable=invalid-name

# Python DB API 2.0 classes
class Cursor:
    # pylint: disable=too-many-instance-attributes

    mf = MessageFormatter()
    __c: duckdb.DuckDBPyConnection
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        host,
        database,
        username,
        password,
        collection,
        port,
        proto,
        session,
        duckdb_path,
        conn,
        c: duckdb.DuckDBPyConnection,
        **kwargs: Any
    ):
        self.__c = c
        self.arraysize = 1
        self.database = database
        self.username = username
        self.password = password
        self.collection = collection
        self.description = None
        self.host = host
        self.port = port
        self.proto = proto
        self._session = session
        self.duckdb_path = duckdb_path
        self._connected = True
        self.connection = conn
        self._result_set = None
        self._result_set_metadata = None
        self._result_set_status = None
        self.rowcount = -1
        self.lastrowid = None
        self.default_storage_plugin = None

    def _native_result_types(self, column_types):
        for result in self._result_set:
            i = 0  # Column positional index
            for column_type in column_types:
                if result[i]:
                    result[i] = type_map.result_conversion_mapping[type(column_type)](
                        result[i]
                    )
                i += 1

        self._result_set = list(tuple(result for result in self._result_set))

    @property
    def connected(self):
        return self._connected

    # Decorator for methods which require connection
    def connected_(func):  # pylint: disable=no-self-argument # noqa: B902
        def func_wrapper(self, *args, **kwargs):
            if self.connected is False:
                raise CursorClosedException("Cursor object is closed")
            if self.connection.connected is False:
                raise ConnectionClosedException("Connection object is closed")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return func_wrapper

    @staticmethod
    def substitute_in_query(string_query, parameters):
        query = string_query

        # Statement semi-colon is not supported in Solr syntax
        if query.endswith(";"):
            query = query[:-1]

        for param in parameters:
            if isinstance(param, str):
                query = query.replace("?", f"{param!r}", 1)
            else:
                query = query.replace("?", str(param), 1)
        return query

    @staticmethod
    # pylint: disable=too-many-arguments
    def submit_query(query, host, port, proto, database, collection, session):
        print(f"######@QUERY:{query}")
        local_payload = query
        url = f"{proto}{host}:{port}/{database}/api/{collection}"
        return session.get(
            url,
            #params=local_payload,
            headers=_HEADER,
        )

    @connected_
    def getdesc(self):
        return self.description

    @connected_
    def close(self):
        self._connected = False

    @connected_
    def execute(
        self, 
        statement: str,  
        parameters: Optional[Tuple] = None,
        context: Optional[Any] = None,
    ) -> None:
    
        """
        Prepare and execute a database query.

        Parameters may be provided as sequence and will be
        bound to variables in the query. Variables are specified in a
        question mark notation.

        Args:
             operation (str): The query to be executed
             parameters (Tuple): The query parameters
        """
        print(f"XXX:{statement}xxxxx:::{parameters}")
        result = self.submit_query(
            self.substitute_in_query(statement, parameters),
            self.host,
            self.port,
            self.proto,
            self.database,
            self.collection,
            self._session,
        )

        logging.info(self.mf.format("Query:", statement))

        if result.status_code != 200:
            raise DatabaseHTTPError(result.text, result.status_code)

        rows = result.json()
        try:
            if statement.lower() == "commit":  # this is largely for ipython-sql
                self.__c.commit()
            elif statement.lower() in (
                "register",
                "register(?, ?)",
                "register($1, $2)",
            ):
                assert parameters and len(parameters) == 2, parameters
                view_name, df = parameters
                self.__c.register(view_name, df)
            elif parameters is None:
                self.__c.execute(statement)
            else:
                self.__c.execute(statement, parameters)
        except RuntimeError as e:
            if e.args[0].startswith("Not implemented Error"):
                raise NotImplementedError(*e.args) from e
            elif (
                e.args[0]
                == "TransactionContext Error: cannot commit - no transaction is active"
            ):
                return
            else:
                raise e

        return self

    @connected_
    def fetchone(self):
        """Fetches the next row of a query result set, returning a single object,
        or None when no more data is available.

        An UninitializedResultSetError is raised if the previous call to
        .execute*() did not produce any result set or no call was issued yet."""
        return None

    @connected_
    def fetchmany(self, size=None):
        """Fetches the next set of rows of a query result, returning a list of tuples.
        An empty list is returned when no more rows are available.

        Args:
            size (int): The size of the result subset to return. Default is 1.

        Returns:
            list(tuple): The result subset.

        An UninitializedResultSetError exception is raised if the previous call to
        .execute*() did not produce any result set or no call was issued yet.
        """

        return []

    @connected_
    def fetchall(self):
        """
        Fetches all remaining rows of a query result.

        An UninitializedResultSetError exception is raised if the previous call to
        .execute*() did not produce any result set or no call was issued yet.
        """
        return []

    @connected_
    def get_query_metadata(self):
        return self._result_set_metadata

    def get_default_plugin(self):
        return self.default_storage_plugin

    def __iter__(self):
        return self._result_set.__iter__()

class Connection:
    # pylint: disable=too-many-instance-attributes

    mf = MessageFormatter()

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        host,
        database,
        username,
        password,
        collection,
        port,
        proto,
        session,
        duckdb_path,
        conn,
        **kwargs: Any
    ):

        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.collection = collection
        self.proto = proto
        self.port = port
        self._session = session
        self._connected = True
        self.duckdb_path = duckdb_path,
        self.conn = conn

    @property
    def session(self):
        return self._session

    @property
    def connected(self):
        return self._connected

    # Decorator for methods which require connection
    def connected_(func):  # pylint: disable=no-self-argument # noqa: B902
        def func_wrapper(self, *args, **kwargs):
            if self.connected is False:
                logging.error(
                    self.mf.format("ConnectionClosedException in func_wrapper")
                )
                raise ConnectionClosedException("Connection object is closed")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return func_wrapper

    @connected_
    def close(self):
        self._connected = False

    @connected_
    def commit(self):
        """
        JSON/HTTP does not support commit in the transactional context
        """

    @connected_
    def rollback(self):
        """
        JSON/HTTP does not support rollback
        """

    @connected_
    def cursor(self):
        return Cursor(
            self.host,
            self.database,
            self.username,
            self.password,
            self.collection,
            self.port,
            self.proto,
            self._session,
            self.duckdb_path,
            self.conn,
            self,
        )

# pylint: disable=too-many-arguments
def connect(
    host,
    database,
    collection="resources",
    port=443,
    username=None,
    password=None,
    use_ssl= True,
    verify_ssl=None,
    token=None,
    auth=None,
    duckdb_path=":memory:",
    **cparams,
):
    session = Session()        
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
        
    return Connection(
        host,
        database,
        username,
        password,
        collection,
        port,
        proto,
        session,
        duckdb_path,
        conn
    )


def add_authorization(session, username, password, token):
    if token is not None:
        session.headers.update({"Authorization": f"Bearer {token}"})
    else:
        session.auth = (username, password)