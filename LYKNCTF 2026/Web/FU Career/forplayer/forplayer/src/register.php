<?php
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = strtolower(trim($_POST['username'] ?? ''));
    $password = $_POST['password'] ?? '';
    $full_name = trim($_POST['full_name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $department = trim($_POST['department'] ?? 'Applicant');
    if (empty($department)) $department = 'Applicant';

    if (!$username || !$password || !$full_name || !$email) {
        $_SESSION['flash'] = ['type' => 'warning', 'message' => 'Vui lòng nhập đầy đủ thông tin.'];
    } else {
        $check = mysqli_query($conn, "SELECT id FROM users WHERE username = '" . mysqli_real_escape_string($conn, $username) . "'");
        if (mysqli_num_rows($check) > 0) {
            $_SESSION['flash'] = ['type' => 'danger', 'message' => 'Username đã tồn tại.'];
        } else {
            $hash = password_hash($password, PASSWORD_DEFAULT);
            $now = date('Y-m-d H:i:s');
            $stmt = $conn->prepare("INSERT INTO users (username, password_hash, email, full_name, department, role, created_at) VALUES (?, ?, ?, ?, ?, 'user', ?)");
            $stmt->bind_param("ssssss", $username, $hash, $email, $full_name, $department, $now);
            if ($stmt->execute()) {
                $_SESSION['flash'] = ['type' => 'success', 'message' => 'Tạo tài khoản thành công, bạn có thể đăng nhập.'];
                header("Location: login.php");
                exit;
            } else {
                $_SESSION['flash'] = ['type' => 'danger', 'message' => 'Lỗi hệ thống.'];
            }
        }
    }
}
require_once 'header.php';
?>

<section class="auth-shell">
  <form class="panel form-panel" method="post" action="register.php">
    <p class="eyebrow"><?= $lang=='en' ? 'New Candidate' : 'Ứng viên mới' ?></p>
    <h1><?= $lang=='en' ? 'Create Account' : 'Tạo tài khoản' ?></h1>
    <p class="muted" style="margin:8px 0 4px; font-size:.88rem;"><?= $lang=='en' ? 'Register to submit your CV and track application status.' : 'Đăng ký để gửi CV và theo dõi trạng thái ứng tuyển.' ?></p>
    <label><?= $lang=='en' ? 'Full Name' : 'Họ tên' ?> <span style="color:var(--fpt-red);">*</span><input name="full_name" placeholder="<?= $lang=='en' ? 'Enter full name' : 'Nhập họ tên đầy đủ' ?>" required></label>
    <label>Email <span style="color:var(--fpt-red);">*</span><input name="email" type="email" placeholder="email@example.com" required></label>
    <label>Username <span style="color:var(--fpt-red);">*</span><input name="username" placeholder="<?= $lang=='en' ? 'Choose a username' : 'Chọn username' ?>" required></label>
    <label><?= $lang=='en' ? 'Interested Department' : 'Đơn vị quan tâm' ?>
      <select name="department">
        <option value="Applicant" selected><?= $lang=='en' ? 'General Applicant' : 'Ứng viên chung' ?></option>
        <option value="Trường Đại học FPT"><?= $lang=='en' ? 'FPT University' : 'Trường Đại học FPT' ?></option>
        <option value="FPT Polytechnic"><?= $lang=='en' ? 'FPT Polytechnic College' : 'Trường Cao đẳng FPT Polytechnic' ?></option>
        <option value="FPT Schools"><?= $lang=='en' ? 'FPT Schools System' : 'Hệ thống Trường Phổ thông FPT' ?></option>
        <option value="Greenwich Việt Nam">Greenwich Vietnam</option>
        <option value="Tổ chức Giáo dục FPT"><?= $lang=='en' ? 'FPT Education' : 'Tổ chức Giáo dục FPT' ?></option>
      </select>
    </label>
    <label>Password <span style="color:var(--fpt-red);">*</span><input name="password" type="password" placeholder="<?= $lang=='en' ? 'Create password' : 'Tạo mật khẩu' ?>" required></label>
    <button class="button" type="submit" style="width:100%; margin-top:8px;"><?= $lang=='en' ? 'Create Account' : 'Tạo tài khoản' ?></button>
    <p class="muted" style="margin-top:14px; text-align:center; font-size:.88rem;">
      <?= $lang=='en' ? 'Already have an account?' : 'Đã có tài khoản?' ?> <a href="/login.php" style="color:var(--fpt-orange); font-weight:600;"><?= $lang=='en' ? 'Login' : 'Đăng nhập' ?></a>
    </p>
  </form>
</section>

<?php require_once 'footer.php'; ?>
