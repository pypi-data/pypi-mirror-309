from .base import Magnitude

_mass_names = {
    'kg' : ['kilo'],
    'g' : ['gram'],
    'lb' : ['pound', 'lbs'],
    'oz' : ['ounce', 'ounces'],
    't' : ['tonne'],
    'Da' : ['u', 'amu']
}

_mass_conv = {
    'g' : lambda x: 1e-3*x,
    'lb' : lambda x: 0.45359237*x,
    'oz' : lambda x: 28.349523125e-3*x,
    't' : lambda x: 1e3*x,
    'Da' : lambda x: 1.66053906892e-27*x
}

class Mass(Magnitude):

    _units = 'kg'

    def _convert(self, val, units):
        key = self._check_units(units, _mass_names)
        if key == Mass._units:
            self._x = val
        else:
            self._x = _mass_conv[key](val)

    @property
    def units(self):
        return Mass._units

    def list_units():
        return list(_mass_names.keys())
