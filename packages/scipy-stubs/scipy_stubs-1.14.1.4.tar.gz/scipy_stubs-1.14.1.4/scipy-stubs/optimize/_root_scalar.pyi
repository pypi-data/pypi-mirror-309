from scipy._typing import Untyped

__all__ = ["root_scalar"]

ROOT_SCALAR_METHODS: Untyped

class MemoizeDer:
    fun: Untyped
    vals: Untyped
    x: Untyped
    n_calls: int
    def __init__(self, fun: Untyped) -> None: ...
    def __call__(self, x: Untyped, *args: Untyped) -> Untyped: ...
    def fprime(self, x: Untyped, *args: Untyped) -> Untyped: ...
    def fprime2(self, x: Untyped, *args: Untyped) -> Untyped: ...
    def ncalls(self) -> Untyped: ...

def root_scalar(
    f: Untyped,
    args: Untyped = (),
    method: Untyped | None = None,
    bracket: Untyped | None = None,
    fprime: Untyped | None = None,
    fprime2: Untyped | None = None,
    x0: Untyped | None = None,
    x1: Untyped | None = None,
    xtol: Untyped | None = None,
    rtol: Untyped | None = None,
    maxiter: Untyped | None = None,
    options: Untyped | None = None,
) -> Untyped: ...
