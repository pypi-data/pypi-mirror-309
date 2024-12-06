from datetime import datetime
from enum import Enum
from typing import Literal, Union

from verse.core import DataModel


class MatchCondition(DataModel):
    """Match condition."""

    exists: bool | None = None
    """Check item exists."""

    if_match: str | None = None
    """If match."""

    if_none_match: str | None = None
    """If none match."""

    if_modified_since: datetime | None = None
    """If modified since."""

    if_unmodified_since: datetime | None = None
    """If unmodified since."""

    if_version_match: str | None = None
    """If version match."""

    if_version_not_match: str | None = None
    """If version not match."""


class BaseIndex(DataModel):
    """Store index."""

    type: str
    """Index type."""

    name: str | None = None
    """Index name."""


class WildcardIndex(BaseIndex):
    """Wildcard index."""

    path: str = "*"
    """Wilcard path."""

    excluded: list[str] = []
    """Excluded paths."""

    type: Literal["wildcard"] = "wildcard"
    """Index type."""


class FieldIndex(BaseIndex):
    """Field index."""

    field: str
    """Index field."""

    field_type: str | None = None
    """Field type."""

    type: Literal["field"] = "field"
    """Index type."""


class ExcludeIndex(BaseIndex):
    """Exclude index."""

    field: str
    """Index field."""

    field_type: str | None = None
    """Field type."""

    type: Literal["exclude"] = "exclude"


class RangeIndex(BaseIndex):
    """Field index."""

    field: str
    """Index field."""

    field_type: str | None = None
    """Field type."""

    type: Literal["range"] = "range"
    """Index type."""


class HashIndex(BaseIndex):
    """Field index."""

    field: str
    """Index field."""

    field_type: str | None = None
    """Field type."""

    type: Literal["hash"] = "hash"
    """Index type."""


class AscIndex(BaseIndex):
    """Ascending index."""

    field: str
    """Index field."""

    field_type: str | None = None
    """Field type."""

    type: Literal["asc"] = "asc"
    """Index type."""


class DescIndex(BaseIndex):
    """Descending index."""

    field: str
    """Index field."""

    field_type: str | None = None
    """Field type."""

    type: Literal["desc"] = "desc"
    """Index type."""


class ArrayIndex(BaseIndex):
    """Array index."""

    field: str
    """Index field."""

    field_type: str | None = None
    """Field type."""

    type: Literal["array"] = "array"
    """Index type."""


class TTLIndex(BaseIndex):
    """TTL index."""

    field: str
    """Index field."""

    type: Literal["ttl"] = "ttl"
    """Index type."""


class GeospatialIndex(BaseIndex):
    """Geospatial index."""

    field: str
    """Index field."""

    field_type: str | None = None
    """Field type."""

    type: Literal["geospatial"] = "geospatial"
    """Index type."""


class TextIndex(BaseIndex):
    """Text index."""

    field: str
    """Index field."""

    type: Literal["text"] = "text"
    """Index type."""


class VectorIndexMetric(str, Enum):
    """Vector index metric."""

    DOTPRODUCT = "dotproduct"
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"
    HAMMING = "hamming"


class VectorIndexStructure(str, Enum):
    """Vector index structure."""

    FLAT = "flat"
    HNSW = "hnsw"
    QUANTIZED_FLAT = "quantized_flat"
    DISKANN = "diskann"


class VectorIndex(BaseIndex):
    """Vector index."""

    field: str | None = None
    """Index field name."""

    dimension: int = 4
    """Vector dimension."""

    metric: VectorIndexMetric = VectorIndexMetric.DOTPRODUCT
    """Index metric."""

    structure: VectorIndexStructure | None = None
    """Vector index structure."""

    nconfig: dict | None = None
    """Native config."""

    type: Literal["vector"] = "vector"
    """Index type."""


class SparseVectorIndex(DataModel):
    """Sparse vector index."""

    field: str | None = None
    """Sparse vector field name."""

    nconfig: dict | None = None
    """Native config."""

    type: Literal["sparse_vector"] = "sparse_vector"
    """Index type."""


class CompositeIndex(BaseIndex):
    """Composite index."""

    fields: list[
        AscIndex
        | DescIndex
        | ArrayIndex
        | GeospatialIndex
        | TextIndex
        | VectorIndex
        | SparseVectorIndex
    ]
    """Composite index fields."""

    type: Literal["composite"] = "composite"
    """Index type."""


class IndexType:
    FIELD = "field"
    COMPOSITE = "composite"
    ASC = "asc"
    DESC = "desc"
    ARRAY = "array"
    EXCLUDE = "exclude"
    TTL = "ttl"
    GEOSPATIAL = "geospatial"
    TEXT = "text"
    VECTOR = "vector"
    SPARSE_VECTOR = "sparse_vector"
    RANGE = "range"
    HASH = "hash"
    WILDCARD = "wildcard"


Index = Union[
    FieldIndex,
    CompositeIndex,
    AscIndex,
    DescIndex,
    ArrayIndex,
    TTLIndex,
    GeospatialIndex,
    TextIndex,
    VectorIndex,
    SparseVectorIndex,
    RangeIndex,
    HashIndex,
    ExcludeIndex,
    WildcardIndex,
    BaseIndex,
]
