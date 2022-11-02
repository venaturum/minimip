from minimip._typing import Constraint, Problem, PythonScalar


class Variable:
    def __init__(self, problem: Problem, name: str):
        self._problem = problem
        self._name = name

    @property
    def problem(self) -> Problem:
        return self._problem

    def add_to_constraint(self, constraint: Constraint, coefficient: PythonScalar):
        self.problem.add_variable_to_constraint(self, constraint, coefficient)
