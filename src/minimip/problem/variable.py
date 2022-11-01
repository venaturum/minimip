from minimip._typing import Constraint, Problem
from minimip._typing.types import PythonScalar


class Variable:
    def __init__(self, problem: Problem):
        self._problem = problem

    @property
    def problem(self) -> Problem:
        return self._problem

    def add_to_constraint(self, constraint: Constraint, coefficient: PythonScalar):
        self.problem.add_variable_to_constraint(self, constraint, coefficient)
