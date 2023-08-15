php_template = """
<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Yesterday's News</title>
<style>.item {max-width: 800px; margin: 0 auto; } .sidebar { position: fixed; width: 200px; height: 100%; overflow: auto; padding: 0.5em; } .sidebar a {color: #000; text-decoration: none; } .sidebar {position: fixed; width: 200px; height: 100%; overflow: auto; padding: 0.5em; border-right: 1px solid #000; } body { padding: 0; margin: 0; } .sidebar p {margin: 0; padding: 15px 0; } body > div > a { max-width: 800px; margin: 0 auto; display: block; padding-top: 20px; } .item a {color: #000;} select#categories {margin: 0 auto; display: block;} span.category-text {text-transform: capitalize;} select#categories {text-transform: capitalize; font-size: 17px; margin-top: 10px; padding: 5px 20px;}</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
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

<script>
$(document).ready(function () {
  var categories = ["All"];
  $(".item .category-text").each(function () {
    var category = $(this).text();
    if (!categories.includes(category)) {
      categories.push(category);
    }
  });

  // Display all categories in dropdown
  var select = $("<select id='categories' />");
  $.each(categories, function(i, val) {
    select.append($("<option/>", {
      value: val,
      text : val 
    }));
  });

  select.insertBefore('.item:first'); // assuming we want it above the items
});

$(document).on('change', '#categories', function() {
  var selectedCategory = $(this).val();

  if (selectedCategory === 'All') {
    $('.item').show();
    $('.item').next('hr').show(); // show the <hr> elements
  } else {
    $('.item').each(function() {
      var itemCategory = $(this).find('.category-text').text();
      if (itemCategory === selectedCategory) {
        $(this).show();
        $(this).next('hr').show(); // show the <hr> element following the visible item
      } else {
        $(this).hide();
        $(this).next('hr').hide(); // hide the <hr> element following the hidden item
      }
    });
  }
});
</script>

</html>


"""