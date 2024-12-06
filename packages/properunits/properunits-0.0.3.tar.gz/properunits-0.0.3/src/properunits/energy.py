from .base import Magnitude

_en_names = {
    'J' : ['Joules', 'joule', 'joules'],
    'eV' : ['ev'],
    'cal' : ['Cal', 'calories'],
    'kWh' : ['kiloWatt hour'],
    'Btu' : ['BTU']
}

_en_conv = {
    'eV' : lambda x: 1.6021767e-19*x,
    'cal' : lambda x: 4.184*x,
    'kWh' : lambda x: 3.6e6*x,
    'Btu' : lambda x: 1.0551e3*x
}

class Energy(Magnitude):

    _units = 'J'

    def _convert(self, val, units):
        key = self._check_units(units, _en_names)
        if key == Energy._units:
            self._x = val
        else:
            self._x = _en_conv[key](val)

    @property
    def units(self):
        return Energy._units

    def list_units():
        return list(_en_names.keys())
