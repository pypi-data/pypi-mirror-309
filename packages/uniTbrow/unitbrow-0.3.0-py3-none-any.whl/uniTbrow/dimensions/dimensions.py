from sympy import symbols as _symbols, Mul, Pow
import numbers

_dimension_space = dict()
_dimension_namespace = dict()


def _dict_to_tuple(dict_obj):
    return tuple(sorted(dict_obj.items()))


def lookup_dimension(name):
    try:
        return _dimension_namespace[name]
    except KeyError:
        return None


class Dimension:
    def __init__(self, name: str, base=None, symbol=None):
        self.name = name
        self.base = None
        self.symbol = None
        if base is None:
            self.base = {self.name: 1}
            self.symbol = _symbols(name, positive=True, real=True)
        elif isinstance(base, Dimension):
            self.base = base.base
            self.symbol = base.symbol
        else:
            assert isinstance(base, dict) and symbol is not None, "base and symbol must be provided together"
            self.base = base
            self.symbol = symbol
        _dimension_space[_dict_to_tuple(self.base)] = self
        _dimension_namespace[self.name] = self

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __mul__(self, other):
        if isinstance(other, Dimension):
            new_base = {**self.base}
            for key, value in other.base.items():
                if key in new_base:
                    new_base[key] += value
                else:
                    new_base[key] = value
            new_base = {k: v for k, v in new_base.items() if v != 0}
            if _dict_to_tuple(new_base) in _dimension_space:
                return _dimension_space[_dict_to_tuple(new_base)]
            return Dimension(f"{self.name}*{other.name}", base=new_base, symbol=Mul(self.symbol, other.symbol))
        raise NotImplementedError

    def __rmul__(self, other):
        if isinstance(other, Dimension):
            new_base = {**self.base}
            for key, value in other.base.items():
                if key in new_base:
                    new_base[key] += value
                else:
                    new_base[key] = value
            new_base = {k: v for k, v in new_base.items() if v != 0}
            if _dict_to_tuple(new_base) in _dimension_space:
                return _dimension_space[_dict_to_tuple(new_base)]
            return Dimension(f"{other.name}*{self.name}", base=new_base, symbol=Mul(other.symbol, self.symbol))
        raise NotImplementedError

    def __truediv__(self, other):
        if isinstance(other, Dimension):
            new_base = {**self.base}
            for key, value in other.base.items():
                if key in new_base:
                    new_base[key] -= value
                else:
                    new_base[key] = -value
            new_base = {k: v for k, v in new_base.items() if v != 0}
            if _dict_to_tuple(new_base) in _dimension_space:
                return _dimension_space[_dict_to_tuple(new_base)]
            return Dimension(str.join("*", [f"{k}{f"**({v})" if v != 1 else ""}" for k, v in new_base.items()]), base=new_base, symbol=Mul(self.symbol, Pow(other.symbol, -1)))
        raise NotImplementedError


    def __rtruediv__(self, other):
        if isinstance(other, Dimension):
            new_base = {**self.base}
            for key, value in other.base.items():
                if key in new_base:
                    new_base[key] -= value
                else:
                    new_base[key] = -value
            new_base = {k: v for k, v in new_base.items() if v != 0}
            if _dict_to_tuple(new_base) in _dimension_space:
                return _dimension_space[_dict_to_tuple(new_base)]
            return Dimension(str.join("*", [f"{k}{f"**({v})" if v != 1 else ""}" for k, v in new_base.items()]), base=new_base, symbol=Mul(other.symbol, Pow(self.symbol, -1)))
        elif isinstance(other, numbers.Number) and other == 1:
            return pow(self, -1)
        raise NotImplementedError


    def __pow__(self, power):
        if isinstance(power, numbers.Number):
            new_base = {k: v*power for k, v in self.base.items()}
            new_base = {k: v for k, v in new_base.items() if v != 0}
            if _dict_to_tuple(new_base) in _dimension_space:
                return _dimension_space[_dict_to_tuple(new_base)]
            return Dimension(str.join("*", [f"{k}{f'**({v})' if v != 1 else ''}" for k, v in new_base.items()]), base=new_base, symbol=Pow(self.symbol, power))
        raise NotImplementedError


    def __hash__(self):
        return hash(_dict_to_tuple(self.base))

    def __eq__(self, other):
        if isinstance(other, Dimension):
            return hash(self) == hash(other)
        return False


class Dimensionless(Dimension):
    def __init__(self):
        super().__init__("dimensionless", base={}, symbol=1)


# Base Dimensions
current = Dimension("current")
length = Dimension("length")
luminous_intensity = Dimension("luminous_intensity")
mass = Dimension("mass")
temperature = Dimension("temperature")
time = Dimension("time")

# Derived Dimensions
acceleration = Dimension("acceleration", base=length/(time**2))
angle = Dimension("angle", base=length/length)
area = Dimension("area", base=length**2)
charge = Dimension("charge", base=time*current)
force = Dimension("force", base=mass*length/(time**2))
energy = Dimension("energy", base=force*length)
action = Dimension("action", base=energy*time)
frequency = Dimension("frequency", base=1/time)
power = Dimension("power", base=energy/time)
pressure = Dimension("pressure", base=force/area)
solid_angle = Dimension("solid_angle", base=area/area)
electric_potential = Dimension("electric_potential", base=power/current)
capacitance = Dimension("capacitance", base=charge/electric_potential)
resistance = Dimension("resistance", base=electric_potential/current)
conductance = Dimension("conductance", base=1/resistance)
magnetic_flux = Dimension("magnetic_flux", base=energy/current)
magnetic_induction = Dimension("magnetic_induction", base=magnetic_flux/area)
electric_inductance = Dimension("electric_inductance", base=resistance*time)
luminous_flux = Dimension("luminous_flux", base=luminous_intensity*solid_angle)
illuminance = Dimension("illuminance", base=luminous_flux/area)
volume = Dimension("volume", base=length**3)
velocity = Dimension("velocity", base=length/time)

# Dimensionless
dimensionless = Dimensionless()

__all__ = [
    'Dimension',
    'Dimensionless',
    'lookup_dimension',
    *(dimension for dimension in _dimension_namespace if ("*" not in dimension) and str.strip(dimension) != "")
]
