from .base import Magnitude

_p_names = {
    'Pa' : ['Pa', 'Pascal', 'Pascals'],
    'Torr' : ['Torr', 'torr', 'Torrs'],
    'mTorr' : ['mTorr', 'mtorr'],
    'atm' : ['atm', 'Atm', 'Atmos'],
    'psi' : ['PSI', 'Psi'],
    'ksi' : ['KSI'],
    'bar' : ['bar', 'Bar', 'bars']
}

_p_conv = {
    'Torr' : lambda x: 133.322*x,
    'mTorr' : lambda x: 0.133322*x,
    'atm' : lambda x: 101325*x,
    'psi' : lambda x: 6.894757e3*x,
    'ksi' : lambda x: 6.894757e6*x,
    'bar' : lambda x: 1e5*x
}

class Pressure(Magnitude):

    _units = 'Pa'

    def convert(self, val, units):
        key = self.check_units(units, _p_names)
        if key == Pressure._units:
            self._x = val
        else:
            self._x = _p_conv[key](val)

    @property
    def units(self):
        return Pressure._units

