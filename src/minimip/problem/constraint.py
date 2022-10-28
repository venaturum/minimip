from minimip._typing import Problem, Variable


class Constraint:
    def __init__(self, problem: Problem):
        self._problem = problem

    @property
    def problem(self) -> Problem:
        return self._problem

    def add_variable(self, variable: Variable):
        self.problem.add_variable_to_constraint(variable, self)
