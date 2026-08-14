CREATE TABLE IF NOT EXISTS daily_summaries (
    summary_date TEXT PRIMARY KEY, --iso string
    mood INTEGER NOT NULL CHECK (mood BETWEEN 1 AND 5),
    productivity INTEGER NOT NULL CHECK (productivity BETWEEN 1 AND 5),
    stress INTEGER NOT NULL CHECK (stress BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS activities (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_date TEXT NOT NULL,
    activity TEXT NOT NULL,
    activity_start TEXT NOT NULL, --iso string
    activity_end TEXT NOT NULL, --iso string
    effort INTEGER NOT NULL CHECK (effort BETWEEN 1 AND 5),
    enjoyability INTEGER NOT NULL CHECK (enjoyability BETWEEN 1 AND 5),

    FOREIGN KEY (activity_date) REFERENCES daily_summaries (summary_date)
);

CREATE TABLE IF NOT EXISTS sleep (
    sleep_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sleep_start_time TEXT NOT NULL, --iso string
    sleep_end_time TEXT NOT NULL, --iso string
    sleep_quality INTEGER NOT NULL CHECK (sleep_quality BETWEEN 1 AND 5)
);
