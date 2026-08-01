CREATE TABLE IF NOT EXISTS daily_summaries (
    date TEXT PRIMARY KEY, --iso string
    mood INTEGER NOT NULL CHECK(mood BETWEEN 1 AND 10),
    productivity INTEGER NOT NULL CHECK(productivity BETWEEN 1 AND 10),
    stress INTEGER NOT NULL CHECK(stress BETWEEN 1 AND 10)
);

CREATE TABLE IF NOT EXISTS activities (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    activity TEXT NOT NULL,
    activity_start TEXT NOT NULL, --iso string
    activity_end TEXT NOT NULL, --iso string
    difficulty INTEGER NOT NULL CHECK(difficulty BETWEEN 1 AND 10),
    enjoyability INTEGER NOT NULL CHECK(enjoyability  BETWEEN 1 AND 10),

    FOREIGN KEY(date) REFERENCES daily_summaries(date)
);

CREATE TABLE IF NOT EXISTS sleep (
    sleep_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sleep_start_time TEXT NOT NULL, --iso string
    sleep_end_time TEXT NOT NULL, --iso string
    mood INTEGER NOT NULL CHECK(mood BETWEEN 1 AND 10)
);