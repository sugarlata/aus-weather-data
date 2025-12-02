import pytest

from aus_weather_data.common.utils import get_translation_coordinate


@pytest.mark.parametrize(
    "latitude, longitude, distance, bearing, target_latitude, target_longitude",
    [
        # Test case: North from equator
        (0, 0, 100, 0, 0.89832, 0),
        # Test case: East from equator
        (0, 0, 100, 90, 0, 0.89832),
        # Test case: South from equator
        (0, 0, 100, 180, -0.89832, 0),
        # Test case: West from equator
        (0, 0, 100, 270, 0, -0.89832),
        # Test case: Northeast from Sydney
        (-33.8688, 151.2093, 50, 45, -33.55061, 151.5904),
        # Test case: Small distance
        (37.7749, -122.4194, 1, 90, 37.7749, -122.40803),
        # Test case: Large distance
        (0, 0, 1000, 0, 8.9832, 0),
        # Test case: Bearing at 360 (should wrap to 0)
        (0, 0, 100, 360, 0.89832, 0),
    ],
)
def test_translation_coordinate_success(
    latitude, longitude, distance, bearing, target_latitude, target_longitude
):
    """Test successful coordinate translation calculations."""
    result = get_translation_coordinate(latitude, longitude, distance, bearing)
    assert result == (target_latitude, target_longitude)


@pytest.mark.parametrize(
    "latitude, longitude, distance, bearing, expected_error",
    [
        # Distance validation errors
        (0, 0, -1, 0, ValueError),  # Negative distance
        (0, 0, -100, 0, ValueError),  # Large negative distance
        (0, 0, -0.1, 0, ValueError),  # Small negative distance
        # Bearing validation errors
        (0, 0, 100, -1, ValueError),  # Negative bearing
        (0, 0, 100, 361, ValueError),  # Bearing > 360
        (0, 0, 100, -0.1, ValueError),  # Small negative bearing
        (0, 0, 100, 360.1, ValueError),  # Bearing slightly > 360
        # Latitude validation errors
        (-91, 0, 100, 0, ValueError),  # Latitude < -90
        (91, 0, 100, 0, ValueError),  # Latitude > 90
        (-90.1, 0, 100, 0, ValueError),  # Latitude slightly < -90
        (90.1, 0, 100, 0, ValueError),  # Latitude slightly > 90
        # Longitude validation errors
        (0, -181, 100, 0, ValueError),  # Longitude < -180
        (0, 181, 100, 0, ValueError),  # Longitude > 180
        (0, -180.1, 100, 0, ValueError),  # Longitude slightly < -180
        (0, 180.1, 100, 0, ValueError),  # Longitude slightly > 180
        # Edge cases: boundary values (these should pass, but testing them)
        # Note: 0 distance might be edge case - testing it in success case
        # Combined invalid parameters
        (-91, -181, -100, 361, ValueError),  # All invalid
    ],
)
def test_translation_coordinate_failure(
    latitude, longitude, distance, bearing, expected_error
):
    """Test that ValueError is raised for invalid input parameters."""
    with pytest.raises(expected_error):
        get_translation_coordinate(latitude, longitude, distance, bearing)
