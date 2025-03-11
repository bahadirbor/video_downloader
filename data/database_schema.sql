-- SQLite database schema codes

-- Channel names and id's
CREATE TABLE IF NOT EXISTS channels(
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS videos(
    id TEXT PRIMARY KEY,
    channel_id TEXT NOT NULL,
    title TEXT NOT NULL,
    published_at TEXT NOT NULL,
    download INTEGER DEFAULT 0, -- 1: Downloaded
    FOREIGN KEY (channel_id) REFERENCES channel(id)
);


CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    task_type TEXT CHECK(task_type IN ('video_check','download_check')) NOT NULL,
    last_run TIMESTAMP DEFAULT NULL,
    next_run TIMESTAMP NOT NULL
);
