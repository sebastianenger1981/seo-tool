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
#ini_set('display_errors', 0);
#error_reporting(E_ALL);
#ini_set('display_errors', 1);

/*
//var_dump($_SERVER['HTTP_HOST']);
if (strpos($_SERVER['HTTP_HOST'], "www") === false){
	header("HTTP/1.1 301 Moved Permanently");
	header("Location: https://www.artikelschreiber.com/");
	header("Connection: close");
	exit(0);
} // if (strpos($_SERVER['HTTP_HOST'], "www") === false){
*/

// https://securityheaders.com/?q=https%3A%2F%2Fwww.artikelschreiber.com%2F&hide=on&followRedirects=on

// Get last modification time of the current PHP file
$file_last_mod_time 	= filemtime(__FILE__);

// Get last modification time of the main content (that user sees)
$content_last_mod_time 	= 1636651199;	# STATIC, am 2021-11-11 zuletzt bearbeitet

// Combine both to generate a unique ETag for a unique content
// Specification says ETag should be specified within double quotes
$etag 					= '"' . $file_last_mod_time . '.' . $content_last_mod_time . '"';

// Last Modified Senden
$gmt_mtime 				= gmdate('D, d M Y H:i:s', $content_last_mod_time ) . ' GMT';

$seconds_to_cache 		= 2764800; // 32 Tage
$ts 					= gmdate("D, d M Y H:i:s", time() + $seconds_to_cache) . " GMT";

header('Link: <https://www.artikelschreiber.com/en/>; rel="canonical"');
header("Pragma: cache");
header("Cache-Control: public, max-age=$seconds_to_cache, pre-check=$seconds_to_cache, s-maxage=$seconds_to_cache");
header("Content-Type: text/html; charset=UTF-8");
header("Expires: $ts");
header("X-UA-Compatible: IE=edge,chrome=1");
header("Last-Modified: " . $gmt_mtime );
header('ETag: ' . $etag);

// Check whether browser had sent a HTTP_IF_NONE_MATCH request header
if(isset($_SERVER['HTTP_IF_NONE_MATCH'])) {
	// If HTTP_IF_NONE_MATCH is same as the generated ETag => content is the same as browser cache
	// So send a 304 Not Modified response header and exit
	if($_SERVER['HTTP_IF_NONE_MATCH'] == $etag) {
		header('HTTP/1.1 304 Not Modified', true, 304);
		exit();
	} // if($_SERVER['HTTP_IF_NONE_MATCH'] == $etag) {
} // if(isset($_SERVER['HTTP_IF_NONE_MATCH'])) {
	
require_once("/home/www/wwwartikelschreiber/libraryv3/Functions.inc.php"); 
require_once("/home/www/wwwartikelschreiber/libraryv3/Logging.inc.php"); 
require_once("/home/www/wwwartikelschreiber/libraryv3/Minify.inc.php"); 
require_once("/home/www/wwwartikelschreiber/libraryv3/Template.inc.php"); 
require_once("/home/www/wwwartikelschreiber/libraryv3/Language.inc.php");

$Func						= new Functions();
$myLogs 					= new Logging();
$myLogs->logURL();

$Langua						= new Language();
$language_array				= $Langua->getLanguageArray();
$language					= "en";
$tadditionalContentLinks	= $Func->createAddLinkService($language);
$myAdditionalNewsLinks 		= $Func->getAdditionalNewsLinks($language);
$language_html_flags 		= $Func->createLanguageFlagsHmtl();
$filename 					= "/home/www/security/unaiqueASCOM/latest_artikelschreibercom_$language.json";

if (file_exists($filename)){
	$filecontent 	= file_get_contents($filename);
	$json_file 		= json_decode($filecontent, true);
	$last_content 	= str_replace(["\r\n", "\r", "\n"], "<br />", $json_file['openai']);
	$openai_lastchar 			= substr(trim($last_content), -1);
		
	switch ($openai_lastchar){
		case $openai_lastchar != '.': $last_content .= ".";
		case $openai_lastchar != '!': $last_content .= ".";
		case $openai_lastchar != '?': $last_content .= ".";
		break;
	};
}; // if (file_exists($filename)){

$arr_cookie_options = array (
	'expires' 	=> time() - 60*60*3,
	'path' 		=> '/',
	'domain' 	=> 'www.artikelschreiber.com', // leading dot for compatibility or use subdomain
	'secure' 	=> true,     // or false
	'httponly' 	=> False,    // or false
	'samesite' 	=> 'Strict' // None || Lax  || Strict
);
setcookie("DemoArtikelSessionID", "", $arr_cookie_options);   
unset($_COOKIE["DemoArtikelSessionID"]);

$content 	= array_merge(
		array('robots'=>"index,follow,all"),
		array('title'=>$language_array[$language]['index_title']),
		array('description'=>$language_array[$language]['index_description']),
		array('links'=>$additional_links),
		array('title_linking'=>$language_array[$language]['index_title']),
		array('description_linking'=>$language_array[$language]['index_description']),
		array('url_linking'=>$language_array[$language]['url']),
		array('index_title_short_de'=>$language_array["de"]['index_title_short']),
		array('index_description_de'=>$language_array["de"]['index_description']),
		array('index_title_short_en'=>$language_array[$language]['index_title_short']),
		array('index_description_en'=>$language_array[$language]['index_description']),
		array('startpage_url_de'=>$language_array["de"]['url']),
		array('startpage_url_en'=>$language_array[$language]['url']),
		array('startpage_header_h1'=>$language_array[$language]['startpage_header_h1']),
		array('startpage_header_h2'=>$language_array[$language]['startpage_header_h2']),
		array('text'=>""),
		array('additionalNewsLinks'=>$myAdditionalNewsLinks),
		array('lang'=>$language),
		array('language'=>$language),
		array('summary'=>""),
		#array('sprachprofil'=>""),
		#array('sprachprofil_plain'=>""),
		array('uniqueidentifier'=>""),
		array('headline'=>""),
		array('article_description'=>""),
		array('language_text'=>''),
		array('language_html_links'=>$language_html_flags),
		array('wikipedia'=>''),
		array('youtube'=>''),
		array('suchanfrage'=>""),
		array('imagefiller1'=>""),
		array('ai_adv'=>$last_content),
		array('contentLinkNewDiv'=>$tadditionalContentLinks),
		array('keywords_startpage'=>$keywords_startpage),
		array('article_text_singleline'=>"Free Texts - Unique Content Marketing Texts ✓ Unique Text | ArtikelSchreiber.com"),
		array('count_articles'=>"The team of the ArtikelSchreiber.com has already created $p_count_articles english articles for satisfied users. With 3 clicks you are there too!"),
		array('topics'=>"")
	);
$Minify 	= new Minify();
$design		= new Template();
$design->setPath("/home/www/wwwartikelschreiber/tplv3");
$HtmlOutputDesign 	= $design->display_cache('index_en', $content, false, false, 3600*3);
echo $Minify->doMinify($HtmlOutputDesign);
$Logs = new Logging();
$Logs->logQuerys(__FILE__);
exit(0);