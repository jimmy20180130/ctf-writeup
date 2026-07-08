<?php
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = strtolower(trim($_POST['username'] ?? ''));
    $password = $_POST['password'] ?? '';
    
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    $user = $result->fetch_assoc();
    
    if ($user && password_verify($password, $user['password_hash'])) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['flash'] = ['type' => 'success', 'message' => 'Đăng nhập thành công.'];
        header("Location: dashboard.php");
        exit;
    }
    
    $_SESSION['flash'] = ['type' => 'danger', 'message' => 'Sai username hoặc password.'];
}

require_once 'header.php';
?>

<section class="auth-shell">
  <form class="panel form-panel" method="post" action="login.php">
    <p class="eyebrow">Candidate Portal</p>
    <h1><?= $lang=='en' ? 'Login' : 'Đăng nhập' ?></h1>
    <p class="muted" style="margin:8px 0 4px; font-size:.88rem;"><?= $lang=='en' ? 'Login to manage your applications.' : 'Đăng nhập để quản lý hồ sơ ứng tuyển của bạn.' ?></p>
    <label>Username<input name="username" autocomplete="username" placeholder="<?= $lang=='en' ? 'Enter username' : 'Nhập username' ?>" required></label>
    <label>Password<input name="password" type="password" autocomplete="current-password" placeholder="<?= $lang=='en' ? 'Enter password' : 'Nhập mật khẩu' ?>" required></label>
    <button class="button" type="submit" style="width:100%; margin-top:8px;"><?= $lang=='en' ? 'Login' : 'Đăng nhập' ?></button>
    <p class="muted" style="margin-top:14px; text-align:center; font-size:.88rem;">
      <a href="/forgot.php" style="color:var(--fpt-orange); font-weight:600;"><?= $lang=='en' ? 'Forgot password?' : 'Quên mật khẩu?' ?></a>
      &nbsp;·&nbsp;
      <a href="/register.php" style="color:var(--fpt-orange); font-weight:600;"><?= $lang=='en' ? 'Create new account' : 'Tạo tài khoản mới' ?></a>
    </p>
  </form>
</section>

<?php require_once 'footer.php'; ?>
