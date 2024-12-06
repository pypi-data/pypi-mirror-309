from typing import Any, final

import numpy as np
import numpy.typing as npt
import optype.numpy as onp
from scipy._typing import Untyped
from scipy.sparse import csc_matrix

@final
class SuperLU:
    L: csc_matrix
    U: csc_matrix
    nnz: int
    perm_r: onp.Array1D[np.intp]
    perm_c: onp.Array1D[np.intp]
    shape: tuple[int, ...]

    def solve(self, /, rhs: npt.NDArray[np.number[Any]]) -> npt.NDArray[np.number[Any]]: ...

def gssv(*args: Untyped, **kwargs: Untyped) -> Untyped: ...
def gstrf(*args: Untyped, **kwargs: Untyped) -> Untyped: ...
def gstrs(*args: Untyped, **kwargs: Untyped) -> Untyped: ...
