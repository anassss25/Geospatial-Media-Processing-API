import pytest
from src.processing.exif_parser import _convert_to_decimal_degrees

# Mocking the rational number structure that exifread uses internally
class MockRatio:
    def __init__(self, num, den):
        self.num = num
        self.den = den

class MockExifValue:
    def __init__(self, d, m, s):
        self.values = [MockRatio(*d), MockRatio(*m), MockRatio(*s)]

def test_convert_to_decimal_degrees_north_east():
    # 51° 30' 36" North should convert to a positive 51.51 decimal
    dms = MockExifValue((51, 1), (30, 1), (36, 1))
    decimal = _convert_to_decimal_degrees(dms, 'N')
    
    # Use pytest.approx to handle floating point precision issues
    assert decimal == pytest.approx(51.51, 0.001)

def test_convert_to_decimal_degrees_south_west():
    # West longitudes and South latitudes must return negative values for mapping
    dms = MockExifValue((51, 1), (30, 1), (36, 1))
    decimal = _convert_to_decimal_degrees(dms, 'W')
    
    assert decimal == pytest.approx(-51.51, 0.001)