from typing import TypeAlias

import numpy as np
import numpy.typing as npt
import optype as op
import optype.numpy as onp
from numpy._typing import _ArrayLikeInt, _ArrayLikeNumber_co
from scipy._typing import AnyShape, DCTType, NormalizationMode

__all__ = ["dct", "dctn", "dst", "dstn", "idct", "idctn", "idst", "idstn"]

# this doesn't include `numpy.float16`
_ArrayReal: TypeAlias = npt.NDArray[np.float32 | np.float64 | np.longdouble]

###

# TODO: Add overloads for specific return dtypes, as discussed in:
# https://github.com/jorenham/scipy-stubs/pull/118#discussion_r1807957439

def dctn(
    x: _ArrayLikeNumber_co,
    type: DCTType = 2,
    s: _ArrayLikeInt | None = None,
    axes: AnyShape | None = None,
    norm: NormalizationMode | None = None,
    overwrite_x: op.CanBool = False,
    workers: onp.ToInt | None = None,
    *,
    orthogonalize: op.CanBool | None = None,
) -> _ArrayReal: ...
def idctn(
    x: _ArrayLikeNumber_co,
    type: DCTType = 2,
    s: _ArrayLikeInt | None = None,
    axes: AnyShape | None = None,
    norm: NormalizationMode | None = None,
    overwrite_x: op.CanBool = False,
    workers: onp.ToInt | None = None,
    orthogonalize: op.CanBool | None = None,
) -> _ArrayReal: ...
def dstn(
    x: _ArrayLikeNumber_co,
    type: DCTType = 2,
    s: _ArrayLikeInt | None = None,
    axes: AnyShape | None = None,
    norm: NormalizationMode | None = None,
    overwrite_x: op.CanBool = False,
    workers: onp.ToInt | None = None,
    orthogonalize: op.CanBool | None = None,
) -> _ArrayReal: ...
def idstn(
    x: _ArrayLikeNumber_co,
    type: DCTType = 2,
    s: _ArrayLikeInt | None = None,
    axes: AnyShape | None = None,
    norm: NormalizationMode | None = None,
    overwrite_x: op.CanBool = False,
    workers: onp.ToInt | None = None,
    orthogonalize: op.CanBool | None = None,
) -> _ArrayReal: ...
def dct(
    x: _ArrayLikeNumber_co,
    type: DCTType = 2,
    n: onp.ToInt | None = None,
    axis: op.CanIndex = -1,
    norm: NormalizationMode | None = None,
    overwrite_x: op.CanBool = False,
    workers: onp.ToInt | None = None,
    orthogonalize: op.CanBool | None = None,
) -> _ArrayReal: ...
def idct(
    x: _ArrayLikeNumber_co,
    type: DCTType = 2,
    n: onp.ToInt | None = None,
    axis: op.CanIndex = -1,
    norm: NormalizationMode | None = None,
    overwrite_x: op.CanBool = False,
    workers: onp.ToInt | None = None,
    orthogonalize: op.CanBool | None = None,
) -> _ArrayReal: ...
def dst(
    x: _ArrayLikeNumber_co,
    type: DCTType = 2,
    n: onp.ToInt | None = None,
    axis: op.CanIndex = -1,
    norm: NormalizationMode | None = None,
    overwrite_x: op.CanBool = False,
    workers: onp.ToInt | None = None,
    orthogonalize: op.CanBool | None = None,
) -> _ArrayReal: ...
def idst(
    x: _ArrayLikeNumber_co,
    type: DCTType = 2,
    n: onp.ToInt | None = None,
    axis: op.CanIndex = -1,
    norm: NormalizationMode | None = None,
    overwrite_x: op.CanBool = False,
    workers: onp.ToInt | None = None,
    orthogonalize: op.CanBool | None = None,
) -> _ArrayReal: ...
