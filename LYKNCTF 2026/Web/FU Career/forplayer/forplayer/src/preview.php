<?php
require_once 'config.php';
require_admin();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // VULNERABILITY: Raw input used in query -> SQLi
    $cv_id = $_POST['cv_id'] ?? '';
    
    // Allows UNION-based SQL injection including INTO OUTFILE
    $query = "SELECT * FROM cv_submissions WHERE id = $cv_id";
    $result = @mysqli_query($conn, $query);
    
    if (!$result) {
        $_SESSION['flash'] = ['type' => 'danger', 'message' => 'Lỗi query preview: ' . mysqli_error($conn)];
        header("Location: admin.php");
        exit;
    }
    
    $cv = mysqli_fetch_assoc($result);
    if (!$cv) {
        $_SESSION['flash'] = ['type' => 'warning', 'message' => 'Không tìm thấy CV.'];
        header("Location: admin.php");
        exit;
    }
    
    // In PHP version, we just output the CV contents or a simulation of the preview pipeline
    $cv_path = __DIR__ . '/uploads/' . $cv['stored_filename'];
    if (file_exists($cv_path)) {
        $output = htmlspecialchars(file_get_contents($cv_path));
    } else {
        $output = "File không tồn tại.";
    }
} else {
    header("Location: admin.php");
    exit;
}

require_once 'header.php';
?>

<section class="dashboard">
  <div class="section-head row-between">
    <div>
      <p class="eyebrow">Preview Pipeline</p>
      <h1><?= htmlspecialchars($cv['candidate_name'] ?? 'Unknown') ?></h1>
    </div>
    <a class="button ghost" href="admin.php">← Quay lại</a>
  </div>
  <section class="panel wide">
    <dl class="meta">
      <dt>Vị trí</dt><dd><?= htmlspecialchars($cv['position'] ?? 'Unknown') ?></dd>
      <dt>File</dt><dd><?= htmlspecialchars($cv['original_filename'] ?? 'Unknown') ?></dd>
      <dt>Trạng thái</dt><dd><span class="pill"><?= htmlspecialchars($cv['status'] ?? 'Unknown') ?></span></dd>
    </dl>
    <div class="preview-note">Hệ thống tuyển dụng đã tạo bản xem trước nội bộ.</div>
    <pre class="terminal"><?= $output ?></pre>
  </section>
</section>

<?php require_once 'footer.php'; ?>
