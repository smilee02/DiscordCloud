DROP TABLE IF EXISTS file;
DROP TABLE IF EXISTS file_chunk;
CREATE TABLE file (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    total_size INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE file_chunk (
    id TEXT PRIMARY KEY,
    file_id TEXT NOT NULL,
    chunk_number INTEGER NOT NULL,
    chunk_size INTEGER NOT NULL,
    FOREIGN KEY (file_id) REFERENCES file (id)
);