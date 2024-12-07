# Register the custom dialect
from sqlalchemy.dialects import registry as _registry

__version__ = "1.0.41"

_registry.register(
    "dhis2", "sqlalchemy_dhis2.jsonhttp_dialect", "JSONHTTPDialect"
)

from sqlalchemy_dhis2.connection import connect
from sqlalchemy_dhis2.exceptions import (
    DataError,
    DatabaseError,
    DatabaseHTTPError,
    Error,
    IntegrityError,
    InternalError,
    AuthenticationError,
    OperationalError,
    ProgrammingError,
    CursorClosedException,
    ConnectionClosedException,
    UninitializedResultSetError
)


__all__ = [
    'connect',
    'apilevel',
    'threadsafety',
    'paramstyle',
    'DataError',
    'DatabaseError',
    'DatabaseHTTPError',
    'Error',
    'IntegrityError',
    'InternalError',
    'AuthenticationError',
    'OperationalError',
    'ProgrammingError',
    'CursorClosedException',
    'ConnectionClosedException',
    'UninitializedResultSetError'
    
]


apilevel = '2.0'
# Threads may share the module and connections
threadsafety = 3
paramstyle = 'qmark'