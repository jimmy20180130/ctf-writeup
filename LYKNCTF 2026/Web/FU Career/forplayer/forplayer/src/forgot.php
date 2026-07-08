<?php
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = strtolower(trim($_POST['username'] ?? ''));
    
    $stmt = $conn->prepare("SELECT id FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows === 0) {
        $_SESSION['flash'] = ['type' => 'danger', 'message' => 'Không tìm thấy username này.'];
    } else {
        $user = $result->fetch_assoc();
        $otp = sprintf("%04d", mt_rand(0, 9999));
        $now = date('Y-m-d H:i:s');
        
        $update = $conn->prepare("UPDATE users SET reset_otp = ?, reset_otp_created_at = ? WHERE id = ?");
        $update->bind_param("ssi", $otp, $now, $user['id']);
        $update->execute();
        
        // Log to Apache error log for challenge debug (simulating sending to internal mail)
        error_log("CTF OTP for $username is $otp (valid for 30 min)");
        
        $_SESSION['flash'] = ['type' => 'info', 'message' => 'OTP đã được gửi tới mailbox nội bộ. Hãy nhập mã trong vòng 30 phút để đặt lại mật khẩu.'];
        header("Location: reset.php?username=" . urlencode($username));
        exit;
    }
}

require_once 'header.php';
?>

<section class="auth-shell">
  <form class="panel form-panel" method="post" action="forgot.php">
    <p class="eyebrow">Account Recovery</p>
    <h1><?= $lang=='en' ? 'Forgot Password' : 'Quên mật khẩu' ?></h1>
    <p class="muted" style="margin:8px 0 4px; font-size:.88rem;">Nhập đúng username để hệ thống gửi OTP 4 số tới mailbox nội bộ.</p>
    <label>Username<input name="username" placeholder="<?= $lang=='en' ? 'Enter username' : 'Nhập username' ?> của bạn" required></label>
    <button class="button" type="submit" style="width:100%; margin-top:8px;">Gửi OTP</button>
    <p class="muted" style="margin-top:14px; text-align:center; font-size:.88rem;">
      <a href="/login.php" style="color:var(--fpt-orange); font-weight:600;">← Quay lại đăng nhập</a>
    </p>
  </form>
</section>

<?php require_once 'footer.php'; ?>
