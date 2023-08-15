
<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>News feeds</title>
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
    if ($php_file != "index.php") {
        $link_name = substr($php_file, 0, -4);
        echo "<p><a href='$php_file'>$link_name</a></p>";
    }
}
?>
</div>
<div style="margin-left: 210px;">
<div class='item'><h2><a href="https://www.cnn.com/2023/04/17/media/dominion-fox-news-allegations/index.html" target="_blank">Here are the 20 specific Fox broadcasts and tweets Dominion says were defamatory</a></h2><div class="description"> Fox-Dominion trial delay 'is not unusual,' judge says. Fox News' defamation battle isn't stopping Trump's election lies. Fox's defamation case against the media network continues to grow in court. Fox has been accused of defamation by Fox News of defaming Fox News.</div><br><span class="date"><strong>Published on:</strong> Mon, 17 Apr 2023 16:01:11 GMT</span><br><div class="category"><strong>Category: </strong><span class="category-text">entertainment</span></div><br><div class="source"><strong>Source: </strong><span class="source-text">CNN</span></div><br><div class="link"><a href="https://www.cnn.com/2023/04/17/media/dominion-fox-news-allegations/index.html" target="_blank">Click here to read the full article</a></div><br></div><hr><div class='item'><h2><a href="https://www.cnn.com/2023/04/18/media/fox-dominion-settlement/index.html" target="_blank">Judge in Fox News-Dominion defamation trial: 'The parties have resolved their case'</a></h2><div class="description"> The judge announced in court that a settlement has been reached in the historic defamation case between Fox News and Dominion Voting Systems. Fox News was sued by Dominion for defamation of its voting software. The judge said the settlement was reached in court in a historic case that was heard in court on Tuesday.</div><br><span class="date"><strong>Published on:</strong> Wed, 19 Apr 2023 08:28:17 GMT</span><br><div class="category"><strong>Category: </strong><span class="category-text">world</span></div><br><div class="source"><strong>Source: </strong><span class="source-text">CNN</span></div><br><div class="link"><a href="https://www.cnn.com/2023/04/18/media/fox-dominion-settlement/index.html" target="_blank">Click here to read the full article</a></div><br></div><hr><div class='item'><h2><a href="https://www.cnn.com/videos/politics/2023/04/18/jake-tapper-dominion-lawsuit-settlement-fox-news-statement-lead-vpx.cnn" target="_blank">'Difficult to say with a straight face': Tapper reacts to Fox News' statement on settlement</a></h2><div class="description"> Fox News will pay more than $787 million to Dominion, a lawyer for the company says. Dominion Voting Systems sued Fox News for defamation. The network will pay the company more than a million dollars in damages, the lawyer says. The judge for the case announced a settlement in the case.</div><br><span class="date"><strong>Published on:</strong> Tue, 18 Apr 2023 21:17:44 GMT</span><br><div class="category"><strong>Category: </strong><span class="category-text">entertainment</span></div><br><div class="source"><strong>Source: </strong><span class="source-text">CNN</span></div><br><div class="link"><a href="https://www.cnn.com/videos/politics/2023/04/18/jake-tapper-dominion-lawsuit-settlement-fox-news-statement-lead-vpx.cnn" target="_blank">Click here to read the full article</a></div><br></div><hr><div class='item'><h2><a href="https://www.cnn.com/2023/04/18/politics/mccarthy-biden-debt-ceiling/index.html" target="_blank">Millions in the US could face massive consequences unless McCarthy can navigate out of a debt trap he set for Biden</a></h2><div class="description"> DeSantis goes to Washington, a place he once despised, looking for support to take on Trump. He once despised the nation's capital, but now he's in Washington, looking to take it on him. He's hoping to win the White House in Florida in 2020.</div><br><span class="date"><strong>Published on:</strong> Tue, 18 Apr 2023 20:34:45 GMT</span><br><div class="category"><strong>Category: </strong><span class="category-text">world</span></div><br><div class="source"><strong>Source: </strong><span class="source-text">CNN</span></div><br><div class="link"><a href="https://www.cnn.com/2023/04/18/politics/mccarthy-biden-debt-ceiling/index.html" target="_blank">Click here to read the full article</a></div><br></div><hr><div class='item'><h2><a href="https://www.cnn.com/2023/04/18/us/kansas-city-ralph-yarl-shooting-tuesday/index.html" target="_blank">White homeowner accused of shooting a Black teen who rang his doorbell turns himself in to face criminal charges</a></h2><div class="description"> 20-year-old woman shot after friend turned into wrong driveway in upstate New York, officials say. 'A major part of Ralph died': Aunt of teen shot after ringing wrong doorbell, aunt says. Woman shot after turning in wrong driveway, police say.</div><br><span class="date"><strong>Published on:</strong> Wed, 19 Apr 2023 04:29:05 GMT</span><br><div class="category"><strong>Category: </strong><span class="category-text">entertainment</span></div><br><div class="source"><strong>Source: </strong><span class="source-text">CNN</span></div><br><div class="link"><a href="https://www.cnn.com/2023/04/18/us/kansas-city-ralph-yarl-shooting-tuesday/index.html" target="_blank">Click here to read the full article</a></div><br></div><hr>
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


