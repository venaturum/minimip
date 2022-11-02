from __future__ import annotations

from typing import Collection, Iterable, Protocol

import numpy as np

from minimip._constants import ConstraintSense
from minimip._typing.types import PythonScalar


class Problem(Protocol):
    @property
    def constraints(self) -> Iterable[Constraint]:
        ...

    @property
    def variables(self) -> Iterable[Variable]:
        ...

    def make_variable(self, name: str) -> Variable:
        ...

    def make_constraint(
        self, sense: ConstraintSense, RHS: PythonScalar, name: str = ""
    ) -> Constraint:
        ...

    def add_variable_to_constraint(
        self, variable: Variable, constraint: Constraint, coefficient: PythonScalar
    ):
        ...

    def add_variable_to_objective(self, variable: Variable, coefficient: PythonScalar):
        ...

    def set_objective_constant(self, constant: PythonScalar):
        ...


class Constraint(Protocol):
    def __init__(
        self, problem: Problem, sense: ConstraintSense, RHS: PythonScalar, name: str
    ):
        ...

    @property
    def problem(self) -> Problem:
        ...

    def add_variable(self, variable: Variable, coefficient: PythonScalar):
        ...


class Variable(Protocol):
    def __init__(self, problem: Problem, name: str):
        ...

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

    def add_variable_to_objective(self, variable: Variable, coefficient: PythonScalar):
        ...
