from sympy import Equality
from uniTbrow.units import to_base_units
from .base_unit_systems import si, cgs


def to_si_units(expr):
    return si.convert(expr)


def to_cgs_units(expr):
    return cgs.convert(expr)


def convert(expr, new_units):
    if isinstance(expr, Equality):
        return Equality(convert(expr.lhs, new_units), convert(expr.rhs, new_units))
    return to_base_units(expr/new_units) * new_units
