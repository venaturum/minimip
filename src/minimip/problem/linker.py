import numpy as np

from minimip._typing import Collection
from minimip._typing import Constraint as ConstraintType
from minimip._typing import Iterable, List, PythonScalar
from minimip._typing import Variable as VariableType


class SimpleLinker:
    def __init__(self):
        self._links: List = []
        self._variables: List = []
        self._constraints: List = []
        self._coefficients: List = []

    def add_variable_to_constraint(
        self,
        variable: VariableType,
        constraint: ConstraintType,
        coefficient: PythonScalar,
    ):
        # self._links.append((variable, constraint, coefficient))
        self._variables.append(variable)
        self._constraints.append(constraint)
        self._coefficients.append(coefficient)

    def make_matrix(self, variables: Collection, constraints: Collection) -> np.ndarray:
        var_map = {v: k for k, v in enumerate(variables)}
        con_map = {v: k for k, v in enumerate(constraints)}
        var_coords = tuple(map(var_map.get, self._variables))
        cons_coords = tuple(map(con_map.get, self._constraints))
        A = np.zeros((len(constraints), len(variables)))
        A[cons_coords, var_coords] = self._coefficients
        return A