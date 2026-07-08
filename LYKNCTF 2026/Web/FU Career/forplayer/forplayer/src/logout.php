<?php
session_start();
session_destroy();
session_start();
$_SESSION['flash'] = ['type' => 'info', 'message' => 'Đã đăng xuất.'];
header("Location: index.php");
exit;
?>
