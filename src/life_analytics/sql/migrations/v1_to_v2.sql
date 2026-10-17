CREATE TABLE daily_summaries_new (
    summary_date TEXT PRIMARY KEY,
    mood INTEGER NOT NULL,
    productivity INTEGER NOT NULL,
    stress INTEGER NOT NULL
);

INSERT INTO daily_summaries_new (
    summary_date,
    mood,
    productivity,
    stress
)
SELECT
    summary_date,
    mood,
    productivity,
    stress
FROM daily_summaries;

DROP TABLE daily_summaries;

ALTER TABLE daily_summaries_new
RENAME TO daily_summaries;

CREATE TABLE activities_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    description TEXT,
    start_at TEXT NOT NULL,
    end_at TEXT NOT NULL,
    effort INTEGER NOT NULL,
    enjoyability INTEGER NOT NULL,
    energy_before INTEGER NOT NULL,
    energy_after INTEGER NOT NULL
);

INSERT INTO activities_new (
    id,
    category,
    description,
    start_at,
    end_at,
    effort,
    enjoyability,
    energy_before,
    energy_after
)
SELECT
    id,
    category,
    description,
    start_at,
    end_at,
    effort,
    enjoyability,
    energy_before,
    energy_after
FROM activities;

DROP TABLE activities;

ALTER TABLE activities_new
RENAME TO activities;

CREATE TABLE sleep_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_at TEXT NOT NULL,
    end_at TEXT NOT NULL,
    quality INTEGER NOT NULL,
    sleep_type TEXT NOT NULL CHECK (sleep_type IN ('sleep', 'nap'))
);

INSERT INTO sleep_new (
    id,
    start_at,
    end_at,
    quality,
    sleep_type
)
SELECT
    id,
    start_at,
    end_at,
    quality,
    sleep_type
FROM sleep;

DROP TABLE sleep;

ALTER TABLE sleep_new
RENAME TO sleep;

PRAGMA user_version = 2;
