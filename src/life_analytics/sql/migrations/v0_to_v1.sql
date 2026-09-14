CREATE TABLE new_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    description TEXT, -- the only nullable value
    start_at TEXT NOT NULL, --iso string datetime
    end_at TEXT NOT NULL, --iso string datetime
    effort INTEGER NOT NULL CHECK (effort BETWEEN 1 AND 5),
    enjoyability INTEGER NOT NULL CHECK (enjoyability BETWEEN 1 AND 5),
    energy_before INTEGER NOT NULL CHECK (energy_before BETWEEN 1 AND 5),
    energy_after INTEGER NOT NULL CHECK (energy_after BETWEEN 1 AND 5)
);

-- adding all the data in new_activities
INSERT INTO new_activities (
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
    activity_id,
    activity_category,
    activity_description,
    -- im assuming you did the activities on the same activity_date
    -- sorry but this is the best i can do for this migration
    activity_date || 'T' || activity_start AS start_at,
    activity_date || 'T' || activity_end AS end_at,
    effort,
    enjoyability,
    energy_before,
    energy_after
FROM activities;

DROP TABLE activities;
ALTER TABLE new_activities RENAME TO activities;

-- rename sleep columns
ALTER TABLE sleep RENAME sleep_id TO id;
ALTER TABLE sleep RENAME sleep_start_time TO start_at;
ALTER TABLE sleep RENAME sleep_end_time TO end_at;
ALTER TABLE sleep RENAME sleep_quality TO quality;

PRAGMA user_version = 1;
