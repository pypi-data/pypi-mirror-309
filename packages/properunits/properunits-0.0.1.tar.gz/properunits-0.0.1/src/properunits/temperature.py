from .base import Magnitude

_T_names = {
    'C' : ['C', 'Celsius', 'Centigrades'],
    'K' : ['K', 'Kelvin'],
    'F' : ['F', 'Farenheit']
}

_T_conv = {
    'C' : lambda x: x + 273.15,
    'F' : lambda x: (x-32)/1.8
}

class Temperature(Magnitude):

    _units = 'K'

    def convert(self, val, units):
        key = self.check_units(units, _T_names)
        if key == Temperature._units:
            self._x = val
        else:
            self._x = _T_conv[key](val)

    @property
    def units(self):
        return Temperature._units

