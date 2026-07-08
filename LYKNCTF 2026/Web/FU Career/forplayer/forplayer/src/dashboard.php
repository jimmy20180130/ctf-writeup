<?php
require_once 'config.php';
require_login();

$user = current_user();
if ($user['role'] === 'admin') {
    header("Location: admin.php");
    exit;
}

$notes_result = mysqli_query($conn, "SELECT * FROM internal_notes WHERE visibility = 'user'");
$cvs_result = mysqli_query($conn, "SELECT * FROM cv_submissions WHERE user_id = {$user['id']} ORDER BY created_at DESC");

require_once 'header.php';
?>

<section class="dashboard">
  <div class="section-head row-between">
    <div>
      <p class="eyebrow"><?= $lang=='en' ? 'Candidate' : 'Ứng viên' ?></p>
      <h1><?= $lang=='en' ? 'Hello, ' : 'Xin chào, ' ?><?= htmlspecialchars($user['full_name']) ?></h1>
    </div>
    <span class="pill"><?= htmlspecialchars($user['department']) ?></span>
  </div>

  <div class="dash-grid">
    <section class="panel">
      <h2>📄 Upload CV</h2>
      <form class="stack-form" method="post" action="upload.php" enctype="multipart/form-data">
        <label><?= $lang=='en' ? 'Candidate Name' : 'Họ tên ứng viên' ?><input name="candidate_name" value="<?= htmlspecialchars($user['full_name']) ?>" placeholder="<?= $lang=='en' ? 'Enter your name' : 'Nhập họ tên' ?>"></label>
        <label><?= $lang=='en' ? 'Position' : 'Vị trí ứng tuyển' ?>
          <select name="position">
            <option><?= $lang=='en' ? 'Information Security Lecturer' : 'Giảng viên An toàn thông tin' ?></option>
            <option><?= $lang=='en' ? 'IT Lecturer' : 'Giảng viên Công nghệ thông tin' ?></option>
            <option><?= $lang=='en' ? 'Admissions Officer' : 'Cán bộ Tuyển sinh' ?></option>
            <option><?= $lang=='en' ? 'English Teacher' : 'Giáo viên Tiếng Anh' ?></option>
            <option><?= $lang=='en' ? 'HR Specialist' : 'Chuyên viên Nhân sự' ?></option>
            <option><?= $lang=='en' ? 'Marketing Officer' : 'Cán bộ Marketing' ?></option>
            <option><?= $lang=='en' ? 'IT Teacher' : 'Giáo viên Tin học' ?></option>
          </select>
        </label>
        <label><?= $lang=='en' ? 'Short Bio' : 'Giới thiệu ngắn' ?><textarea name="cover_letter" rows="4" placeholder="<?= $lang=='en' ? 'Write a few lines about yourself...' : 'Viết vài dòng giới thiệu bản thân...' ?>"></textarea></label>
        <label><?= $lang=='en' ? 'CV File (txt, pdf, doc, docx)' : 'File CV (txt, pdf, doc, docx)' ?><input type="file" name="cv" accept=".txt,.pdf,.doc,.docx" required></label>
        <button class="button" type="submit"><?= $lang=='en' ? 'Submit CV' : 'Gửi CV' ?></button>
      </form>
    </section>

    <section class="panel">
      <h2>📋 <?= $lang=='en' ? 'Internal Notices' : 'Thông báo nội bộ' ?></h2>
      <div class="note-list">
        <?php if (mysqli_num_rows($notes_result) > 0): ?>
          <?php while ($note = mysqli_fetch_assoc($notes_result)): ?>
            <article>
              <h3><?= htmlspecialchars($note['title']) ?></h3>
              <p><?= htmlspecialchars($note['body']) ?></p>
            </article>
          <?php endwhile; ?>
        <?php else: ?>
          <p class="muted"><?= $lang=='en' ? 'No notices yet.' : 'Chưa có thông báo nào.' ?></p>
        <?php endif; ?>
      </div>
    </section>
  </div>

  <section class="panel wide">
    <h2>📑 <?= $lang=='en' ? 'Submitted CVs' : 'CV đã gửi' ?></h2>
    <table>
      <thead><tr><th>ID</th><th><?= $lang=='en' ? 'Position' : 'Vị trí' ?></th><th><?= $lang=='en' ? 'File' : 'File' ?></th><th><?= $lang=='en' ? 'Status' : 'Trạng thái' ?></th></tr></thead>
      <tbody>
        <?php if (mysqli_num_rows($cvs_result) > 0): ?>
          <?php while ($cv = mysqli_fetch_assoc($cvs_result)): ?>
            <tr>
              <td><?= htmlspecialchars($cv['id']) ?></td>
              <td><?= htmlspecialchars($cv['position']) ?></td>
              <td><?= htmlspecialchars($cv['original_filename']) ?></td>
              <td><span class="pill"><?= htmlspecialchars($cv['status']) ?></span></td>
            </tr>
          <?php endwhile; ?>
        <?php else: ?>
          <tr><td colspan="4" class="muted" style="text-align:center;"><?= $lang=='en' ? 'No CVs submitted yet.' : 'Chưa có CV nào.' ?></td></tr>
        <?php endif; ?>
      </tbody>
    </table>
  </section>
</section>

<?php require_once 'footer.php'; ?>
