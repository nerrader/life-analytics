import sqlite3

import pytest

from life_analytics.logic import database


def test_add_daily_summary_with_valid_data(tmp_path) -> None:
    database.create_database(tmp_path / "test.db")
    database.add_daily_summary(tmp_path / "test.db", "2026-04-08", 10, 10, 10)

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT date, productivity, mood, stress FROM daily_summaries")
        test_row = cursor.fetchone()

    assert test_row == ("2026-04-08", 10, 10, 10)


def test_add_daily_summary_with_invalid_data(tmp_path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_daily_summary(tmp_path / "test.db", "2026-20-20", -500, 11, 0)  # type: ignore (this is literally invalid data)


def test_add_activity_with_valid_data(tmp_path) -> None:
    database.create_database(tmp_path / "test.db")
    database.add_activity(
        tmp_path / "test.db", "2026-20-20", "testing", "17:34", "20:08", 10, 10
    )

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT activity_id, date, activity, activity_start, activity_end, difficulty, enjoyability FROM activities"
        )
        test_row = cursor.fetchone()

    assert test_row == (1, "2026-20-20", "testing", "17:34", "20:08", 10, 10)


def test_add_activity_with_invalid_data(tmp_path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_activity(
            tmp_path / "test.db",
            "2026-20-20",
            -500,  # type: ignore
            100,  # type: ignore
            "99:99",
            0,  # type: ignore
            0,  # type: ignore
        )


def test_add_sleep_with_valid_data(tmp_path) -> None:
    database.create_database(tmp_path / "test.db")
    database.add_sleep(tmp_path / "test.db", "2026-04-08T17:37", "2026-04-09T06:56", 10)

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT sleep_id, sleep_start_time, sleep_end_time, sleep_quality FROM sleep"
        )
        test_row = cursor.fetchone()

    assert test_row == (1, "2026-04-08T17:37", "2026-04-09T06:56", 10)


def test_add_sleep_with_invalid_data(tmp_path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_sleep(tmp_path / "test.db", "2026-20-01", 10, 11)  # type: ignore (this is literally invalid data)
