from collections.abc import Iterable, Sequence
from datetime import datetime
from statistics import mean
from typing import Any

from life_analytics.logic.database import ActivityRecord, SleepRecord, SummaryRecord


def calculate_tracking_stats(
    summary_records: Sequence[SummaryRecord],
) -> dict[str, Any]:
    first_summary = summary_records[-1]

    first_tracking_date = first_summary.summary_date
    tracking_days = len(summary_records)

    return {"Tracking Since": first_tracking_date, "Tracked Days": tracking_days}


def calculate_daily_summary_data(
    summary_records: Iterable[SummaryRecord],
) -> dict[str, Any]:
    average_mood = mean([record.mood for record in summary_records])
    average_productivity = mean([record.productivity for record in summary_records])
    average_stress = mean([record.stress for record in summary_records])

    return {
        "Avg Mood": average_mood,
        "Avg Productivity": average_productivity,
        "Avg Stress": average_stress,
    }


def calculate_activity_data(
    activity_records: Iterable[ActivityRecord],
) -> dict[str, Any]:
    activity_durations = [
        (
            datetime.fromisoformat(record.end_at)
            - datetime.fromisoformat(record.start_at)
        ).total_seconds()
        for record in activity_records
    ]

    average_durations = mean(activity_durations)
    average_effort = mean(record.effort for record in activity_records)
    average_enjoyability = mean(record.enjoyability for record in activity_records)

    return {
        "Avg Duration": average_durations,
        "Avg Effort": average_effort,
        "Avg Enjoyability": average_enjoyability,
    }


def calculate_sleep_data(sleep_records: Iterable[SleepRecord]) -> dict[str, Any]:
    sleep_durations = [
        (
            datetime.fromisoformat(record.end_at)
            - datetime.fromisoformat(record.start_at)
        ).total_seconds()
        for record in sleep_records
    ]

    average_duration = mean(sleep_durations)
    average_sleep_quality = mean(record.quality for record in sleep_records)
    total_naps = len([record for record in sleep_records if record.sleep_type == "nap"])

    return {
        "Avg Duration": average_duration,
        "Avg Quality": average_sleep_quality,
        "Total Naps": total_naps,
    }
