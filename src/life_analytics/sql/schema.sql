CREATE TABLE daily_summaries (
    date TEXT PRIMARY KEY, --unix timestamp
    outside_for_leisure_minutes INTEGER NOT NULL,
    exercise_minutes INTEGER NOT NULL,
    mood INTEGER CHECK(mood BETWEEN 1 AND 10),
    productivity INTEGER CHECK(productivity BETWEEN 1 AND 10),
    stress INTEGER CHECK(stress BETWEEN 1 AND 10)
);

CREATE TABLE activities (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    activity TEXT NOT NULL,
    activity_start TEXT NOT NULL, --unix timestamp
    activity_end TEXT NOT NULL, --unix timestamp
    difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 10)
    enjoyability INTEGER CHECK(enjoyability BETWEEN 1 AND 10)
    productivity INTEGER CHECK(productivity BETWEEN 1 AND 10)

    FOREIGN KEY(date) REFERENCES daily_summaries(date)
);

CREATE TABLE sleep (
    sleep_id INTEGER PRIMARY_KEY AUTOINCREMENT,
    sleep_start_time TEXT NOT NULL --unix timestamp
    sleep_end_time TEXT NOT NULL --unix timestamp
    mood INTEGER CHECK(mood BETWEEN 1 AND 10)
);