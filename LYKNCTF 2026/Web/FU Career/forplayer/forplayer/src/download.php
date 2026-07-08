<?php
require_once 'config.php';
require_admin();

$file = $_GET['file'] ?? '';
if (empty($file) || strpos($file, '/') !== false || strpos($file, '\\') !== false) {
    header("HTTP/1.0 404 Not Found");
    exit;
}

$path = __DIR__ . '/uploads/' . $file;
if (file_exists($path)) {
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="'.basename($path).'"');
    header('Expires: 0');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    header('Content-Length: ' . filesize($path));
    readfile($path);
    exit;
} else {
    header("HTTP/1.0 404 Not Found");
    exit;
}
?>
