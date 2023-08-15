php_template = """
<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>News feeds</title>
<style>.item {max-width: 800px; margin: 0 auto; } .sidebar { position: fixed; width: 200px; height: 100%; overflow: auto; padding: 0.5em; } .sidebar a {color: #000; text-decoration: none; } .sidebar {position: fixed; width: 200px; height: 100%; overflow: auto; padding: 0.5em; border-right: 1px solid #000; } body { padding: 0; margin: 0; } .sidebar p {margin: 0; padding: 15px 0; } body > div > a { max-width: 800px; margin: 0 auto; display: block; padding-top: 20px; } .item a {color: #000;} </style>
</head>
<body>
<?php
$php_files = glob("*.php");
?>
<div class="sidebar">
<h3>Dates</h3>
<?php
foreach ($php_files as $php_file) {
    $link_name = substr($php_file, 0, -4);
    echo "<p><a href='$php_file'>$link_name</a></p>";
}
?>
</div>
<div style="margin-left: 210px;">
[news_items]
</div>


</body>
</html>


"""