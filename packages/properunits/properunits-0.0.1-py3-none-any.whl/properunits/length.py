from .base import Magnitude

_length_names = {
    'nm' : ['nanometers'],
    'A' : ['Angstroms'],
    'in' : ['inch', 'inches'],
    'mi' : ['mile', 'miles'],
    'yd' : ['yard', 'yards']
}

_length_conv = {
    'nm' : lambda x: 1e-9*x,
    'A' : lambda x: 1e-10*x,
    'in' : lambda x: 2.54e-2*x,
    'mi' : lambda x: 1609.34*x,
    'yd' : lambda x: 0.9144*x,
}

_area_names = {
    'nm2' : ['nm^2'],
    'A2' : ['A^2'],
    'm2' : ['m^2']
}

_area_conv = {
    'nm2' : lambda x: 1e-18*x,
    'A2' : lambda x: 1e-20*x,
}

_volume_names = {
    'l' : ['liter', 'liters'],
    'cm3' : ['cm^3'],
    'm3' : ['m^3']
}

_volume_conv = {
    'l' : lambda x: 1e-6*x,
    'cm3' : lambda x: 1e-6*x,
}


class Length(Magnitude):

    _units = 'm'

    def convert(self, val, units):
        key = self.check_units(units, _length_names)
        if key == Length._units:
            self._x = val
        else:
            self._x = _length_conv[key](val)

    @property
    def units(self):
        return Length._units


class Area(Magnitude):

    _units = 'm2'

    def convert(self, val, units):
        key = self.check_units(units, _area_names)
        if key == Area._units:
            self._x = val
        else:
            self._x = _area_conv[key](val)

    @property
    def units(self):
        return Area._units


class Volume(Magnitude):

    _units = 'm3'

    def convert(self, val, units):
        key = self.check_units(units, _volume_names)
        if key == Volume._units:
            self._x = val
        else:
            self._x = _volume_conv[key](val)

    @property
    def units(self):
        return Volume._units
