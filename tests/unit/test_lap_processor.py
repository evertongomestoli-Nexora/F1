"""Unit tests for the pure functions in `f1.processing.lap_processor`."""

from f1.domain.models import Driver, Lap
from f1.processing.lap_processor import (
    build_driver_index,
    compute_top_n_laps,
    filter_valid_laps,
)


def make_lap(driver_number: int, lap_number: int, lap_duration, is_pit_out_lap=False) -> Lap:
    return Lap(
        session_key=1,
        driver_number=driver_number,
        lap_number=lap_number,
        lap_duration=lap_duration,
        is_pit_out_lap=is_pit_out_lap,
    )


def test_filter_valid_laps_drops_none_duration():
    laps = [make_lap(1, 1, None), make_lap(1, 2, 90.5)]
    result = filter_valid_laps(laps)
    assert result == [laps[1]]


def test_filter_valid_laps_drops_zero_or_negative_duration():
    laps = [make_lap(1, 1, 0), make_lap(1, 2, -5.0), make_lap(1, 3, 90.5)]
    result = filter_valid_laps(laps)
    assert result == [laps[2]]


def test_filter_valid_laps_drops_pit_out_laps():
    laps = [make_lap(1, 1, 95.0, is_pit_out_lap=True), make_lap(1, 2, 90.5)]
    result = filter_valid_laps(laps)
    assert result == [laps[1]]


def test_build_driver_index_maps_by_driver_number():
    drivers = [
        Driver(driver_number=1, session_key=1, full_name="Driver One"),
        Driver(driver_number=44, session_key=1, full_name="Driver Two"),
    ]
    index = build_driver_index(drivers)
    assert index[1].full_name == "Driver One"
    assert index[44].full_name == "Driver Two"


def test_compute_top_n_laps_keeps_only_fastest_per_driver():
    drivers = [Driver(driver_number=1, session_key=1, full_name="Driver One", team_name="Team A")]
    driver_index = build_driver_index(drivers)
    laps = [make_lap(1, 1, 92.0), make_lap(1, 2, 89.0), make_lap(1, 3, 91.0)]

    result = compute_top_n_laps(laps, driver_index, n=10)

    assert len(result) == 1
    assert result[0].lap_number == 2
    assert result[0].lap_duration == 89.0
    assert result[0].driver_name == "Driver One"
    assert result[0].team_name == "Team A"


def test_compute_top_n_laps_sorts_ascending_and_limits_to_n():
    driver_index: dict[int, Driver] = {}
    laps = [make_lap(1, 1, 95.0), make_lap(2, 1, 90.0), make_lap(3, 1, 92.0)]

    result = compute_top_n_laps(laps, driver_index, n=2)

    assert [entry.driver_number for entry in result] == [2, 3]
    assert result[0].driver_name == "#2"


def test_compute_top_n_laps_ignores_invalid_laps():
    driver_index: dict[int, Driver] = {}
    laps = [make_lap(1, 1, None), make_lap(2, 1, 90.0, is_pit_out_lap=True)]

    result = compute_top_n_laps(laps, driver_index, n=10)

    assert result == []
