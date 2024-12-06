from properunits import Mass
import pytest


def test_mass():
    m = Mass(100, 'lb')
    assert m.x == pytest.approx(45.359237)

