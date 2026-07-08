<?php
require_once 'config.php';
require_login();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $user = current_user();
    $position = trim($_POST['position'] ?? 'Ứng tuyển mở');
    $cover_letter = trim($_POST['cover_letter'] ?? '');
    $candidate_name = $user['full_name'];
    
    if (!isset($_FILES['cv']) || $_FILES['cv']['error'] !== UPLOAD_ERR_OK) {
        $_SESSION['flash'] = ['type' => 'warning', 'message' => 'Vui lòng chọn file CV.'];
        header("Location: dashboard.php");
        exit;
    }
    
    $file = $_FILES['cv'];
    $allowed_extensions = ['txt', 'pdf', 'doc', 'docx'];
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    
    if (!in_array($ext, $allowed_extensions)) {
        $_SESSION['flash'] = ['type' => 'danger', 'message' => 'CV chỉ nhận txt, pdf, doc, docx.'];
        header("Location: dashboard.php");
        exit;
    }
    
    $original = basename($file['name']);
    $stored = $user['id'] . '_' . bin2hex(random_bytes(4)) . '_' . preg_replace('/[^a-zA-Z0-9_.-]/', '_', $original);
    $upload_dir = __DIR__ . '/uploads/';
    $upload_path = $upload_dir . $stored;
    
    if (move_uploaded_file($file['tmp_name'], $upload_path)) {
        $now = date('Y-m-d H:i:s');
        $stmt = $conn->prepare("INSERT INTO cv_submissions (user_id, candidate_name, position, original_filename, stored_filename, cover_letter, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)");
        $stmt->bind_param("issssss", $user['id'], $candidate_name, $position, $original, $stored, $cover_letter, $now);
        $stmt->execute();
        
        $_SESSION['flash'] = ['type' => 'success', 'message' => 'CV đã được gửi tới bộ phận tuyển dụng.'];
    } else {
        $_SESSION['flash'] = ['type' => 'danger', 'message' => 'Lỗi upload file.'];
    }
    header("Location: dashboard.php");
    exit;
}
?>
