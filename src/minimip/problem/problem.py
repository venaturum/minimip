from dataclasses import dataclass

import numpy as np

from minimip._constants import ConstraintSense, ObjectiveSense
from minimip._typing import Constraint as ConstraintType
from minimip._typing import Iterable, Linker, List, NDArray, PythonScalar, Union
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
        self._sense: ObjectiveSense = ObjectiveSense.MIN
        self._obj_constant: PythonScalar = 0

    def set_sense(self, sense: Union[str, ObjectiveSense]):
        if isinstance(sense, str):
            sense = ObjectiveSense[sense.upper()]
        self._sense = sense

    @property
    def sense(self):
        return self._sense

    @property
    def constraints(self) -> Iterable[ConstraintType]:
        return self._constraints

    @property
    def variables(self) -> Iterable[VariableType]:
        return self._variables

    def make_variable(self, name: str) -> VariableType:
        result = Variable(self, name)
        self._variables.append(result)
        return result

    def make_constraint(
        self,
        sense: ConstraintSense,
        RHS: PythonScalar,
        name: str = "",
    ) -> ConstraintType:
        result = Constraint(self, sense, RHS, name)
        self._constraints.append(result)
        return result

    def set_objective_constant(self, constant: PythonScalar):
        self._obj_constant = constant

    def add_variable_to_constraint(
        self,
        variable: VariableType,
        constraint: ConstraintType,
        coefficient: PythonScalar,
    ):
        self._linker.add_variable_to_constraint(variable, constraint, coefficient)

    def add_variable_to_objective(
        self,
        variable: VariableType,
        coefficient: PythonScalar,
    ):
        self._linker.add_variable_to_objective(variable, coefficient)

    # def make_coefficient_matrix(self):
    #     return self._linker.make_matrix(self.variables, self.constraints)

    def _to_matrix_problem(self):
        return MatrixProblem(
            sense=self.sense,
            c=self._linker.make_objective_vector(self.variables),
            A=self._linker.make_coefficient_matrix(self.variables, self.constraints),
            relation=np.array([c.sense.value for c in self.constraints]),
            b=np.array([c.RHS for c in self.constraints]),
        )


@dataclass
class MatrixProblem:
    """
    Representing a problem in the form
    max/min  c^Tx
    s.t.   Ax <= b
    """

    sense: ObjectiveSense
    c: NDArray[np.float_]
    A: NDArray[np.float_]
    relation: NDArray[np.int_]
    b: NDArray[np.float_]
