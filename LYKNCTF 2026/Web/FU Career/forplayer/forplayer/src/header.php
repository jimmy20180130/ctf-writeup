<?php
require_once 'config.php';
$me = current_user();
?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FPT Education Career</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <link href="https://career.fpt.edu.vn/Content/scripts/bootstrap/css/bootstrap.css" rel="stylesheet" />
    <link href="/css/style.css" rel="stylesheet" />
    <link href="/css/ctf.css" rel="stylesheet" />
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
<header>
    <div class="container">
        <div class="header-inner" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
            <a href="/" class="header-logo">
                <img src="https://career.fpt.edu.vn/Assets/images/logo.svg" alt="FPT Education" style="height: 40px;">
            </a>
            <div class="header-right-wrapper">
                <div class="header-right">
                    <ul class="header-menu" style="display: flex; list-style: none; gap: 20px; margin: 0; align-items: center;">
                        <li><a href="/" style="text-decoration: none; color: #333; font-weight: 600;"><?= $lang == 'en' ? 'Home' : 'Trang chủ' ?></a></li>
                        <li><a target="_blank" href="https://fpt.edu.vn/About" style="text-decoration: none; color: #333; font-weight: 600;"><?= $lang == 'en' ? 'About Us' : 'Về chúng tôi' ?></a></li>
                        <li><a href="/#jobs" style="text-decoration: none; color: #333; font-weight: 600;"><?= $lang == 'en' ? 'Jobs' : 'Việc làm' ?></a></li>
                        <li><a href="/#news" style="text-decoration: none; color: #333; font-weight: 600;"><?= $lang == 'en' ? 'News' : 'Tin tức' ?></a></li>
                        <?php if ($me): ?>
                            <li><a href="/dashboard.php" style="text-decoration: none; color: #f37021; font-weight: 600;">Dashboard</a></li>
                            <li><a href="/logout.php" style="text-decoration: none; color: #333; font-weight: 600;"><?= $lang == 'en' ? 'Logout' : 'Đăng xuất' ?></a></li>
                        <?php else: ?>
                            <li><a href="/login.php" style="text-decoration: none; color: #333; font-weight: 600;"><?= $lang == 'en' ? 'Login' : 'Đăng nhập' ?></a></li>
                            <li><a href="/register.php" style="text-decoration: none; background: #f37021; color: #fff; padding: 8px 16px; border-radius: 4px; font-weight: 600;"><?= $lang == 'en' ? 'Apply Now' : 'Ứng tuyển' ?></a></li>
                        <?php endif; ?>
                        <li style="display: flex; align-items: center; gap: 8px; margin-left: 10px;">
                            <a href="?lang=vi"><img src="https://career.fpt.edu.vn/Assets/images/logo-vi.png" alt="VN"></a>
                            <span style="color: #ccc;">|</span>
                            <a href="?lang=en"><img src="https://career.fpt.edu.vn/Assets/images/logo-en.png" alt="EN"></a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</header>
<?php if (isset($_SESSION['flash'])): ?>
  <div class="container mt-3">
    <div class="alert alert-<?= htmlspecialchars($_SESSION['flash']['type']) ?>">
      <?= htmlspecialchars($_SESSION['flash']['message']) ?>
    </div>
  </div>
  <?php unset($_SESSION['flash']); ?>
<?php endif; ?>
<main>
