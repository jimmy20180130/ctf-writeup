<?php
$target_dir = "submissions/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));
$msg = "No Form Submission";
$msg_type = "alert-danger";

// Check if image file is a actual image or fake image
if (isset($_POST["submit"])) {

    // --- PATCH 1: extension whitelist ---
    // Stops attackers naming their file shell.php / shell.phtml / shell.phar etc.
    // Magic-byte polyglots with .php extension get rejected here.
    $allowed_ext = ["jpg", "jpeg", "png", "gif"];
    if (!in_array($imageFileType, $allowed_ext, true)) {
        $msg = "<p>Only JPG, JPEG, PNG, and GIF files are allowed.</p>";
        $msg_type = "alert-warning";
        $uploadOk = 0;
    } else {
        $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
        if ($check === false) {
            $msg = "<p>File is not an image.</p>";
            $msg_type = "alert-warning";
            $uploadOk = 0;
        } else {
            // --- PATCH 2: strict MIME check ---
            $allowed_mimes = ["image/jpeg", "image/png", "image/gif"];
            if (!in_array($check["mime"], $allowed_mimes, true)) {
                $msg = "<p>Invalid image MIME type.</p>";
                $msg_type = "alert-warning";
                $uploadOk = 0;
            } else {
                // --- PATCH 3: re-encode through GD ---
                // Strips EXIF / comment / appended data. Defeats the
                // exiftool -Comment='<' . '?php ...' polyglot trick.
                $tmp = $_FILES["fileToUpload"]["tmp_name"];
                $img = false;
                switch ($check["mime"]) {
                    case "image/jpeg":
                        $img = @imagecreatefromjpeg($tmp);
                        if ($img !== false) { imagejpeg($img, $tmp, 90); }
                        break;
                    case "image/png":
                        $img = @imagecreatefrompng($tmp);
                        if ($img !== false) { imagepng($img, $tmp); }
                        break;
                    case "image/gif":
                        $img = @imagecreatefromgif($tmp);
                        if ($img !== false) { imagegif($img, $tmp); }
                        break;
                }
                if ($img === false) {
                    $msg = "<p>Image processing failed.</p>";
                    $msg_type = "alert-warning";
                    $uploadOk = 0;
                } else {
                    imagedestroy($img);
                    $msg = "<p>File is an image - " . $check["mime"] . ".</p>";
                    $msg_type = "alert-success";
                    $uploadOk = 1;
                }
            }
        }
    }
}

// Check if file already exists
if (file_exists($target_file)) {
    $msg = "Sorry, file already exists.";
    $msg_type = "alert-warning";
    $uploadOk = 0;
}

// Check file size
if ($_FILES["fileToUpload"]["size"] > 500000) {
    $msg = "Sorry, your file is too large.";
    $msg_type = "alert-warning";
    $uploadOk = 0;
}

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    $msg = $msg . "<p>Sorry, your file was not uploaded.</p>";
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        $msg = "<p>The file " . htmlspecialchars(basename($_FILES["fileToUpload"]["name"])) . " has been uploaded.</p>";
        $msg_type = "alert-success";
    } else {
        $msg = "Sorry, there was an error uploading your file.";
        $msg_type = "alert-danger";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Upload Result</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 640px; margin: 60px auto; padding: 24px; color: #222; }
    .alert { padding: 14px 18px; border-radius: 4px; margin: 16px 0; }
    .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .alert-warning { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    .alert-danger  { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    a { color: #2c5282; }
  </style>
</head>
<body>
  <h1>Upload Result</h1>
  <div class="alert <?= htmlspecialchars($msg_type) ?>"><?= $msg ?></div>
  <p><a href="index.php">&larr; Back to upload</a></p>
</body>
</html>
