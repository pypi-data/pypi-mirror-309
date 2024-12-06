from enum import Enum
from typing import Any

from verse.core import DataModel


class VectorSearchArgs(DataModel):
    """Vector search args."""

    vector: list[float] | None = None
    """Vector floats."""

    sparse_vector: dict[int, float] | None = None
    """Sparse vector dictionary."""

    field: str | None = None
    """Vector field name."""


class VectorValue(DataModel):
    """Vector value."""

    vector: list[float] | None = None
    """Vector floats."""

    sparse_vector: dict[int, float] | None = None
    """Sparse vector dictionary."""

    content: str | None = None
    """Text context."""


class VectorKey(DataModel):
    """Vector key."""

    id: str
    """Vector id."""


class VectorProperties(DataModel):
    """Vector properties."""

    score: float | None = None
    """Match score."""


class VectorItem(DataModel):
    """Vector item."""

    key: VectorKey
    """Vector key."""

    value: VectorValue | None = None
    """Vector value."""

    metadata: dict[str, Any] | None = None
    """Vector metadata."""

    properties: VectorProperties | None = None
    """Vector properties."""


class VectorList(DataModel):
    """Vector list."""

    items: list[VectorItem]
    """List of vector items."""


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


class VectorIndex(DataModel):
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


class SparseVectorIndex(DataModel):
    """Sparse vector index."""

    field: str | None = None
    """Sparse vector field name."""

    nconfig: dict | None = None
    """Native config."""


class VectorCollectionConfig(DataModel):
    """Vector collection config."""

    vector_index: VectorIndex | None = None
    """Vector index."""

    sparse_vector_index: SparseVectorIndex | None = None
    """Sparse vector index."""

    nconfig: dict[str, Any] | None = None
    """Native config."""
