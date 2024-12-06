from typing import TypeAlias, overload

import numpy as np
import optype.numpy as onp
from numpy._typing import _ArrayLikeFloat_co, _ArrayLikeNumber_co

__all__ = ["cc_diff", "cs_diff", "diff", "hilbert", "ihilbert", "itilbert", "sc_diff", "shift", "ss_diff", "tilbert"]

# the suffix correspond to the relevant dtype charcode(s)
_Vec_d: TypeAlias = onp.Array1D[np.float64]
_Vec_dD: TypeAlias = onp.Array1D[np.float64 | np.complex128]

_Cache: TypeAlias = dict[tuple[onp.ToFloat, ...], _Vec_d]  # {n: kernel}

###

#
@overload
def diff(x: _ArrayLikeFloat_co, order: int = 1, period: onp.ToFloat | None = None, _cache: _Cache = ...) -> _Vec_d: ...
@overload
def diff(x: _ArrayLikeNumber_co, order: int = 1, period: onp.ToFloat | None = None, _cache: _Cache = ...) -> _Vec_dD: ...

#
@overload
def tilbert(x: _ArrayLikeFloat_co, h: onp.ToFloat, period: onp.ToFloat | None = None, _cache: _Cache = ...) -> _Vec_d: ...
@overload
def tilbert(x: _ArrayLikeNumber_co, h: onp.ToFloat, period: onp.ToFloat | None = None, _cache: _Cache = ...) -> _Vec_dD: ...

#
@overload
def itilbert(x: _ArrayLikeFloat_co, h: onp.ToFloat, period: onp.ToFloat | None = None, _cache: _Cache = ...) -> _Vec_d: ...
@overload
def itilbert(x: _ArrayLikeNumber_co, h: onp.ToFloat, period: onp.ToFloat | None = None, _cache: _Cache = ...) -> _Vec_dD: ...

#
@overload
def hilbert(x: _ArrayLikeFloat_co, _cache: _Cache = ...) -> _Vec_d: ...
@overload
def hilbert(x: _ArrayLikeNumber_co, _cache: _Cache = ...) -> _Vec_dD: ...

#
@overload
def ihilbert(x: _ArrayLikeFloat_co) -> _Vec_d: ...
@overload
def ihilbert(x: _ArrayLikeNumber_co) -> _Vec_dD: ...

#
@overload
def cs_diff(
    x: _ArrayLikeFloat_co,
    a: onp.ToFloat,
    b: onp.ToFloat,
    period: onp.ToFloat | None = None,
    _cache: _Cache = ...,
) -> _Vec_d: ...
@overload
def cs_diff(
    x: _ArrayLikeNumber_co,
    a: onp.ToFloat,
    b: onp.ToFloat,
    period: onp.ToFloat | None = None,
    _cache: _Cache = ...,
) -> _Vec_dD: ...

#
@overload
def sc_diff(
    x: _ArrayLikeFloat_co,
    a: onp.ToFloat,
    b: onp.ToFloat,
    period: onp.ToFloat | None = None,
    _cache: _Cache = ...,
) -> _Vec_d: ...
@overload
def sc_diff(
    x: _ArrayLikeNumber_co,
    a: onp.ToFloat,
    b: onp.ToFloat,
    period: onp.ToFloat | None = None,
    _cache: _Cache = ...,
) -> _Vec_dD: ...

#
@overload
def ss_diff(
    x: _ArrayLikeFloat_co,
    a: onp.ToFloat,
    b: onp.ToFloat,
    period: onp.ToFloat | None = None,
    _cache: _Cache = ...,
) -> _Vec_d: ...
@overload
def ss_diff(
    x: _ArrayLikeNumber_co,
    a: onp.ToFloat,
    b: onp.ToFloat,
    period: onp.ToFloat | None = None,
    _cache: _Cache = ...,
) -> _Vec_dD: ...

#
@overload
def cc_diff(
    x: _ArrayLikeFloat_co,
    a: onp.ToFloat,
    b: onp.ToFloat,
    period: onp.ToFloat | None = None,
    _cache: _Cache = ...,
) -> _Vec_d: ...
@overload
def cc_diff(
    x: _ArrayLikeNumber_co,
    a: onp.ToFloat,
    b: onp.ToFloat,
    period: onp.ToFloat | None = None,
    _cache: _Cache = ...,
) -> _Vec_dD: ...

#
@overload
def shift(x: _ArrayLikeFloat_co, a: onp.ToFloat, period: onp.ToFloat | None = None, _cache: _Cache = ...) -> _Vec_d: ...
@overload
def shift(x: _ArrayLikeNumber_co, a: onp.ToFloat, period: onp.ToFloat | None = None, _cache: _Cache = ...) -> _Vec_dD: ...
