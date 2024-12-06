
class Magnitude:
    """Base class for physical magnitudes
    
    A physical magnitude comprises a numerical value with units.

    These units are converted back to a default representation when
    the value is set. The original value and units are 
    """

    def __init__(self, val, units=None):
        self.set(val, units)

    def set(self, val, units):
        self._oval = val
        self._ounits = units
        self.convert(val, units)

    @property
    def val(self):
        return self._oval, self._ounits
    
    
    @property
    def x(self):
        return self._x

    @property
    def units(self):
        raise(NotImplementedError, "Units not defined")

    
    def convert(self, val, units):
        raise(NotImplementedError, "Conversion not implemented")
    
    def check_units(self, units, unit_dict):
        if units in unit_dict.keys():
            return units
        else:
            for k, v in unit_dict.items():
                if units in v:
                    return k
            return None
        

