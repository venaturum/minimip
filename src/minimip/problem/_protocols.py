from __future__ import annotations

from typing import Protocol


class Problem(Protocol):
    @property
    def constraints(self):
        ...

    @property
    def variables(self):
        ...

    def make_variable(self):
        ...

    def make_constraint(self):
        ...

    def add_variable_to_constraint(self, variable: Variable, constraint: Constraint):
        ...


class Constraint(Protocol):
    @property
    def problem(self) -> Problem:
        ...

    def add_variable(self, variable: Variable):
        ...


class Variable(Protocol):
    @property
    def problem(self) -> Problem:
        ...

    def add_to_constraint(self, constraint: Constraint):
        ...
