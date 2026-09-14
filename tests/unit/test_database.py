import sqlite3
from pathlib import Path

import pytest

from life_analytics.logic import database


def test_add_daily_summary_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    database.add_daily_summary(
        tmp_path / "test.db",
        {
            "summary_date": "2026-04-08",
            "productivity": 5,
            "mood": 5,
            "stress": 5,
        },
    )

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT summary_date, productivity, mood, stress FROM daily_summaries"
        )
        test_row = cursor.fetchone()

    assert test_row == ("2026-04-08", 5, 5, 5)


def test_add_daily_summary_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_daily_summary(
            tmp_path / "test.db",
            {
                "summary_date": "2026-04-08",
                "productivity": 6,
                "mood": 5,
                "stress": 5,
            },
        )


def test_add_activity_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    database.add_activity(
        tmp_path / "test.db",
        {
            "category": "DEV",
            "description": "unit testing",
            "start_at": "17:34",
            "end_at": "20:08",
            "effort": 5,
            "enjoyability": 5,
            "energy_before": 5,
            "energy_after": 5,
        },
    )

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, category, description,
                   start_at, end_at, effort, enjoyability,
                   energy_before, energy_after
            FROM activities
            """
        )
        test_row = cursor.fetchone()

    assert test_row == (
        1,
        "DEV",
        "unit testing",
        "17:34",
        "20:08",
        5,
        5,
        5,
        5,
    )


def test_add_activity_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_activity(
            tmp_path / "test.db",
            {
                "category": "DEV",
                "description": "unit testing",
                "start_at": "99:99",
                "end_at": "99:99",
                "effort": 0,
                "enjoyability": 0,
                "energy_before": 5,
                "energy_after": 5,
            },
        )


def test_add_sleep_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    database.add_sleep(
        tmp_path / "test.db",
        {
            "start_at": "2026-04-08T17:37",
            "end_at": "2026-04-09T06:56",
            "quality": 5,
            "sleep_type": "sleep",
        },
    )

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, start_at, end_at,
                   quality, sleep_type
            FROM sleep
            """
        )
        test_row = cursor.fetchone()

    assert test_row == (
        1,
        "2026-04-08T17:37",
        "2026-04-09T06:56",
        5,
        "sleep",
    )


def test_add_sleep_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_sleep(
            tmp_path / "test.db",
            {
                "start_at": "2026-04-08T17:37",
                "end_at": "2026-04-09T06:56",
                "quality": 6,
                "sleep_type": "sleep",
            },
        )
