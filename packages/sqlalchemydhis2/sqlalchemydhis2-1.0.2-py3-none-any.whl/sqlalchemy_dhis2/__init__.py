# Register the custom dialect
from sqlalchemy.dialects import registry as _registry

__version__ = "1.0.2"

_registry.register(
    "dhis2", "sqlalchemy_access.jsonhttp_dialect", "JSONHTTPDialect"
)