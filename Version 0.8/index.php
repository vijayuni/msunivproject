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