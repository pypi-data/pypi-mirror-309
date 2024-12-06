
class Magnitude:
    """Base class for physical magnitudes
    
    A physical magnitude comprises a numerical value with units.

    The magnitude is converted to SI units as it is defined. The
    original value and units are still preserved.
    """

    def __init__(self, val, units=None):
        self.set(val, units)

    def set(self, val, units):
        """Set a new value and units"""
        self._oval = val
        self._ounits = units
        self._convert(val, units)

    @property
    def value(self):
        """Return the original value and units"""
        return self._oval, self._ounits
    
    
    @property
    def x(self):
        """Return the converted value"""
        return self._x

    @property
    def units(self):
        """Return the converted units"""
        raise(NotImplementedError, "Units not defined")

    def unit_list():
        raise(NotImplementedError, "list of units not implemented")
    
    def _convert(self, val, units):
        raise(NotImplementedError, "Conversion not implemented")
    
    def _check_units(self, units, unit_dict):
        if units in unit_dict.keys():
            return units
        else:
            for k, v in unit_dict.items():
                if units in v:
                    return k
            return None
        

