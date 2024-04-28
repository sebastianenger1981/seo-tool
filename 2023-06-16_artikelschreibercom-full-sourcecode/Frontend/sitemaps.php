<?php
/*
Copyright (c) 2023, Sebastian Enger, M.Sc.
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree (BSD-4-Clause). 

Frontend and Backend Source Code for Project:
- https://www.artikelschreiber.com/
- https://www.artikelschreiben.com/
- https://www.unaique.net/
*/
ini_set('memory_limit','8512M');
ini_set('max_execution_time', 31000);
ini_set('display_errors', 0);

require_once("/home/www/wwwartikelschreiber/libraryv3/Language.inc.php");
require_once("/home/www/wwwartikelschreiber/libraryv3/Logging.inc.php"); 
require_once("/home/www/wwwartikelschreiber/libraryv3/Functions.inc.php");
require_once("/home/www/wwwartikelschreiber/libraryv3/Security.inc.php");
$dom 				= new DOMDocument();
$Lang				= new Language();
$Func				= new Functions();
$Secu				= new Security();
$myLogs 			= new Logging();
$myLogs->logURL();

$seconds_to_cache = 72000;
$ts = gmdate("D, d M Y H:i:s", time() + $seconds_to_cache) . " GMT";

//header("Content-type: text/html; charset=utf-8");
header("Content-type: text/xml; charset=utf-8");
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");
header('X-UA-Compatible: IE=edge,chrome=1');
header('X-XSS-Protection: 1; mode=block');
header('X-Frame-Options: DENY');
header('X-Content-Type-Options: nosniff');

//create your XML document, using the namespaces
$urlset = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" /><!--?xml version="1.0" encoding="UTF-8"?-->');

$max_count 			= 50000;
$max_counterfl		= 0;
$blog_path 						= "/home/www/wwwartikelschreiber/texts/";
$files 							= scandir($blog_path);
for ($y=0; $y<count($files) - 1; $y++){
//for ($y=0; $y<$max_count; $y++){
	$myfinfile 					= $blog_path."/".$files[$y];
	//echo $files[$y] . "<br>"; 
	//echo stripos($files[$y], '.html') . "<br>"; 
		
	if (strlen($files[$y]) > 10 and stripos($files[$y], '.html') !== false){
		$contains_sum 			= array();
		//echo " IN " .$myfinfile . "<br>"; 
		if($dom->loadHTMLFile($myfinfile)) { // https://stackoverflow.com/questions/399332/fastest-way-to-retrieve-a-title-in-php
			$list 				= $dom->getElementsByTagName("span"); #title
			$contains_sum 		= array();
			for ($x=0; $x<$list->length - 1; $x++){
				$text 			= $list->item($x)->textContent;
				$isBadEntry 	= $Func->isBadBlogContent($text);
				array_push($contains_sum, $isBadEntry);
			} // for ($x=0; $x<$list->length - 1; $x++){
		}; // if($dom->loadHTMLFile($myfinfile)) {
		
		if (array_sum($contains_sum) < 2){ // weniger als 2 Stopwort Listen Einträge bei ca. 16 <span></span> Content einträgen bei tplv3/index_show_en.tpl
			//if($dom->loadHTMLFile($myfinfile)) { 
			//$list_title		= $dom->getElementsByTagName("title"); #title
			//$title 			= $list_title->item(0)->textContent;
			$myfinurl 			= $url.$files[$y];
			if ($Func->endsWith($myfinurl,".html")){
				//if (strlen($title) > 7 and $Func->endsWith($myfinurl,".html")){
				//$title 			= $Secu->sanitizeForJsonOption($title);
				//$title 			= preg_replace('/[\x00-\x1F\x80-\xFF]/', '', $title);
				if ( $max_counterfl < $max_count){
					$url = $urlset->addChild('url');
					$url->addChild('loc',"https://www.artikelschreiber.com/texts/$myfinurl" );
					$url->addChild('lastmod', date("Y-m-d", filemtime($myfinfile)) );
					$url->addChild('changefreq', 'yearly');  //weekly etc.
					$url->addChild('priority', "0.44");
					$max_counterfl++;
				}; // if ( $max_counterfl < $max_count){
			}; // if ($Func->endsWith($myfinurl,".html")){
			//}; // if($dom->loadHTMLFile($myfinfile)) { 
		};// if (array_sum($contains_sum) < 2){
		$contains_sum 				= array();
	}; // if (strlen($files[$y]) > 10 stripos($files[$y], '.php') !== True){
}; //for ($y=0; $iy<count($files) - 1; $y++){



$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/texts/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'daily');  //weekly etc.
$url->addChild('priority', "0.85");

$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/texts/feed.php" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'daily');  //weekly etc.
$url->addChild('priority', "0.75");


//add whitespaces to xml output (optional, of course)
$dom = new DomDocument();
$dom->loadXML($urlset->asXML());
$dom->formatOutput = true;
//output xml
echo $dom->saveXML();
exit(0);
?>