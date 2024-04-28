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
header('Access-Control-Allow-Origin: https://www.artikelschreiber.com/, https://artikelschreiber.com/');
ini_set('memory_limit','3512M');
ini_set('max_execution_time', 3000);

require_once("/home/www/wwwartikelschreiber/libraryv3/Logging.inc.php"); 
$myLogs 	= new Logging();
$myLogs->logURL();
$base_dir 	= __DIR__;
$list 		= explode("/",$_SERVER["SCRIPT_FILENAME"]);
$language 	= $list[4];
$path 		= pathinfo($_SERVER["SCRIPT_FILENAME"]);
$files 		= scandir($path["dirname"]);
$url 		= "https://www.artikelschreiber.com".$_SERVER["REQUEST_URI"];

$lan 		= array("de","en","fr","es","it","ru","pt","sa","in","jp","cn","tr");
$array_additional	= array();

for ($a=0; $a<count($lan); $a++){
	$myLanguage = $lan[$a];
	if ($myLanguage =='de'){
		array_push($array_additional,"https://www.artikelschreiber.com/");
		array_push($array_additional,"https://www.artikelschreiber.com/de/blog/");
		array_push($array_additional,"https://www.artikelschreiber.com/marketing/");
	} else{
		array_push($array_additional,"https://www.artikelschreiber.com/$myLanguage/");
		array_push($array_additional,"https://www.artikelschreiber.com/$myLanguage/blog/");
	}
} // foreach ($random_keys as $key => $value) {

shuffle($files);
header("Content-Type: application/rss+xml; charset=UTF-8");

echo "<?xml version='1.0' encoding='UTF-8'?>
<rss version='2.0'>
<channel>
<title>RSS Feed $language | Artikelschreiber.com</title>
<link>https://www.artikelschreiber.com/</link>
<description>Artikelschreiber.com RSS</description>
<copyright>Copyright (C) 2022 Artikelschreiber.com</copyright>
<language>$language-$language</language>";
 
for ($i=0; $i<25; $i++){
	$fname = $files[$i];
	if (strlen($fname) > 3){
		$title 	= str_replace("-"," ", $fname);
		$title 	= str_replace(".html","", $title);
		//$title	= preg_replace('/&(?!#?[a-z0-9]+;)/', '&amp;', $title);
		$title = htmlspecialchars($title);
		$link = "https://www.artikelschreiber.com/$language/blog/$fname";
		$myDate = date("D, d M Y H:i:s O", time());
echo "<item>
<title>$title</title>
<link>$link</link>
<guid>$link</guid>
<description>Article and Text: $title</description>
<pubDate>$myDate</pubDate>
</item>";
	} // if (strlen($fname) > 3){
} // for ($i=0; $i<25; $i++){
	
for ($i=0; $i<count($array_additional); $i++){
	$fname = $array_additional[$i];
	if (strlen($fname) > 3){
		$title 	= $fname; //str_replace("-"," ", $fname);
		$title 	= str_replace(".html","", $title);
		//$title	= preg_replace('/&(?!#?[a-z0-9]+;)/', '&amp;', $title);
		$title = htmlspecialchars($title);
		$link = $fname; //"https://www.artikelschreiber.com/$language/blog/$fname";
		$myDate = date("D, d M Y H:i:s O", time());
echo "<item>
<title>$title</title>
<link>$link</link>
<guid>$link</guid>
<description>Article and Text: $title</description>
<pubDate>$myDate</pubDate>
</item>";
	} // if (strlen($fname) > 3){
} // for ($i=0; $i<25; $i++){
	
echo "</channel></rss>";
exit(0);
?>