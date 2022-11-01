from minimip._constants import ConstraintSense
from minimip._typing import Constraint as ConstraintType
from minimip._typing import Linker, List, PythonScalar
from minimip._typing import Variable as VariableType
from minimip.problem.constraint import Constraint
from minimip.problem.linker import SimpleLinker
from minimip.problem.variable import Variable


class Problem:
    def __init__(self, name: str = "", linker: Linker = SimpleLinker()):
        self.name: str = name
        self._linker: Linker = linker
        self._constraints: List[ConstraintType] = []
        self._variables: List[VariableType] = []

    @property
    def constraints(self):
        return self._constraints

    @property
    def variables(self):
        return self._variables

    def make_variable(self):
        result = Variable(self)
        self._variables.append(result)
        return result

    def make_constraint(self, sense: ConstraintSense, RHS: PythonScalar):
        result = Constraint(self, sense, RHS)
        self._constraints.append(result)
        return result

    def add_variable_to_constraint(
        self,
        variable: VariableType,
        constraint: ConstraintType,
        coefficient: PythonScalar,
    ):
        self._linker.add_variable_to_constraint(variable, constraint, coefficient)

    def make_matrix(self):
        return self._linker.make_matrix(self.variables, self.constraints)
