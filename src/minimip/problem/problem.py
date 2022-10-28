from minimip._typing import Constraint as ConstraintType
from minimip._typing import List
from minimip._typing import Variable as VariableType
from minimip.problem.constraint import Constraint
from minimip.problem.variable import Variable


class Problem:
    def __init__(self, name: str):
        self.name = name
        self._constraints: List[ConstraintType] = []
        self._variables: List[VariableType] = []

    @property
    def constraints(self):
        return self._constraints

    @property
    def variables(self):
        return self._variables

    def make_variable(self):
        return Variable(self, self.problem)

    def make_constraint(self):
        return Constraint(self, self.problem)

    def add_variable_to_constraint(self, variable: Variable, constraint: Constraint):
        ...
