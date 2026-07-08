<?php
session_start();

if (isset($_GET['lang']) && in_array($_GET['lang'], ['vi', 'en'])) {
    $_SESSION['lang'] = $_GET['lang'];
}
$lang = isset($_SESSION['lang']) ? $_SESSION['lang'] : 'vi';


$conn = mysqli_connect("127.0.0.1", "ctf", "ctfpassword", "fucareer");
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

function is_logged_in()
{
    return isset($_SESSION['user_id']);
}

function current_user()
{
    global $conn;
    if (!is_logged_in())
        return null;
    $id = (int) $_SESSION['user_id'];
    $result = mysqli_query($conn, "SELECT * FROM users WHERE id = $id");
    return mysqli_fetch_assoc($result);
}

function require_login()
{
    if (!is_logged_in()) {
        $_SESSION['flash'] = ['type' => 'warning', 'message' => 'Bạn cần đăng nhập để tiếp tục.'];
        header("Location: login.php");
        exit;
    }
}

function require_admin()
{
    require_login();
    $user = current_user();
    if ($user['role'] !== 'admin') {
        $_SESSION['flash'] = ['type' => 'danger', 'message' => 'Khu vực này chỉ dành cho admin.'];
        header("Location: dashboard.php");
        exit;
    }
}

function display_flash()
{
    if (isset($_SESSION['flash'])) {
        $flash = $_SESSION['flash'];
        echo "<div class='alert alert-{$flash['type']}'>{$flash['message']}</div>";
        unset($_SESSION['flash']);
    }
}
?>