from __future__ import annotations

from typing import Collection, Iterable, Protocol

import numpy as np

from minimip._constants import ConstraintSense
from minimip._typing.types import PythonScalar


class Problem(Protocol):
    @property
    def constraints(self):
        ...

    @property
    def variables(self):
        ...

    def make_variable(self):
        ...

    def make_constraint(self, sense: ConstraintSense, RHS: PythonScalar):
        ...

    def add_variable_to_constraint(
        self, variable: Variable, constraint: Constraint, coefficient: PythonScalar
    ):
        ...


class Constraint(Protocol):
    def __init__(self, problem: Problem, sense: ConstraintSense, RHS: PythonScalar):
        ...

    @property
    def problem(self) -> Problem:
        ...

    def add_variable(self, variable: Variable, coefficient: PythonScalar):
        ...


class Variable(Protocol):
    @property
    def problem(self) -> Problem:
        ...

    def add_to_constraint(self, constraint: Constraint, coefficient: PythonScalar):
        ...


class Linker(Protocol):
    def add_variable_to_constraint(
        self, variable: Variable, constraint: Constraint, coefficient: PythonScalar
    ):
        ...

    def make_matrix(self, variables: Collection, constraints: Collection) -> np.ndarray:
        ...
