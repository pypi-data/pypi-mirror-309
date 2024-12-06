from properunits import Temperature
import pytest


def test_temperature():
    temp = Temperature(100, 'C')
    assert temp.x == pytest.approx(373.15)

    