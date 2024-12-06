from cellestial.single.core.dimensional import dimensional, expression
from cellestial.single.core.grids import dimensionals, expressions, pcas, tsnes, umaps
from cellestial.single.core.subdimensional import pca, tsne, umap

# alias
dim = dimensional


__all__ = [
    "dimensionals",
    "dim",
    "umap",
    "umaps",
    "pca",
    "pcas",
    "tsne",
    "tsnes",
    "expression",
    "expressions",
]