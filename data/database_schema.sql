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
    decription TEXT,
    published_at TEXT NOT NULL,
    download INTEGER DEFAULT 0, -- 1: Downloaded
    FOREIGN KEY (channel_id) REFERENCES channel(id)
);

CREATE TABLE IF NOT EXISTS downloads(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    status TEXT CHECK(status IN ('pending','in_progress','completed','failed')) DEFAULT 'pending',
    download_path TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES videos(id)
);

CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    task_type TEXT CHECK(task_type IN ('video_check','download_check')) NOT NULL,
    last_run TIMESTAMP DEFAULT NULL,
    next_run TIMESTAMP NOT NULL
);
