from typing import Callable, Literal
import numpy as np
import numpy.typing as npt


def _df(f: Callable, x: np.floating, h=1e-6) -> np.floating:
    return (f(x + h) - f(x - h)) / (2 * h)


def _d2f(f, x, h=1e-5) -> np.floating:
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h**2)

def _newton_method(f: Callable, a: float, b: float, tol: float=1e-5,
                  max_iter: int=100,
                  mode: Literal['max', "min"]='min') -> np.floating | float:
    x = (a + b) / 2
    history = [x]

    if mode == "max":
        g = lambda x: -f(x)  # noqa: E731
    else:
        g = f

    for _ in range(max_iter):
        f1_ = _df(g, x)
        f2_ = _d2f(g, x)

        if abs(f2_) < 1e-12:
            break

        x_new = x - f1_ / f2_
        history.append(x_new)

        if abs(x_new - x) < tol:
            return x_new

        x = x_new

    return x

def _golden_section_search(f, a, b, tol=1e-5, max_iter=100):
    """Поиск минимума функции одной переменной на [a, b]."""
    gr = (np.sqrt(5) - 1) / 2  # золотое сечение

    c = b - gr * (b - a)
    d = a + gr * (b - a)

    for _ in range(max_iter):
        if abs(b - a) < tol:
            break

        if f(c) < f(d):
            b = d
        else:
            a = c

        c = b - gr * (b - a)
        d = a + gr * (b - a)

    return (a + b) / 2


def coordinate_descent(
    f: Callable,
    starting_approx: npt.NDArray,
    bounds: list[tuple[int, int]],
    tol: float=1e-5,
    max_iter: int=10000,
    mode: Literal['max', "min"]='min',
) -> npt.NDArray:
    """
    Циклический покоординатный спуск.

    f       — функция f(x), где x — numpy-вектор
    x0      — начальная точка
    bounds  — [(a1,b1), ..., (an,bn)] границы поиска
    """
    x = starting_approx.astype(float).copy()
    n = len(x)

    for _ in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            a, b = bounds[i]

            def f1d(val):
                x_temp = x.copy()
                x_temp[i] = val
                return f(x_temp)

            x[i] = _newton_method(f1d, a, b, tol, mode=mode)

        if np.linalg.norm(x - x_old) < tol:
            break

    return x




if __name__ == "__main__":
    def func(v):
        x, y = v
        return (x - 2)**2 + (y + 1)**2

    start = np.array([0, 0])
    bounds = [(-10, 10), (-10, 10)]

    minimum = coordinate_descent(func, start, bounds)
    print("Найденный минимум:", minimum)
