from enum import Enum
from typing import Any, Union

from verse.core import DataModel
from verse.internal.storage_core import Index

DocumentKeyType = Union[str, int, float, bool]


class DocumentType(str, Enum):
    """Document type."""

    JSON = "json"
    TEXT = "text"
    BYTES = "bytes"


class DocumentFieldType(str, Enum):
    """Document field type."""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    NULL = "null"


class DocumentKey(DataModel):
    """Document key."""

    id: DocumentKeyType
    """Document id."""

    pk: DocumentKeyType | None = None
    """Partition key."""


class DocumentProperties(DataModel):
    """Document properties."""

    etag: str | None = None
    """Document ETag."""


class DocumentItem(DataModel):
    """Document item."""

    key: DocumentKey
    """Document key."""

    value: dict[str, Any] | None = None
    """Document value."""

    properties: DocumentProperties | None = None
    """Document properties."""


class DocumentList(DataModel):
    """Document list."""

    items: list[DocumentItem]
    """List of documents."""


class DocumentCollectionConfig(DataModel):
    """Document collection config."""

    id_field: str | None = None
    """Id field name."""

    id_type: DocumentFieldType | None = None
    """Id field type."""

    pk_field: str | None = None
    """Partition key field name."""

    pk_type: DocumentFieldType | None = None
    """Partition key field type."""

    value_field: str | None = None
    """Value field name."""

    value_type: DocumentType = DocumentType.JSON
    """Value type."""

    indexes: list[Index] | None = None
    """Indexes."""

    nconfig: dict | None = None
    """Native config parameters."""


class DocumentQueryConfig(DataModel):
    """Query config."""

    paging: bool | None = False
    """A value indicating whether the results should be paged."""

    page_size: int | None = None
    """Page size."""
