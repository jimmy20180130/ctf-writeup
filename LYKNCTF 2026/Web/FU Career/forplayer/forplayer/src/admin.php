<?php
require_once 'config.php';
require_admin();

$user = current_user();
$notes_result = mysqli_query($conn, "SELECT * FROM internal_notes WHERE visibility = 'admin'");
$cvs_result = mysqli_query($conn, "SELECT cv_submissions.*, users.username, users.email FROM cv_submissions JOIN users ON users.id = cv_submissions.user_id ORDER BY cv_submissions.created_at DESC");

require_once 'header.php';
?>

<section class="dashboard">
  <div class="section-head row-between">
    <div>
      <p class="eyebrow">Admin Console</p>
      <h1><?= $lang == 'en' ? 'Candidate CV Management' : 'Quản lý CV ứng viên' ?></h1>
      <h2>part1: LYKN{fake_flag_part_1</h2>
    </div>
    <span class="pill danger">HR Admin</span>
  </div>

  <div class="dash-grid">
    <section class="panel">
      <h2><?= $lang == 'en' ? '📝 Operational Notes' : '📝 Ghi chú vận hành' ?></h2>
      <div class="note-list">
        <?php if (mysqli_num_rows($notes_result) > 0): ?>
          <?php while ($note = mysqli_fetch_assoc($notes_result)): ?>
            <article>
              <h3><?= htmlspecialchars($note['title']) ?></h3>
              <p><?= htmlspecialchars($note['body']) ?></p>
            </article>
          <?php endwhile; ?>
        <?php else: ?>
          <p class="muted"><?= $lang == 'en' ? 'No notes.' : 'Không có ghi chú.' ?></p>
        <?php endif; ?>
      </div>
    </section>

    <section class="panel">
      <h2>🔍 <?= $lang == 'en' ? 'Quick Preview' : 'Preview nhanh' ?></h2>
      <p class="muted" style="margin-bottom:12px; font-size:.88rem;">
        <?= $lang == 'en' ? 'Enter CV ID to preview content via internal pipeline.' : 'Nhập CV ID để xem nội dung qua pipeline preview nội bộ.' ?>
      </p>
      <form class="stack-form" method="post" action="preview.php">
        <label>CV ID<input name="cv_id" value="1" placeholder="<?= $lang == 'en' ? 'Enter ID' : 'Nhập ID' ?>"
            required></label>
        <button class="button" type="submit"><?= $lang == 'en' ? 'View CV' : 'Xem CV' ?></button>
      </form>
    </section>
  </div>

  <section class="panel wide">
    <h2>📑 <?= $lang == 'en' ? 'CV List' : 'Danh sách CV' ?></h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th><?= $lang == 'en' ? 'Candidate' : 'Ứng viên' ?></th>
          <th>Username</th>
          <th><?= $lang == 'en' ? 'Position' : 'Vị trí' ?></th>
          <th><?= $lang == 'en' ? 'File' : 'File' ?></th>
          <th><?= $lang == 'en' ? 'Status' : 'Trạng thái' ?></th>
        </tr>
      </thead>
      <tbody>
        <?php if (mysqli_num_rows($cvs_result) > 0): ?>
          <?php while ($cv = mysqli_fetch_assoc($cvs_result)): ?>
            <tr>
              <td><?= htmlspecialchars($cv['id']) ?></td>
              <td><?= htmlspecialchars($cv['candidate_name']) ?></td>
              <td><?= htmlspecialchars($cv['username']) ?></td>
              <td><?= htmlspecialchars($cv['position']) ?></td>
              <td><a href="/uploads/<?= htmlspecialchars($cv['stored_filename']) ?>"
                  style="color:var(--fpt-orange); font-weight:600;"><?= htmlspecialchars($cv['original_filename']) ?></a>
              </td>
              <td><span class="pill"><?= htmlspecialchars($cv['status']) ?></span></td>
            </tr>
          <?php endwhile; ?>
        <?php else: ?>
          <tr>
            <td colspan="6" class="muted" style="text-align:center;">
              <?= $lang == 'en' ? 'No CVs yet.' : 'Không có CV nào.' ?></td>
          </tr>
        <?php endif; ?>
      </tbody>
    </table>
  </section>
</section>

<?php require_once 'footer.php'; ?>