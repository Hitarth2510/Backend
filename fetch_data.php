<?php
// fetch_data.php

header('Content-Type: application/json');

// MongoDB connection details
$mongoUri = 'mongodb://localhost:27017'; // Adjust as needed
$databaseName = 'gunshot_db'; // Replace with your database name
$collectionName = 'gunshot_data'; // Replace with your collection name

try {
    // Create a MongoDB client instance
    $client = new MongoDB\Client($mongoUri);
    $collection = $client->selectCollection($databaseName, $collectionName);
    
    // Fetch the latest document from the collection
    $latestData = $collection->findOne([], ['sort' => ['timestamp' => -1]]);
    
    // Prepare the data for JSON output
    $response = [
        'timestamp' => $latestData->timestamp,
        'direction' => $latestData->direction
    ];
    
    // Output the JSON data
    echo json_encode($response);

} catch (Exception $e) {
    // Handle any errors and output an error message
    echo json_encode(['error' => 'Unable to fetch data: ' . $e->getMessage()]);
}
?>
