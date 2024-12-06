# Properunits
A simple framework to work with physical magnitudes


## Motivation

Properunits does one simple job: it helps
you define physical magnitudes in Python using units
and automatically convert them to SI units so that
downstream calculations are all done consistently.

Properunits does not attempt to do universal unit conversion
or tries to implement operations that preserve and transform
the units. It is meant to extract numerical values that can
be used anywhere without having to worry about unit conversion,
while keeping information on the original value and units used.


## Status

Properunits is still in development. Please check the
documentation in [readthedocs](https://properunits.readthedocs.io/en/latest/).


## Quick install

Through pypi:

```
pip install properunits
```

## Usage

```
from properunits import Temperature, Pressure

T = Temperature(100, 'C')
p = Pressure(1, 'bar')

print(T.x, T.units) # Return value in SI units.
print(Temperature.list_units()) # Return list of temperature units
print(T.value) # Return the original value, unit
```

## Copyright and license

Properunits is distributed under the terms of MIT License. 

