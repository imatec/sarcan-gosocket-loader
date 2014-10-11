<?php
$user = "6e140fe9-e493-4888-ad4b-cbf0e945aa5d";
$pass = "admin";
$accountId = "3580a591-fad4-4c18-9be3-a9e67488346b";

function getURL($URL, $isJSON = false) {
	global $context;
	$content = file_get_contents($URL, false, $context);
	if ($isJSON)
		return json_decode($content);
	return $content;
}

function getFederations() {
	return getURL("http://api.gosocket.net/api/App/GetFederations?countryId=cl", true);
}

function getSentDocuments($federationId, $accountId, $page) {
	return getURL("http://gosocketapi2.azurewebsites.net/api/App/GetSentDocuments?CountryId=cl&FederationId={$federationId}&AccountId={$accountId}&Page={$page}", true);
}

function getDocumentDetails($documentId) {
	return getURL("http://gosocketapi2.azurewebsites.net/api/App/GetDocumentDetail?CountryId=cl&DocumentId={$documentId}", true);
}

function getDetailXML($documentId) {
	return getURL("http://api.gosocket.net/api/App/GetXml?CountryId=cl&DocumentId={$documentId}", false);
}

function createPath($path) {
	if (!file_exists($path)) mkdir($path, 0777, true);
}
function readStartPage($file) {
	$startPage = 1;
	if (file_exists($file) && $fh = fopen($file, "r")) {
		while (($line = fgets($handle)) !== false) {
			$startPage = (int)$line;
		}
	}
	return $startPage;
}
function writeStartPage($file, $pageNum) {
	file_put_contents($file, $pageNum);
}

// create stream context
$opts = array(
	'http'=>array(
		'method'=>"GET",
		'header' => "Authorization: Basic " . base64_encode("{$user}:{$pass}")
	)
);
$context = stream_context_create($opts);

// create base dir
$basePath = dirname(__FILE__)."/gosocket_downloads2";
createPath($basePath);

// get & save federations
$federations = getFederations();
file_put_contents("{$basePath}/federations.json", json_encode($federations));

foreach ($federations->Items as $federation) {
	
	$federationId = $federation->FederationId;
	echo "{$federationId}\n";
	
	// create federation dir
	$federationPath = "{$basePath}/{$federationId}";
	createPath($federationPath);
	
	// get Federation pages amount
	$pages = getSentDocuments($federationId, $accountId, 1);
	$totalPages = $pages->TotalPages;
	$lastPageFileName = "{$federationPath}/lastpage";
	$startPage = readStartPage($lastPageFileName);

	// iterate pages
	for ($pageNum = $startPage; $pageNum <= $totalPages; $pageNum++) {
		// create page dir
		$pagePath = "{$federationPath}/p{$pageNum}";
		createPath($pagePath);
		
		// iterate over documents of a federation
		echo "iterating page {$pageNum}\n";
		
		// get & save page
		$page = getSentDocuments($federationId, $accountId, $pageNum);
		file_put_contents("{$federationPath}/federation_p{$pageNum}_{$federationId}.json", json_encode($page));
		
		foreach ($page->Items as $item) {
			
			$documentId = $item->DocumentId;
			echo " > {$documentId} \n";
			$documentPath = "{$pagePath}/{$documentId}";
			createPath($documentPath);
			
			// iterate over details of a document
			$detail = getDocumentDetails($documentId);
			file_put_contents("{$documentPath}/documentDetail_{$documentId}.json", json_encode($detail));
			
			// copy detail XML
			$detailXML = getDetailXML($documentId);
			$detailXML = base64_decode($detailXML);
			file_put_contents("{$documentPath}/xml_{$documentId}.xml", json_encode($detailXML));
		}
		writeStartPage($lastPageFileName, $pageNum);
	}
}
//print_r($federations);
//print($file);

?>
