<?php

$excludedFiles = ['index.php', 'test.php'];

$files = glob('*.php');

$filteredFiles = array_diff($files, $excludedFiles);

if (empty($filteredFiles)) {
    die("No eligible PHP files found");
}

usort($filteredFiles, function ($a, $b) {
    $timeA = filectime($a);
    $timeB = filectime($b);
    return $timeB - $timeA;
});

header('Location: ' . $filteredFiles[0]);

?>