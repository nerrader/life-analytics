from dataclasses import dataclass

from life_analytics.domain.constants import SleepType


@dataclass
class SummaryInputs:
    mood: float | None = None
    productivity: float | None = None
    stress: float | None = None


@dataclass
class ActivityInputs:
    category: str | None = None
    description: str | None = None
    start_at: str | None = None
    end_at: str | None = None
    effort: float | None = None
    enjoyability: float | None = None
    energy_before: float | None = None
    energy_after: float | None = None


@dataclass
class SleepInputs:
    start_at: str | None = None
    end_at: str | None = None
    quality: float | None = None
    sleep_type: SleepType | None = None
