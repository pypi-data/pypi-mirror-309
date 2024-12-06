from sympy import Dummy
from sympy import pi as _pi
from uniTbrow import dimensions as d
from typing import Optional, Literal

__all__: list[str] = []

_unit_library = dict()


class Unit(Dummy):
    def __new__(cls, name, base=None, dimension=None, proper_name: str = "", doc: str = ""):
        return Dummy.__new__(cls, name, real=True, positive=True)


    def __init__(self, name, base=None, dimension=None, proper_name: str = "", doc: str = ""):
        assert dimension is not None, "dimension must be provided"

        super().__init__()

        self.dimension = dimension
        self.base = base
        self.name = name
        self.proper_name = proper_name
        self.doc = doc
        super().__init__()

    def __repr__(self):
        return self.name

    def __str__(self):
        return repr(self) + " (" + self.dimension.name + ")"


def define_unit(name, alt_names=None, proper_name: str = "", base=None, dimension=None, prefixes: Optional[Literal["metric", "binary"]] = None, doc: str = ""):
    unit = Unit(name, base=base, dimension=dimension, proper_name=proper_name, doc=doc)

    all_names = [name]
    all_names.extend(alt_names)
    for n in all_names:
        if n in _unit_library:
            raise ValueError(f"Unit {n} already defined")
        _unit_library[n] = unit
        globals()[n] = unit
    if prefixes is not None:
        selected_prefixes = []
        if prefixes == "metric":
            selected_prefixes = _metric_prefixes
        elif prefixes == "binary":
            selected_prefixes = _binary_prefixes
        for prefix, prefix_names, factor in selected_prefixes:
            new_proper_name = prefix_names[0] + proper_name
            define_unit(
                prefix + name,
                [
                    *[prefix + n for n in alt_names],
                    *[p + name for p in prefix_names],
                    *[p + n for n in alt_names for p in prefix_names]
                ],
                proper_name=new_proper_name,
                base=factor*unit,
                dimension=unit.dimension,
                doc=doc
            )
    return unit


def lookup_unit(name):
    try:
        if isinstance(name, str):
            return _unit_library[name]
        else:
            return name
    except KeyError:
        return None


def to_base_units(expr):
    changes = None
    while changes != 0:
        changes = 0
        for symbol in expr.free_symbols:
            if isinstance(symbol, Unit):
                unit = symbol
                if unit.base is None:
                    continue
                changes += 1
                expr = expr.subs(symbol, unit.base)
            else:
                continue
    return expr



_metric_prefixes = [
    ("Q", ["quetta"], 10**30),
    ("R", ["ronna"], 10**27),
    ("Y", ["yotta"], 10**24),
    ("Z", ["zetta"], 10**21),
    ("E", ["exa"], 10**18),
    ("P", ["peta"], 10**15),
    ("T", ["tera"], 10**12),
    ("G", ["giga"], 10**9),
    ("M", ["mega"], 10**6),
    ("k", ["kilo"], 10**3),
    ("h", ["hecto"], 10**2),
    ("da", ["deka", "deca"], 10**1),
    ("d", ["deci"], 10**-1),
    ("c", ["centi"], 10**-2),
    ("m", ["milli"], 10**-3),
    ("μ", ["micro", "u"], 10**-6),
    ("n", ["nano"], 10**-9),
    ("p", ["pico"], 10**-12),
    ("f", ["femto"], 10**-15),
    ("a", ["atto"], 10**-18),
    ("z", ["zepto"], 10**-21),
    ("y", ["yocto"], 10**-24),
    ("r", ["ronto"], 10**-27),
    ("q", ["quecto"], 10**-30)
]

_binary_prefixes = [
    
]

# Base Units
m = define_unit("m", ["meter", "metre"], proper_name="meter", dimension=d.length, prefixes="metric")
g = define_unit("g", ["gram"], proper_name="gram", dimension=d.mass, prefixes="metric")
s = define_unit("s", ["second"], proper_name="second", dimension=d.time, prefixes="metric")
mol = define_unit("mol", ["mole"], proper_name="mole", dimension=d.dimensionless, prefixes="metric")
A = define_unit("A", ["ampere", "amp"], proper_name="amp", dimension=d.current, prefixes="metric")
K = define_unit("K", ["kelvin"], proper_name="kelvin", dimension=d.temperature, prefixes="metric")
cd = define_unit("cd", ["candela"], proper_name="candela", dimension=d.luminous_intensity, prefixes="metric")

# Derived Units
kg = lookup_unit("kg")
Hz = define_unit("Hz", ["hertz"], proper_name="hertz", base=1/s, dimension=d.frequency, prefixes="metric")
rad = define_unit("rad", ["radian"], proper_name="radian", base=1, dimension=d.angle)
sr = define_unit("sr", ["steradian"], proper_name="steradian", base=1, dimension=d.solid_angle)
N = define_unit("N", ["newton"], proper_name="newton", base=kg*m/s**2, dimension=d.force, prefixes="metric")
Pa = define_unit("Pa", ["pascal"], proper_name="pascal", base=N/m**2, dimension=d.pressure, prefixes="metric")
J = define_unit("J", ["joule"], proper_name="joule", base=N*m, dimension=d.energy, prefixes="metric")
W = define_unit("W", ["watt"], proper_name="watt", base=J/s, dimension=d.power, prefixes="metric")
C = define_unit("C", ["coulomb"], proper_name="coulomb", base=A*s, dimension=d.charge, prefixes="metric")
V = define_unit("V", ["volt"], proper_name="volt", base=W/A, dimension=d.electric_potential, prefixes="metric")
F = define_unit("F", ["farad"], proper_name="farad", base=C/V, dimension=d.capacitance, prefixes="metric")
ohm = define_unit("Ω", ["ohm"], proper_name="ohm", base=V/A, dimension=d.resistance, prefixes="metric")
S = define_unit("S", ["siemen"], proper_name="siemen", base=A/V, dimension=d.conductance, prefixes="metric")
Wb = define_unit("Wb", ["weber"], proper_name="weber", base=V*s, dimension=d.magnetic_flux, prefixes="metric")
T = define_unit("T", ["tesla"], proper_name="tesla", base=Wb/m**2, dimension=d.magnetic_induction, prefixes="metric")
H = define_unit("H", ["henry"], proper_name="henry", base=Wb/A, dimension=d.electric_inductance, prefixes="metric")

# Basic Imperial Units
yd = define_unit("yd", ["yard"], proper_name="yard", base=0.9144*m, dimension=d.length)
ft = define_unit("ft", ["foot", "feet"], proper_name="foot", base=yd/3, dimension=d.length)
inch = define_unit("in", ["inch"], proper_name="inch", base=ft/12, dimension=d.length)
mile = define_unit("mile", [], proper_name="mile", base=5280*ft, dimension=d.length)
lb = define_unit("lb", ["lbs", "pound"], proper_name="pound", base=0.45359237*kg, dimension=d.mass)

# ------------------------------ Angles ------------------------------
deg = define_unit("°", ["deg", "degree"], proper_name="degree", base=rad*180/_pi, dimension=d.angle)
turn = define_unit("tr", ["turn", "pla"], proper_name="turn", base=rad*2*_pi, dimension=d.angle)
gradian = define_unit("gon", ["ᵍ", "grad", "grade"], proper_name="grade", base=rad*_pi/200, dimension=d.angle)
arcmin = define_unit("arcmin", ["arcminute"], proper_name="arcminute", base=deg/60, dimension=d.angle)
arcsec = define_unit("arcsec", ["arcsecond"], proper_name="arcsecond", base=deg/3600, dimension=d.angle, prefixes="metric")

# ------------------------------ Area ------------------------------
acre = define_unit("acre", ["ac"], proper_name="acre", base=(4840*yd**2), dimension=d.area)
hectare = define_unit("ha", ["hectare"], proper_name="hectare", base=(10000*m**2), dimension=d.area)

# --------------------------- Astronomy ---------------------------
AU = define_unit("AU", ["astronomical_unit"], proper_name="astronomical unit", base=(149597870700*m), dimension=d.length)
pc = define_unit("pc", ["parsec"], proper_name="parsec", base=(AU/_pi), dimension=d.length, prefixes="metric")
ly = define_unit("ly", ["lightyear", "lyr"], proper_name="lightyear", base=9460730472580800*m, dimension=d.length, prefixes="metric")
earth_mass = define_unit("M_⊕", ["M_E", "earth_mass", "earths"], proper_name="earth mass", base=5.9722e24*kg, dimension=d.mass)
solar_mass = define_unit("M_☉", ["M_sun", "solar_mass", "M_{\\odot}", "M_\\odot"], proper_name="solar mass", base=1.98847e30*kg, dimension=d.mass)
solar_luminosity = define_unit("L_☉", ["L_sun", "solar_luminosity", "L_{\\odot}", "L_\\odot"], proper_name="solar luminosity", base=3.828e26*W, dimension=d.power)

# ----------------------------- Energy -----------------------------
erg = define_unit("erg", [], proper_name="erg", base=1e-7*J, dimension=d.energy)
eV = define_unit("eV", ["electronvolt", "electron_volt"], proper_name="electronvolt", base=1.602176634e-19*J, dimension=d.energy, prefixes="metric")
cal = define_unit("cal", ["calorie"], base=4.184*J, proper_name="calorie", dimension=d.energy, prefixes="metric")

# -------------------------- Electrostatic -------------------------
abampere = define_unit("abA", ["abampere"], proper_name="abampere", base=10*A, dimension=d.current)
biot = define_unit("Bi", ["biot"], proper_name="biot", base=10*A, dimension=d.current)
abcoulomb = define_unit("abC", ["abcoulomb"], proper_name="abcoulomb", base=10*C, dimension=d.charge)
abfarad = define_unit("abF", ["abfarad"], proper_name="abfarad", base=1e9*F, dimension=d.capacitance)
abhenry = define_unit("abH", ["abhenry"], proper_name="abhenry", base=1e-9*H, dimension=d.electric_inductance)
abohm = define_unit("abΩ", ["abohm"], proper_name="abohm", base=1e-9*ohm, dimension=d.resistance)
absiemen = define_unit("abS", ["absiemen"], proper_name="absiemen", base=1e9*S, dimension=d.conductance)
abvolt = define_unit("abV", ["abvolt"], proper_name="abvolt", base=1e-8*V, dimension=d.electric_potential)
# TODO verify faraday = define_unit("F", ["faraday"], proper_name="faraday", base=96485.33212*C, dimension=d.charge)
# TODO verify statampere = define_unit("statA", ["statampere"], proper_name="statampere", base=3.335640952e-10*A, dimension=d.current)
# TODO verify statcoulomb = define_unit("statC", ["statcoulomb"], proper_name="statcoulomb", base=3.335640952e-10*C, dimension=d.charge)
# TODO verify statfarad = define_unit("statF", ["statfarad"], proper_name="statfarad", base=1.112650056e-12*F, dimension=d.capacitance)
# TODO verify statmho = define_unit("statS", ["statmho"], proper_name="statmho", base=1.112650056e-12*S, dimension=d.conductance)
# TODO verify statohm = define_unit("statΩ", ["statohm"], proper_name="statohm", base=8.987551787e11*ohm, dimension=d.resistance)
# TODO verify statvolt = define_unit("statV", ["statvolt"], proper_name="statvolt", base=299.792458*V, dimension=d.electric_potential)

# ---------------------------- Frequency ---------------------------
# TODO verify Bq = define_unit("Bq", ["becquerel"], proper_name="becquerel", base=1/s, dimension=d.frequency, prefixes="metric")
# TODO verify Ci = define_unit("Ci", ["curie"], proper_name="curie", base=3.7e10*Bq, dimension=d.frequency, prefixes="metric")
# TODO verify R = define_unit("R", ["roentgen"], proper_name="roentgen", base=2.58e-4*C/kg, dimension=d.frequency)

# ---------------------------- Force -------------------------------
dyne = define_unit("dyn", ["dyne"], proper_name="dyne", base=1e-5*N, dimension=d.force)
lbf = define_unit("lbf", ["poundforce"], proper_name="pounds of force", base=4.4482216152605*N, dimension=d.force)
poundal = define_unit("pdl", ["poundal"], proper_name="poundal", base=lb*ft/s**2, dimension=d.force)

# ---------------------------- Illuminance -------------------------
lumen = define_unit("lm", ["lumen"], proper_name="lumen", base=cd*sr, dimension=d.luminous_flux)
lux = define_unit("lx", ["lux"], proper_name="lux", base=cd/m**2, dimension=d.illuminance)
fc = define_unit("fc", ["footcandle"], proper_name="footcandle", base=lumen/ft**2, dimension=d.illuminance)
phot = define_unit("ph", ["phot"], proper_name="phot", base=10000*lux, dimension=d.illuminance)

# ----------------------------- Length -----------------------------
fermi = define_unit("fermi", [], proper_name="fermi", base=1e-15*m, dimension=d.length)
micron = define_unit("micron", [], proper_name="micron", base=1e-6*m, dimension=d.length)
angstrom = define_unit("Å", ["angstrom"], proper_name="angstrom", base=1e-10*m, dimension=d.length)
fathom = define_unit("fathom", [], proper_name="fathom", base=6*ft, dimension=d.length)
nautical_mile = define_unit("nmi", ["NM", "M", "nautical_mile"], proper_name="nautical mile", base=1852*m, dimension=d.length)
furlong = define_unit("furlong", [], proper_name="furlong", base=220*yd, dimension=d.length)
meh_egyptian = define_unit("meh_egyptian", ["ell_egyptian_royal", "cubit_egyptian_royal"], proper_name="meh (egyptian)", base=0.525*m, dimension=d.length)  # https://www.sizes.com/units/meh.htm
amma_egyptian = define_unit("amma_egyptian", [], proper_name="amma (egyptian)", base=40*meh_egyptian, dimension=d.length)  # https://www.sizes.com/units/amma.htm

# ---------------------------- Luminance ---------------------------
# TODO verify nit = define_unit("nt", ["nit"], base=cd/m**2, dimension=d.luminance)
# TODO verify stilb = define_unit("sb", ["stilb"], base=1e4*cd/m**2, dimension=d.luminance)

# ---------------------------- Magnetic ----------------------------
# TODO verify G = define_unit("G", ["gauss"], base=1e-4*T, dimension=d.magnetic_induction)
# TODO verify Mx = define_unit("Mx", ["maxwell"], base=1e-8*Wb, dimension=d.magnetic_flux)
# TODO verify Gs = define_unit("Gs", ["gauss_second"], base=1e-4*T*s, dimension=d.magnetic_flux)
# TODO verify Oe = define_unit("Oe", ["oersted"], base=250/(4*_pi)*A/m, dimension=d.magnetic_field_strength)

# ------------------------------ Mass ------------------------------
tonne = define_unit("t", ["tonne", "ton_metric"], proper_name="ton (metric)", base=1000*kg, dimension=d.mass)
dalton = define_unit("Da", ["dalton", "u"], proper_name="dalton", base=1.6604390666050e-27*kg, dimension=d.mass, prefixes="metric")
slug = define_unit("sl", ["slug"], proper_name="slug", base=14.59390294*kg, dimension=d.mass)
oz = define_unit("oz", ["ounce"], proper_name="ounce", base=lb/16, dimension=d.mass)
ton = define_unit("ton", ["ton_short"], proper_name="ton (short)", base=2000*lb, dimension=d.mass)
ton_long = define_unit("ton_long", ["ton_imperial", "ton_displacement"], proper_name="ton (imperial)", base=2240*lb, dimension=d.mass)
carat = define_unit("ct", ["carat"], proper_name="carat", base=0.2*g, dimension=d.mass)
carat_imperial = define_unit("ct_imp", ["carat_imperial"], proper_name="carat (imperial)", base=0.00705*oz, dimension=d.mass)
almud_ecu = define_unit("almud_ecu", ["almud_ecuador"], proper_name="almud (ecuador)", base=12.88*kg, dimension=d.mass)  # https://www.sizes.com/units/almud.htm
libra_ecu = define_unit("libra_ecu", ["libra_ecuador"], proper_name="libra (ecuador)", base=460*g, dimension=d.mass)  # https://www.sizes.com/units/libra.htm

# ------------------------------ Power ------------------------------
hp = define_unit("hp", ["horsepower", "horsepower_metric"], proper_name="horsepower (metric)", base=735.49875*W, dimension=d.power, prefixes="metric")
horsepower_mechanical = define_unit("hp_I", ["horsepower_imperial", "horsepower_mechanical"], proper_name="horsepower (imperial)", base=550*ft*lbf/s, dimension=d.power)
horsepower_electric = define_unit("hp_E", ["horsepower_electric"], proper_name="horsepower (electric)", base=746*W, dimension=d.power)
horsepower_boiler = define_unit("hp_S", ["horsepower_boiler"], proper_name="horsepower (boiler)", base=9812.5*W, dimension=d.power)

# ---------------------------- Pressure ----------------------------
bar = define_unit("bar", [], proper_name="bar", base=1e5*Pa, dimension=d.pressure, prefixes="metric")
atm = define_unit("atm", ["atmosphere", "atmosphere_standard"], proper_name="atmosphere", base=101325*Pa, dimension=d.pressure)
mmHg = define_unit("mmHg", ["mm_Hg"], proper_name="millimeters mercury", base=133.322387415*Pa, dimension=d.pressure)
inHg = define_unit("inHg", ["in_Hg"], proper_name="inches mercury", base=3386.389*Pa, dimension=d.pressure)
torr = define_unit("torr", [], proper_name="torr", base=(101325/760)*Pa, dimension=d.pressure)

# ---------------------------- Radiation ---------------------------
# TODO verify Gy = define_unit("Gy", ["gray"], proper_name="gray", base=1*J/kg, dimension=d.dose_equivalent)
# TODO verify Sv = define_unit("Sv", ["sievert"], proper_name="sievert", base=1*J/kg, dimension=d.dose_equivalent)
# TODO verify Bq = define_unit("Bq", ["becquerel"], proper_name="becquerel", base=1/s, dimension=d.activity)
# TODO verify Ci = define_unit("Ci", ["curie"], proper_name="curie", base=3.7e10*Bq, dimension=d.activity)
# TODO verify R = define_unit("R", ["roentgen"], proper_name="roentgen", base=2.58e-4*C/kg, dimension=d.exposure)

# ---------------------------- Resistance --------------------------

# ---------------------------- Temperature -------------------------
rankine = define_unit("°R", ["rankine"], proper_name="degrees rankine", base=K*5/9, dimension=d.temperature)
# TODO fahrenheit = define_unit("°F", ["fahrenheit"], proper_name="degrees fahrenheit", base=(K-459.67)*5/9, dimension=d.temperature)
# TODO celsius = define_unit("°C", ["celsius"], proper_name="degrees celsius", base=K-273.15, dimension=d.temperature)
# TODO reaumur = define_unit("°Ré", ["réaumur"], proper_name="réaumur", base=(K-273.15)*4/5, dimension=d.temperature)

# ---------------------------- Time -------------------------------
minute = define_unit("min", ["minute"], proper_name="minute", base=60*s, dimension=d.time)
hour = define_unit("h", ["hour"], proper_name="hour", base=60*minute, dimension=d.time)
day = define_unit("day", [], proper_name="day", base=24*hour, dimension=d.time)
week = define_unit("wk", ["week"], proper_name="week", base=7*day, dimension=d.time)
fortnight = define_unit("fortnight", [], proper_name="fortnight", base=14*day, dimension=d.time)
year = define_unit("yr", ["year", "year_julian"], proper_name="year (julian)", base=365.25*day, dimension=d.time)
year_leap = define_unit("leap_year", ["year_leap"], proper_name="year (leap)", base=366*day, dimension=d.time)
month = define_unit("mo", ["month"], proper_name="month", base=365.25/12*day, dimension=d.time)
# TODO verify month_sidereal = define_unit("mo_s", ["month_sidereal"], proper_name="month (sidereal)", base=27.321661*day, dimension=d.time)
# TODO verify month_synodic = define_unit("mo_l", ["month_lunar", "month_synodic"], proper_name="month (lunar)", base=29.53059*day, dimension=d.time)
# TODO verify month_tropical = define_unit("mo_t", ["month_tropical"], proper_name="month (tropical)", base=27.321582*day, dimension=d.time)
# TODO verify month_gregorian = define_unit("mo_g", ["month_gregorian"], proper_name="month (gregorian)", base=30.436875*day, dimension=d.time)

# ---------------------------- Velocity ---------------------------
kph = define_unit("kph", ["kilometers_per_hour"], proper_name="kilometers per hour", base=1000*m/hour, dimension=d.velocity)
mph = define_unit("mph", ["miles_per_hour"], proper_name="miles per hour", base=mile/hour, dimension=d.velocity)
fps = define_unit("fps", ["feet_per_second"], proper_name="feet per second", base=ft/s, dimension=d.velocity)
knot = define_unit("kn", ["knot"], proper_name="knot", base=nautical_mile/hour, dimension=d.velocity)
mach = define_unit("mach", [], proper_name="mach", base=343*m/s, dimension=d.velocity)
c = define_unit("c", ["speed_of_light"], proper_name="speed of light", base=299792458*m/s, dimension=d.velocity)

# ---------------------------- Volume -----------------------------
L = define_unit("L", ["liter", "litre", "l", "ℓ"], proper_name="liter", base=1e-3*m**3, dimension=d.volume, prefixes="metric")
# US Liquid Units
gal = define_unit("gal", ["gallon", "gal_US", "gallon_US"], proper_name="gallon (US)", base=231*inch**3, dimension=d.volume)
qt = define_unit("qt", ["quart", "qt_US", "quart_US"], proper_name="quart (US)", base=1/4*gal, dimension=d.volume)
pt = define_unit("pt", ["pint", "pt_US", "pint_US"], proper_name="pint (US)", base=1/2*qt, dimension=d.volume)
cup = define_unit("cup", ["cup_US"], proper_name="cup (US)", base=1/2*pt, dimension=d.volume)
floz = define_unit("floz", ["floz_US", "fluid_ounce", "fluid_ounce_US"], proper_name="fluid ounce (US)", base=1/8*cup, dimension=d.volume)
tbsp = define_unit("tbsp", ["tablespoon", "tablespoon_US"], proper_name="tablespoon (US)", base=1/2*floz, dimension=d.volume)
tsp = define_unit("tsp", ["teaspoon", "teaspoon_US"], proper_name="teaspoon (US)", base=1/3*tbsp, dimension=d.volume)
peck = define_unit("peck", ["peck_US"], proper_name="peck (US)", base=2*gal, dimension=d.volume)
bushel = define_unit("bu", ["bu_US", "bushel", "bushel_US"], proper_name="bushel (US)", base=8*gal, dimension=d.volume)
# US Dry Units
gal_dry = define_unit("gal_dry", ["gallon_dry", "gal_US_dry", "gallon_US_dry"], proper_name="gallon (US, dry)", base=268.8025*inch**3, dimension=d.volume)
qt_dry = define_unit("qt_dry", ["quart_dry", "qt_US_dry", "quart_US_dry"], proper_name="quart (US, dry)", base=1/4*gal_dry, dimension=d.volume)
pt_dry = define_unit("pt_dry", ["pint_dry", "pt_US_dry", "pint_US_dry"], proper_name="pint (US, dry)", base=1/2*qt_dry, dimension=d.volume)
peck_dry = define_unit("peck_dry", ["peck_US_dry"], base=2*gal_dry, proper_name="peck (US, dry)", dimension=d.volume)
bushel_dry = define_unit("bu_dry", ["bu_US_dry", "bushel_dry", "bushel_US_dry"], proper_name="bushel (US, dry)", base=8*gal_dry, dimension=d.volume)
# UK Liquid Units
gal_imp = define_unit("gal_imp", ["gallon_imp", "gallon_UK", "gal_UK"], proper_name="gallon (imperial)", base=4.54609*L, dimension=d.volume)
qt_imp = define_unit("qt_imp", ["quart_imp", "quart_UK", "qt_UK"], base=1/4*gal_imp, proper_name="quart (imperial)", dimension=d.volume)
pt_imp = define_unit("pt_imp", ["pint_imp", "pint_UK", "pt_UK"], proper_name="pint (imperial)", base=1/2*qt_imp, dimension=d.volume)
floz_imp = define_unit("floz_imp", ["fluid_ounce_imp", "floz_UK", "fluid_ounce_UK"], proper_name="fluid ounce (imperial)", base=1/160*gal_imp, dimension=d.volume)
tbsp_imp = define_unit("tbsp_imp", ["tablespoon_imp", "tbsp_UK", "tablespoon_UK"], proper_name="tablespoon (imperial)", base=1/2*floz_imp, dimension=d.volume)
tsp_imp = define_unit("tsp_imp", ["teaspoon_imp", "tsp_UK", "teaspoon_UK"], proper_name="teaspoon (imperial)", base=1/3*tbsp_imp, dimension=d.volume)
peck_imp = define_unit("peck_imp", ["peck_UK"], proper_name="peck (imperial)", base=2*gal_imp, dimension=d.volume)
bushel_imp = define_unit("bu_imp", ["bushel_imp", "bushel_UK", "bu_UK"], proper_name="bushel (imperial)", base=8*gal_imp, dimension=d.volume)
# UK Dry Units
gal_imp_dry = define_unit("gal_imp_dry", ["gallon_imp_dry", "gallon_UK_dry", "gal_UK_dry"], proper_name="gallon (imperial, dry)", base=4.54609*L, dimension=d.volume)
qt_imp_dry = define_unit("qt_imp_dry", ["quart_imp_dry", "quart_UK_dry", "qt_UK_dry"], proper_name="quart (imperial, dry)", base=1/4*gal_imp_dry, dimension=d.volume)
pt_imp_dry = define_unit("pt_imp_dry", ["pint_imp_dry", "pint_UK_dry", "pt_UK_dry"], proper_name="pint (imperial, dry)", base=1/2*qt_imp_dry, dimension=d.volume)
peck_imp_dry = define_unit("peck_imp_dry", ["peck_UK_dry"], proper_name="peck (imperial, dry)", base=2*gal_imp_dry, dimension=d.volume)
bushel_imp_dry = define_unit("bu_imp_dry", ["bushel_imp_dry", "bushel_UK_dry"], proper_name="bushel (imperial, dry)", base=8*gal_imp_dry, dimension=d.volume)
# Other Units
almude_portugal = define_unit("almude_portugal", ["almude_prt"], proper_name="almud (portugal)", base=16.7*L, dimension=d.volume)  # https://www.sizes.com/units/almude.htm
almude_paraguay = define_unit("almude_paraguay", ["almude_pry"], proper_name="almud (paraguay)", base=24*L, dimension=d.volume)  # https://www.sizes.com/units/almude.htm
almud_spain = define_unit("almud_spain", ["almud_esp"], proper_name="almud (spain)", base=4.625*L, dimension=d.volume)  # Thomas J. Glover - Pocket Ref, 4th Ed. ISBN 978-1-88507162-0
almud_canary_islands = define_unit("almud_canary_islands", ["almud_ci"], proper_name="almud (canary islands)", base=5.5*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_cordoba = define_unit("almud_cordoba", ["almud_cba"], proper_name="almud (cordoba)", base=18.08*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_corrientes = define_unit("almud_corrientes", ["almud_crt"], proper_name="almud (corrientes)", base=21.49*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_mendoza = define_unit("almud_mendoza", ["almud_mza"], proper_name="almud (mendoza)", base=9.31*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_belize = define_unit("almud_belize", ["almud_blz"], proper_name="almud (belize)", base=5.683*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_chile = define_unit("almud_chile", ["almud_chl"], proper_name="almud (chile)", base=8.08*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_mexico = define_unit("almud_mexico", ["almud_mex"], proper_name="almud (mexico)", base=7.568*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_philippines = define_unit("almud_philippines", ["almud_phl"], proper_name="almud (philippines)", base=1.76*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_puerto_rico = define_unit("almud_puerto_rico", ["almud_pri"], proper_name="almud (puerto rico)", base=20*L, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
fanega_new_mexico = define_unit("fanega_new_mexico", ["fanega_nm"], proper_name="fanega (new mexico)", base=2476.25*inch**3, dimension=d.volume)  # https://www.sizes.com/units/almud.htm
almud_new_mexico = define_unit("almud_new_mexico", ["almud_nm"], proper_name="almud (new mexico)", base=fanega_new_mexico / 6, dimension=d.volume)  # https://www.sizes.com/units/almud.htm


unit_symbol_dictionary = {name: unit for name, unit in _unit_library.items()}

# Insert units into namespace
__all__ += [
    "Unit",
    "lookup_unit",
    "to_base_units",
    "unit_symbol_dictionary",
    *(unit for unit in _unit_library)
]

