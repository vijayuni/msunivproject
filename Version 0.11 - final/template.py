php_template = """
<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>News feeds</title>
<style>.item {max-width: 800px; margin: 0 auto; } .sidebar { position: fixed; width: 200px; height: 100%; overflow: auto; padding: 0.5em; } .sidebar a {color: #000; text-decoration: none; } .sidebar { position: fixed; width: 200px; height: 100%; overflow: auto; padding: 0.5em; border-right: 1px solid #000; } body { padding: 0; margin: 0; } .sidebar p {margin: 0; padding: 15px 0; } body > div > a { max-width: 800px; margin: 0 auto; display: block; padding-top: 20px; } .item a {color: #000;} select#categories {margin: 0 auto; display: block;} span.category-text {text-transform: capitalize;} select#categories {text-transform: capitalize; font-size: 17px; margin-top: 10px; padding: 5px 20px; display: inline-block;} .sidebar a.active {font-weight: bold;color: red;} .filter-container {margin: 0 auto; max-width: 250px;}</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
<?php
/*$php_files = glob("*.php");*/
?>
<div class="sidebar">
<h3>Dates</h3>
<?php
/*foreach ($php_files as $php_file) {
    if ($php_file != "index.php") {
        $link_name = substr($php_file, 0, -4);
        echo "<p><a href='$php_file'>$link_name</a></p>";
    }
} */

$php_files = scandir(__DIR__);

$php_files = array_filter($php_files, function($file) {
    return pathinfo($file, PATHINFO_EXTENSION) === 'php' && $file !== 'index.php';
});

usort($php_files, function($a, $b) {
    return filemtime($b) - filemtime($a);
});

foreach ($php_files as $php_file) {
    $link_name = substr($php_file, 0, -4);
    //echo "<p><a href='$php_file'>$link_name</a></p>";
    $is_active = basename($_SERVER['PHP_SELF']) === $php_file;
    echo "<p><a href='$php_file' " . ($is_active ? "class='active'" : "") . ">$link_name</a></p>";

}
?>
</div>
<div style="margin-left: 210px;">
[news_items]
</div>


</body>

<script>
$(document).ready(function () {
  var categories = ["All"];
  $(".item .category-text").each(function () {
    var category = $(this).text();
    if (!categories.includes(category)) {
      categories.push(category);
    }
  });

  var select = $("<select id='categories' />");
  $.each(categories, function(i, val) {
    select.append($("<option/>", {
      value: val,
      text : val 
    }));
  });

  var label = $("<label />").text('Filter: ');
  var parentDiv = $("<div class='filter-container' />");
  
  parentDiv.append(label).append(select);
  parentDiv.insertBefore('.item:first');  
});

$(document).on('change', '#categories', function() {
  var selectedCategory = $(this).val();

  if (selectedCategory === 'All') {
    $('.item').show();
    $('.item').next('hr').show();
  } else {
    $('.item').each(function() {
      var itemCategory = $(this).find('.category-text').text();
      if (itemCategory === selectedCategory) {
        $(this).show();
        $(this).next('hr').show();
      } else {
        $(this).hide();
        $(this).next('hr').hide();
      }
    });
  }
});
</script>

</html>


"""