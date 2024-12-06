from properunits import Length, Area, Volume
import pytest


def test_length():
    p = Length(100, 'nm')
    assert p.x == pytest.approx(1e-7)


def test_area():
    p = Area(100, 'nm^2')
    assert p.x == pytest.approx(1e-17)


def test_volume():
    p = Volume(100, 'l')
    assert p.x == pytest.approx(100e-6)
