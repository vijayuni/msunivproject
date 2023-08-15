<?php

/*
// Get all PHP files
$files = glob('*.php');

// Skip if there are no PHP files
if(!$files){
    die("No PHP files found");
}

// Sort files by date in filename, descending
usort($files, function($a, $b) {
    // Get the date part from filename and convert to Unix timestamp
    $dateA = strtotime(substr($a, 0, -7));
    $dateB = strtotime(substr($b, 0, -7));

    // Sort in descending order
    return $dateB - $dateA;
});

// Redirect to the PHP file with the latest date in its filename
header('Location: '.$files[0]);

*/

$excludedFiles = ['index.php', 'test.php'];

$files = glob('*.php');

// Filter out excluded files
$filteredFiles = array_diff($files, $excludedFiles);

// Skip if there are no PHP files after filtering
if (empty($filteredFiles)) {
    die("No eligible PHP files found");
}

// Sort files by creation time, descending
usort($filteredFiles, function ($a, $b) {
    $timeA = filectime($a);
    $timeB = filectime($b);
    return $timeB - $timeA;
});

//print $filteredFiles[0];

// Redirect to the latest created PHP file
header('Location: ' . $filteredFiles[0]);


?>
