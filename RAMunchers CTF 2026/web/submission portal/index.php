<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Coursework Submission Portal</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 640px; margin: 60px auto; padding: 24px; color: #222; }
    h1 { margin-bottom: 4px; }
    .sub { color: #666; margin-bottom: 32px; }
    form { padding: 24px; border: 1px solid #ddd; border-radius: 6px; background: #fafafa; }
    input[type=file] { margin: 12px 0 20px 0; }
    input[type=submit] { padding: 8px 20px; background: #2c5282; color: white; border: 0; border-radius: 4px; cursor: pointer; }
    input[type=submit]:hover { background: #2a4a78; }
    .note { margin-top: 24px; font-size: 0.9em; color: #666; }
  </style>
</head>
<body>
  <h1>Coursework Submission Portal</h1>
  <p class="sub">Upload a screenshot of your assignment for grading.</p>

  <form action="upload.php" method="post" enctype="multipart/form-data">
    <label for="fileToUpload"><strong>Choose image:</strong></label><br>
    <input type="file" name="fileToUpload" id="fileToUpload" required>
    <br>
    <input type="submit" value="Submit" name="submit">
  </form>

  <p class="note">Accepted formats: JPG, PNG, GIF. Max size: 500&nbsp;KB.<br></p>
</body>
</html>
