<?php
$conn = mysqli_connect("127.0.0.1", "ctf", "ctfpassword", "fucareer");
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Seed Admin User if not exists
$admin_username = "admin";
$check_admin = mysqli_query($conn, "SELECT id FROM users WHERE username = '$admin_username'");
if (mysqli_num_rows($check_admin) == 0) {
    $password_hash = password_hash(bin2hex(random_bytes(18)), PASSWORD_DEFAULT);
    $now = date('Y-m-d H:i:s');
    $stmt = $conn->prepare("INSERT INTO users (username, password_hash, email, full_name, department, role, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)");
    $email = "lan.nt.hr@fedu-career.local";
    $full_name = "Nguyen Thi Lan";
    $dept = "Talent Acquisition";
    $role = "admin";
    $stmt->bind_param("sssssss", $admin_username, $password_hash, $email, $full_name, $dept, $role, $now);
    $stmt->execute();
}

// Seed Demo User if not exists
$demo_username = "candidate.demo";
$check_demo = mysqli_query($conn, "SELECT id FROM users WHERE username = '$demo_username'");
if (mysqli_num_rows($check_demo) == 0) {
    $password_hash = password_hash("candidate123", PASSWORD_DEFAULT);
    $now = date('Y-m-d H:i:s');
    $stmt = $conn->prepare("INSERT INTO users (username, password_hash, email, full_name, department, role, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)");
    $email = "candidate@example.local";
    $full_name = "Demo Candidate";
    $dept = "Applicant";
    $role = "user";
    $stmt->bind_param("sssssss", $demo_username, $password_hash, $email, $full_name, $dept, $role, $now);
    $stmt->execute();
    $demo_id = $stmt->insert_id;

    // Insert demo CV
    $stmt = $conn->prepare("INSERT INTO cv_submissions (user_id, candidate_name, position, original_filename, stored_filename, cover_letter, status, created_at) VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)");
    $pos = "Giảng viên An toàn thông tin";
    $orig = "demo_cv.txt";
    $stored = "seed_cv.txt";
    $cover = "Tôi quan tâm tới môi trường giáo dục thực học, thực làm.";
    $stmt->bind_param("issssss", $demo_id, $full_name, $pos, $orig, $stored, $cover, $now);
    $stmt->execute();
}

// Seed Internal Notes
$check_notes = mysqli_query($conn, "SELECT id FROM internal_notes");
if (mysqli_num_rows($check_notes) == 0) {
    mysqli_query($conn, "INSERT INTO internal_notes (title, body, visibility) VALUES ('Admin console', 'CV preview chạy bằng pipeline nội bộ, chỉ mở trong dashboard admin.', 'admin')");
}

echo "Database seeded successfully.\n";
?>
