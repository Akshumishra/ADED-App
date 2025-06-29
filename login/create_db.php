<?php
$db = new SQLite3('db/users.db');

$db->exec("CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT,
    lastName TEXT,
    middleName TEXT,
    age INTEGER,
    dob TEXT,
    gender TEXT,
    address TEXT,
    section TEXT,
    course TEXT,
    email TEXT UNIQUE,
    password TEXT
)");

echo "Database and table created successfully.";
?>
