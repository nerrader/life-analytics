PRAGMA user_version = 2;

CREATE TABLE IF NOT EXISTS daily_summaries (
    summary_date TEXT PRIMARY KEY, --iso string
    mood INTEGER NOT NULL,
    productivity INTEGER NOT NULL,
    stress INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    description TEXT, -- the only nullable value
    start_at TEXT NOT NULL, --iso string
    end_at TEXT NOT NULL, --iso string
    effort INTEGER NOT NULL,
    enjoyability INTEGER NOT NULL,
    energy_before INTEGER NOT NULL,
    energy_after INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS sleep (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_at TEXT NOT NULL, --iso string
    end_at TEXT NOT NULL, --iso string
    quality INTEGER NOT NULL,
    sleep_type TEXT NOT NULL CHECK (sleep_type IN ("sleep", "nap"))
);
