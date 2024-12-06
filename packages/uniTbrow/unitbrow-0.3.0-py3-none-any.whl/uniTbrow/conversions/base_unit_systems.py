import uniTbrow.units as u
import uniTbrow.dimensions as d


def get_dimensions(expr):
    for symbol in expr.free_symbols:
        try:
            unit = u.lookup_unit(symbol)
            expr = expr.subs(symbol, unit.dimension.dimension)
        except KeyError:
            continue
    return expr


class BaseUnitSystem:
    def __init__(self, dimension_unit_map):
        self.dimension_unit_map: dict[d.Dimension, u.Unit] = dimension_unit_map

    def convert(self, expr):
        expr = u.to_base_units(expr)
        for symbol in expr.free_symbols:
            try:
                unit = u.lookup_unit(symbol)
                to_unit = self.dimension_unit_map[unit.dimension]
                conversion_factor = 1
                for sym in to_unit.base.free_symbols:
                    conversion_factor = to_unit.base.subs(sym, 1)
                expr = expr.subs(symbol, (1/conversion_factor)*to_unit)
            except KeyError:
                continue
        return expr


si = BaseUnitSystem({
    d.mass: u.kg,
})

cgs = BaseUnitSystem({
    d.length: u.cm,
})
