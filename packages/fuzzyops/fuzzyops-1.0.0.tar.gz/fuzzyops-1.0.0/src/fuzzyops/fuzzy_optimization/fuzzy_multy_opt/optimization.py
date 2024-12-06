from typing import Tuple

import cvxpy as cp
import numpy as np

from cvxpy.atoms.affine.binary_operators import MulExpression
from cvxpy.atoms.elementwise.minimum import minimum


# Функция принадлежности нечеткому множеству
def _mu(f: MulExpression, g_val: np.int64, t_val: np.int64) -> minimum:
    return cp.minimum(1, 1 - cp.abs(f - g_val) / t_val)


def solve_problem(A: np.ndarray, b: np.ndarray,
                  C: np.ndarray, g: np.ndarray,
                  t: np.ndarray) -> Tuple[float, np.ndarray]:
    num_vars, num_crits, num_cons = A.shape[1], C.shape[0], b.shape[0]

    # Создание переменной для оптимизации
    x = cp.Variable(num_vars)
    # Вспомогательные переменные для моделирования абсолютной величины
    delta = cp.Variable((num_crits, 1))

    mus = [_mu(C[i] @ x, g[i], t[i]) for i in range(num_crits)]
    mus_stacked = cp.vstack(mus)
    objective = cp.Maximize(cp.min(mus_stacked))

    # Добавление ограничений
    constraints = [
        A @ x <= b,
        C @ x >= g - t @ delta,
        C @ x <= g + t @ delta,
        delta >= 0
    ]

    # Формулировка и решение задачи
    prob = cp.Problem(objective, constraints)
    result = prob.solve()

    return result, x.value
