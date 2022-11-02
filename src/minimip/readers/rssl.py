"""Rigid Super Simple Language"""

import re

from minimip._constants import ConstraintSense
from minimip._typing import Dict
from minimip._typing import Problem as ProblemType
from minimip._typing import PythonScalar, Variable
from minimip.problem.problem import Problem

CONST = "CONST"


def _get_LHS_RHS_sense(string: str):
    relation, *_ = re.findall(">=|<=|=", string)
    if _:
        raise RuntimeError("more than one sense found")
    LHS_expr, RHS_expr = string.split(relation)
    sense = ConstraintSense[{">=": "GT", "<=": "LT", "=": "EQ"}[relation]]
    if sense == ConstraintSense.GT:
        LHS_expr, RHS_expr = RHS_expr, LHS_expr
    return LHS_expr, RHS_expr, sense


def _map_symbol_to_coeff(sign, unsigned_coeff, symbol):
    unsigned_coeff = "1" if not unsigned_coeff else unsigned_coeff
    signed_coeff = float("".join([sign, unsigned_coeff]))
    symbol = CONST if not symbol else symbol
    return (symbol, signed_coeff)


def _make_symbol_dict_from_expression(expr):
    regex = "([\+|-]?)((?:\d+(?:\.\d+)?)?)([a-z0-9_]*)"
    expr = expr.replace(" ", "")
    return dict(
        [_map_symbol_to_coeff(*t) for t in re.findall(regex, expr) if t != ("", "", "")]
    )


def _make_symbol_dict(LHS_expr, RHS_expr):
    LHS_dict = _make_symbol_dict_from_expression(LHS_expr)
    RHS_dict = _make_symbol_dict_from_expression(RHS_expr)

    for (symbol, coeff) in RHS_dict.items():
        LHS_dict[symbol] = LHS_dict.get(symbol, 0) - coeff
    return LHS_dict


class RsslReader:
    def __init__(self):
        self._problem: ProblemType = Problem()
        self._name_to_variable_map: Dict = {}

    @property
    def problem(self) -> ProblemType:
        return self._problem

    def _get_var_from_name(self, name) -> Variable:
        if name not in self._name_to_variable_map:
            self._name_to_variable_map[name] = self.problem.make_variable(name)
        return self._name_to_variable_map[name]

    def handle_objective(self, string: str):
        sense, expr = string[:3], string[3:]
        assert sense in ("MAX", "MIN")
        symbol_map = _make_symbol_dict_from_expression(expr)
        if sense == "MIN":
            symbol_map = {k: -v for k, v in symbol_map.items()}
        if CONST in symbol_map:
            self.problem.set_objective_constant(symbol_map.pop(CONST))
        for symbol, coefficient in symbol_map.items():
            variable = self._get_var_from_name(symbol)
        self.problem.add_variable_to_objective(variable, coefficient)

    def handle_constraint(self, string: str):
        LHS_expr, RHS_expr, sense = _get_LHS_RHS_sense(string)
        symbol_map = _make_symbol_dict(LHS_expr, RHS_expr)
        if CONST in symbol_map:
            RHS = -symbol_map.pop(CONST)
        constraint = self.problem.make_constraint(sense, RHS)
        for symbol, coefficient in symbol_map.items():
            variable = self._get_var_from_name(symbol)
            constraint.add_variable(variable, coefficient)


def make_problem(string: str) -> ProblemType:
    obj, *constraints = string.strip("\n").split("\n")
    reader = RsslReader()
    reader.handle_objective(obj)
    for constraint in constraints:
        reader.handle_constraint(constraint)
    return reader.problem
