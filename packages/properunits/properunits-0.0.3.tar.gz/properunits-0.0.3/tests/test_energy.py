from properunits import Energy
import pytest


def test_energy():
    en = Energy(100, 'BTU')
    assert en.x == pytest.approx(1.0551e5)

def test_energy_units():
    Energy.list_units()
    
