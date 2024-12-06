# Register the custom dialect
from sqlalchemy.dialects import registry as _registry

__version__ = "1.0.3"

_registry.register(
    "dhis2", "sqlalchemy_dhis2.jsonhttp_dialect", "JSONHTTPDialect"
)