from collections.abc import Callable, Sequence
from typing import Any, Concatenate, Final, Generic, Literal, TypeAlias, overload, type_check_only
from typing_extensions import TypedDict, TypeVar, Unpack

import numpy as np
import numpy.typing as npt
import optype as op
import optype.numpy as onp
from numpy._typing import _ArrayLikeFloat_co, _ArrayLikeNumber_co
from scipy._lib._util import _RichResult
from scipy.sparse import sparray, spmatrix
from .base import DenseOutput, OdeSolver
from .common import OdeSolution

_SCT_cf = TypeVar("_SCT_cf", bound=np.inexact[Any], default=np.float64 | np.complex128)

_FuncSol: TypeAlias = Callable[[float], npt.NDArray[_SCT_cf]]
_FuncEvent: TypeAlias = Callable[[float, npt.NDArray[_SCT_cf]], float]
_Events: TypeAlias = Sequence[_FuncEvent[_SCT_cf]]

_VectorIntP: TypeAlias = onp.Array1D[np.intp]
_VectorFloat: TypeAlias = onp.Array1D[np.float64]

_IVPMethod: TypeAlias = Literal["RK23", "RK45", "DOP853", "Radau", "BDF", "LSODA"]

@type_check_only
class _SolverOptions(TypedDict, Generic[_SCT_cf], total=False):
    first_step: onp.ToFloat | None
    max_step: onp.ToFloat
    rtol: _ArrayLikeFloat_co
    atol: _ArrayLikeFloat_co
    jac: (
        _ArrayLikeNumber_co
        | spmatrix
        | sparray
        | Callable[[float, npt.NDArray[np.float64]], _ArrayLikeNumber_co | spmatrix | sparray]
        | None
    )
    jac_sparsity: _ArrayLikeFloat_co | spmatrix | sparray | None
    lband: onp.ToInt | None
    uband: onp.ToInt | None
    min_step: onp.ToFloat

###

METHODS: Final[dict[str, type]] = ...
MESSAGES: Final[dict[int, str]] = ...

class OdeResult(
    _RichResult[int | str | npt.NDArray[np.float64 | _SCT_cf] | list[npt.NDArray[np.float64 | _SCT_cf]] | OdeSolution | None],
    Generic[_SCT_cf],
):
    t: _VectorFloat
    y: onp.Array2D[_SCT_cf]
    sol: OdeSolution | None
    t_events: list[_VectorFloat] | None
    y_events: list[npt.NDArray[_SCT_cf]] | None
    nfev: int
    njev: int
    nlu: int
    status: Literal[-1, 0, 1]
    message: str
    success: bool

def prepare_events(events: _FuncEvent[_SCT_cf] | _Events[_SCT_cf]) -> tuple[_Events[_SCT_cf], _VectorFloat, _VectorFloat]: ...
def solve_event_equation(event: _FuncEvent[_SCT_cf], sol: _FuncSol[_SCT_cf], t_old: float, t: float) -> float: ...
def handle_events(
    sol: DenseOutput,
    events: Sequence[_FuncEvent[_SCT_cf]],
    active_events: npt.NDArray[np.intp],
    event_count: npt.NDArray[np.intp | np.float64],
    max_events: npt.NDArray[np.intp | np.float64],
    t_old: float,
    t: float,
) -> tuple[_VectorIntP, _VectorFloat, bool]: ...
def find_active_events(g: _ArrayLikeFloat_co, g_new: _ArrayLikeFloat_co, direction: npt.NDArray[np.float64]) -> _VectorIntP: ...

#
@overload
def solve_ivp(
    fun: Callable[Concatenate[float, onp.Array1D[_SCT_cf], ...], npt.NDArray[_SCT_cf]],
    t_span: Sequence[op.CanFloat],
    y0: _ArrayLikeNumber_co,
    method: _IVPMethod | type[OdeSolver] = "RK45",
    t_eval: _ArrayLikeFloat_co | None = None,
    dense_output: bool = False,
    events: _Events[_SCT_cf] | None = None,
    vectorized: Literal[False, 0] = False,
    args: tuple[object, ...] | None = None,
    **options: Unpack[_SolverOptions],
) -> OdeResult[_SCT_cf]: ...
@overload
def solve_ivp(
    fun: Callable[Concatenate[_VectorFloat, onp.Array2D[_SCT_cf], ...], npt.NDArray[_SCT_cf]],
    t_span: Sequence[op.CanFloat],
    y0: _ArrayLikeNumber_co,
    method: _IVPMethod | type[OdeSolver] = "RK45",
    t_eval: _ArrayLikeFloat_co | None = None,
    dense_output: bool = False,
    events: _Events[_SCT_cf] | None = None,
    *,
    vectorized: Literal[True, 1],
    args: tuple[object, ...] | None = None,
    **options: Unpack[_SolverOptions],
) -> OdeResult[_SCT_cf]: ...
