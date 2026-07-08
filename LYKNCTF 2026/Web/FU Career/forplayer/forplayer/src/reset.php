<?php
require_once 'config.php';

$username = $_GET['username'] ?? '';
if (empty($username)) {
    header("Location: forgot.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $otp = trim($_POST['otp'] ?? '');
    $new_password = $_POST['password'] ?? '';
    
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    $user = $result->fetch_assoc();
    
    if (!$user) {
        $_SESSION['flash'] = ['type' => 'danger', 'message' => 'Tài khoản không tồn tại.'];
    } elseif (empty($user['reset_otp'])) {
        $_SESSION['flash'] = ['type' => 'warning', 'message' => 'OTP chưa được tạo. Vui lòng yêu cầu reset mật khẩu.'];
    } elseif ($otp === $user['reset_otp']) {
        if ($user['reset_otp_created_at']) {
            $otp_created = strtotime($user['reset_otp_created_at']);
            $now = time();
            $elapsed = $now - $otp_created;
            
            if ($elapsed > 1800) { // 30 minutes
                $_SESSION['flash'] = ['type' => 'danger', 'message' => 'OTP đã hết hạn. Vui lòng yêu cầu OTP mới.'];
            } elseif (!empty($new_password)) {
                $hash = password_hash($new_password, PASSWORD_DEFAULT);
                $update = $conn->prepare("UPDATE users SET password_hash = ?, reset_otp = NULL, reset_otp_created_at = NULL WHERE id = ?");
                $update->bind_param("si", $hash, $user['id']);
                $update->execute();
                
                $_SESSION['flash'] = ['type' => 'success', 'message' => 'Đổi mật khẩu thành công.'];
                header("Location: login.php");
                exit;
            } else {
                $_SESSION['flash'] = ['type' => 'warning', 'message' => 'Vui lòng nhập mật khẩu mới.'];
            }
        }
    } else {
        $_SESSION['flash'] = ['type' => 'danger', 'message' => 'OTP không đúng.'];
    }
}

require_once 'header.php';
?>

<section class="auth-shell">
  <form class="panel form-panel" method="post" action="reset.php?username=<?= urlencode($username) ?>">
    <p class="eyebrow">Reset cho <?= htmlspecialchars($username) ?></p>
    <h1>Nhập OTP</h1>
    <p class="muted" style="margin:8px 0 4px; font-size:.88rem;">Nhập mã OTP 4 chữ số đã được gửi tới mailbox nội bộ và mật khẩu mới.</p>
    <label>OTP 4 số<input name="otp" inputmode="numeric" maxlength="4" placeholder="Nhập OTP" required style="text-align:center; font-size:1.3rem; letter-spacing:8px; font-weight:700;"></label>
    <label>Password mới<input name="password" type="password" placeholder="Nhập mật khẩu mới" required></label>
    <button class="button" type="submit" style="width:100%; margin-top:8px;">Đổi mật khẩu</button>
  </form>
</section>

<?php require_once 'footer.php'; ?>
