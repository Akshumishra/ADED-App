<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $db = new SQLite3('db/users.db');

    $firstName = $_POST['firstName'] ?? '';
    $lastName = $_POST['lastName'] ?? '';
    $middleName = $_POST['middleName'] ?? '';
    $age = $_POST['age'] ?? '';
    $dob = $_POST['DOB'] ?? '';
    $gender = $_POST['gender'] ?? '';
    $address = $_POST['address'] ?? '';
    $section = $_POST['section'] ?? '';
    $course = $_POST['course'] ?? '';
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';

    // Hash the password
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

    // Check if email already exists
    $stmt = $db->prepare("SELECT * FROM users WHERE email = :email");
    $stmt->bindValue(':email', $email, SQLITE3_TEXT);
    $result = $stmt->execute();
    $user = $result->fetchArray(SQLITE3_ASSOC);

    if ($user) {
        echo "<script>alert('Email already registered. Please log in.'); window.location.href='../Landing Page/pages/login.html';</script>";
    } else {
        // Insert user data
        $stmt = $db->prepare("INSERT INTO users (firstName, lastName, middleName, age, dob, gender, address, section, course, email, password) 
            VALUES (:firstName, :lastName, :middleName, :age, :dob, :gender, :address, :section, :course, :email, :password)");
        
        $stmt->bindValue(':firstName', $firstName, SQLITE3_TEXT);
        $stmt->bindValue(':lastName', $lastName, SQLITE3_TEXT);
        $stmt->bindValue(':middleName', $middleName, SQLITE3_TEXT);
        $stmt->bindValue(':age', $age, SQLITE3_INTEGER);
        $stmt->bindValue(':dob', $dob, SQLITE3_TEXT);
        $stmt->bindValue(':gender', $gender, SQLITE3_TEXT);
        $stmt->bindValue(':address', $address, SQLITE3_TEXT);
        $stmt->bindValue(':section', $section, SQLITE3_TEXT);
        $stmt->bindValue(':course', $course, SQLITE3_TEXT);
        $stmt->bindValue(':email', $email, SQLITE3_TEXT);
        $stmt->bindValue(':password', $hashedPassword, SQLITE3_TEXT);

        $stmt->execute();

        echo "<script>alert('Registration successful! You can now log in.'); window.location.href='../Landing Page/pages/login.html';</script>";
    }
}
?>
