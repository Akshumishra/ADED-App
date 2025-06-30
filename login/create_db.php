<?php
$db = new SQLite3('db/users.db');

$db->exec("CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullName TEXT,
    dob TEXT,
    gender TEXT,
    email TEXT UNIQUE,
    password TEXT
)");

echo "Database and table created successfully.";
?>
