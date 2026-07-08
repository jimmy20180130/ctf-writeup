<?php require_once 'header.php'; ?>
<?php
if (isset($lang) && $lang == 'en') {
    require 'index_en.php';
} else {
    require 'index_vi.php';
}
?>
<?php require_once 'footer.php'; ?>
