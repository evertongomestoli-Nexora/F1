"""Pure, stateless functions for turning raw laps into dashboard results.

No I/O happens here, so these functions are unit-tested directly with no
mocking required.
"""

from __future__ import annotations

from f1.domain.models import Driver, FastestLapEntry, Lap


def filter_valid_laps(laps: list[Lap]) -> list[Lap]:
    """Keep only laps with a positive recorded duration that are not pit-out laps."""
    return [
        lap
        for lap in laps
        if lap.lap_duration is not None and lap.lap_duration > 0 and not lap.is_pit_out_lap
    ]


def build_driver_index(drivers: list[Driver]) -> dict[int, Driver]:
    """Index drivers by driver_number for O(1) lookup."""
    return {driver.driver_number: driver for driver in drivers}


def compute_top_n_laps(
    laps: list[Lap], driver_index: dict[int, Driver], n: int = 10
) -> list[FastestLapEntry]:
    """Compute the top-N fastest laps, one per driver, sorted ascending by duration.

    Laps are pre-filtered with `filter_valid_laps` by the caller (or here, for
    safety) before ranking. Only the fastest lap per driver is kept.
    """
    valid_laps = filter_valid_laps(laps)

    best_per_driver: dict[int, Lap] = {}
    for lap in valid_laps:
        current_best = best_per_driver.get(lap.driver_number)
        if current_best is None or lap.lap_duration < current_best.lap_duration:
            best_per_driver[lap.driver_number] = lap

    entries = []
    for driver_number, lap in best_per_driver.items():
        driver = driver_index.get(driver_number)
        driver_name = driver.full_name if driver else f"#{driver_number}"
        team_name = driver.team_name if driver else None
        entries.append(
            FastestLapEntry(
                driver_number=driver_number,
                driver_name=driver_name,
                team_name=team_name,
                lap_number=lap.lap_number,
                lap_duration=lap.lap_duration,
            )
        )

    entries.sort(key=lambda entry: entry.lap_duration)
    return entries[:n]
