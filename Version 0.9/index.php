<?php
session_start();

?>

<!DOCTYPE html>
<html>
   <head>
     <title>Yesterday's News</title>
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
         <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.3/css/materialize.min.css">
         <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
         <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.3/js/materialize.min.js"></script>
      <style>
         div {
               width : 200px;
               height : 200px;
            }
      </style>
   </head>
   <body class="container">
      <h2>Yesterday's News</h2>
	  
		<p>I am working on an experimental project that summarizes and gives the headings from different RSS feeds. I aim to provide a quick overview of the latest headlines and developments, automatically generated every day at 12:00 AM GMT.</p>
		<p><strong>Note: </strong> This is an ongoing experimental project, and as such, the summarization process may have occasional imperfections or omissions.</p>
		
		<p><strong>Note: </strong> To access the news, simply click on the date corresponding to the file creation. The file format includes the date and hour of its creation<p>
      <br/>
      <table>
      <thead>
         <tr><th>S.No</th><th>Date</th></tr>
      </thead>
	  <tbody>
		<?php
			date_default_timezone_set('Europe/London');
			
			$dirArray = glob("files/*.{PHP,php}",GLOB_BRACE);

			//	count elements in array
			$indexCount	= count($dirArray);
			// sort 'em
			sort($dirArray);
			$location = "http://localhost:8080/";

			for($index=0; $index < $indexCount; $index++) {
			  $filename = $dirArray[$index];
			  $url = str_replace(' ', '%20', $filename);
			  $date = substr($filename, 0, strrpos($filename, ' '));
			  $date = str_replace ('files/', '', $date);
			  $hours = substr($filename, strrpos($filename, ' ') + 1, 2);
			  $new_filename = date('d-m-Y', strtotime($date)) . " " . $hours . " Hours";
			  
			  ?>
				  
				<tr><td><?php echo($index + 1); ?></td><td><a href=<?php echo("$url"); ?>><?php echo($new_filename); ?></a></td></tr>
				
		<?php } ?>

      </tbody>
		 
      </table>
   </body>
</html>