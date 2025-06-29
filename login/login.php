<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $db = new SQLite3('db/users.db');

    $email = trim($_POST['email']);
    $password = trim($_POST['password']);

    $stmt = $db->prepare("SELECT * FROM users WHERE email = :email");
    $stmt->bindValue(':email', $email, SQLITE3_TEXT);
    $result = $stmt->execute();
    $user = $result->fetchArray(SQLITE3_ASSOC);

    if ($user && password_verify($password, $user['password'])) {
        echo "<script>alert('Logged in successfully!'); window.location.href='dashboard.html';</script>";
    } else {
        echo "<script>alert('Incorrect credentials. Please register yourself on the portal.'); window.location.href='register.html';</script>";
    }
}
?>
