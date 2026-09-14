PRAGMA user_version = 1;

CREATE TABLE IF NOT EXISTS daily_summaries (
    summary_date TEXT PRIMARY KEY, --iso string
    mood INTEGER NOT NULL CHECK (mood BETWEEN 1 AND 5),
    productivity INTEGER NOT NULL CHECK (productivity BETWEEN 1 AND 5),
    stress INTEGER NOT NULL CHECK (stress BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    description TEXT, -- the only nullable value
    start_at TEXT NOT NULL, --iso string
    end_at TEXT NOT NULL, --iso string
    effort INTEGER NOT NULL CHECK (effort BETWEEN 1 AND 5),
    enjoyability INTEGER NOT NULL CHECK (enjoyability BETWEEN 1 AND 5),
    energy_before INTEGER NOT NULL CHECK (energy_before BETWEEN 1 AND 5),
    energy_after INTEGER NOT NULL CHECK (energy_after BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS sleep (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_at TEXT NOT NULL, --iso string
    end_at TEXT NOT NULL, --iso string
    quality INTEGER NOT NULL CHECK (quality BETWEEN 1 AND 5),
    sleep_type TEXT NOT NULL CHECK (sleep_type IN ("sleep", "nap"))
);
