from .base import Magnitude

_f_names = {
    'N' : ['Newton'],
    'dyn' : ['Dyne, dyne'],
    'lbf' : ['pound-force'],
    'pdl' : ['poundal']
}

_f_conv = {
    'dyn' : lambda x: 1e-5*x,
    'lbf' : lambda x: 4.448222*x,
    'pdl' : lambda x: 0.1382550*x
}

class Force(Magnitude):

    _units = 'N'

    def _convert(self, val, units):
        key = self._check_units(units, _f_names)
        if key == Force._units:
            self._x = val
        else:
            self._x = _f_conv[key](val)

    @property
    def units(self):
        return Force._units

    def unit_list():
        return list(_f_names.keys())
