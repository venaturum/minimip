from minimip._constants import ConstraintSense
from minimip._typing import Problem, Variable
from minimip._typing.types import PythonScalar


class Constraint:
    def __init__(self, problem: Problem, sense: ConstraintSense, RHS: PythonScalar):
        self._problem = problem
        self._sense = sense
        self._RHS = RHS

    @property
    def problem(self) -> Problem:
        return self._problem

    def add_variable(self, variable: Variable, coefficient: PythonScalar):
        self.problem.add_variable_to_constraint(variable, self, coefficient)
