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
ini_set('memory_limit','5512M');
ini_set('max_execution_time', 30000);
//error_reporting(E_ALL);
//ini_set('display_errors', 1);
// setting error logging to be active
ini_set("log_errors", TRUE); 
ini_set('error_log', "/tmp/errors.txt");
$language					= "";
$post_mk					= "";
$post_sk					= "";
$sessionID					= "";

if (isset($_REQUEST['lang'])){
	$language					= trim($_REQUEST['lang']);
}
if (isset($_REQUEST['mainkeyword'])){
	$post_mk					= trim($_REQUEST['mainkeyword']); // utf8_encode(trim($_POST['mainkeyword']));
}
if (isset($_REQUEST['subkeyword'])){
	$post_sk					= trim($_REQUEST['subkeyword']); // utf8_encode(trim($_POST['subkeyword']));
}
if (isset($_REQUEST['uniqueidentifier'])){
	$sessionID					= utf8_encode(trim($_REQUEST['uniqueidentifier']));
}
/*
var_dump($post_mk); echo "\n";
var_dump($post_sk);echo "\n";
var_dump($language);echo "\n";
var_dump($sessionID);echo "\n";
*/

if (strlen($language) != 2 or empty($language)) {
	//echo "The string $newphrase does not consist of all letters or digits.\n";
	header("HTTP/1.1 301 Moved Permanently");
	header("Location: https://www.artikelschreiber.com/");
	header("Connection: close");
	exit(0);
} // if (strlen($newphrase) < 9) {

require_once("/home/www/wwwartikelschreiber/libraryv3/Security.inc.php");
require_once("/home/www/wwwartikelschreiber/libraryv3/Functions.inc.php");
require_once("/home/www/wwwartikelschreiber/libraryv3/Logging.inc.php"); 
require_once("/home/www/wwwartikelschreiber/libraryv3/Template.inc.php"); 
require_once("/home/www/wwwartikelschreiber/libraryv3/Language.inc.php");

$alternativeImg				= "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/AI_Humans_and_Robots.jpg/600px-AI_Humans_and_Robots.jpg";
$alternativeAds 			= '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8441004200831936" crossorigin="anonymous"></script>';


//$sqllite_dir 				= 'sqlite://home/www/wwwartikelschreiber/libraryv3/db/nodouble.sqlite';
//$sqllite_db  				= new PDO($sqllite_dir); //or die("cannot open the database");
$Security					= new Security();
$Func 						= new Functions();
$design						= new Template();
$Logs 						= new Logging();
$Lang						= new Language();
$langArray					= $Lang->getLanguageArray();
$isValidBetweenRequests 	= $Security->getLastmodFromIPToFile();	// in schreibenDE.php zuerst aufrufen, Mit Rückgabeparameter
$Logs->logURL();

$mainkeyword 				= filter_var($post_mk, FILTER_SANITIZE_STRING);
$subkeyword 				= filter_var($post_sk, FILTER_SANITIZE_STRING);

$mk_badflag					= $Security->isBadEntry($mainkeyword);
$sk_badflag					= $Security->isBadEntry($subkeyword);

if ($mk_badflag === True){
	$mainkeyword 			= "";
}
if ($sk_badflag === True){
	$subkeyword 			= "";
}

$mainkeyword				= $Security->sanitizeRequest($mainkeyword);
$subkeyword					= $Security->sanitizeRequest($subkeyword);
$mainkeyword 				= substr($mainkeyword,0,255);
$subkeyword 				= substr($subkeyword,0,255);

if (strlen($subkeyword) == 0){
	$subkeyword = $mainkeyword ;
} // if (strlen($subkeyword) == 0){

$Security->logRequestsWithIP($mainkeyword,$subkeyword);
$checkInputLanguage			= $Lang->checkExistingLanguage($language);

if ($checkInputLanguage === False){
	$language = "en";
} // if ($checkInputLanguage === False){
//echo $language;

$tadditionalContentLinks	= $Func->createAddLinkServiceAdvanced($language, $sessionID);
//$key 						= str_replace(" ","",strtolower($post_mk.$post_sk));
$maintext					= "$mainkeyword, $subkeyword";

if (strlen($sessionID) < 30 and (strlen($mainkeyword) >= 2 or strlen($subkeyword) >= 2)){
	$seconds_to_cache 			= 75000;
	$ts 						= gmdate("D, d M Y H:i:s", time() + $seconds_to_cache) . " GMT";
	header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
	header("Cache-Control: post-check=0, pre-check=0", false);
	header("Pragma: no-cache");
	header("Content-Type: text/html; charset=UTF-8");
	header("Expires: $ts");
	//header("Cache-Control: public, max-age=$seconds_to_cache, pre-check=$seconds_to_cache");
	header("X-UA-Compatible: IE=edge,chrome=1");
	
	$content_create = array_merge(
		array('robots'=>"index,follow,all"),
		array('title'=>$langArray[$language]['title_create']),
		array('description'=>$langArray[$language]['description_create']),
		array('contentLinkNewDiv'=>$tadditionalContentLinks),
		array('title_linking'=>$langArray[$language]['index_title']),
		array('description_linking'=>$langArray[$language]['index_description']),
		array('url_linking'=>$langArray[$language]['url']),
		array('language'=>$language),
		array('canonical'=>$langArray[$language]['url']),
		array('startpage_url'=>$langArray["de"]['url']),
		array('suchanfrage'=>$langArray[$language]['url'])
	);

	$myCookieTime 		= time()-36000;
	$arr_cookie_options = $Func->setCookieOptions($myCookieTime);
	setcookie("DemoArtikelSessionID", "", $arr_cookie_options);
	unset($_COOKIE["DemoArtikelSessionID"]);
	
	$sessionID 			= md5($maintext.time().uniqid(rand(), true).uniqid(rand(), true).uniqid(rand(), true)) ."-ARTIKELSCHREIBER";
	$myCookieTime 		= time()+36000;
	$arr_cookie_options = $Func->setCookieOptions($myCookieTime);
	setcookie("DemoArtikelSessionID", $sessionID, $arr_cookie_options);  // verfällt in 1 Stunde 
	$Func->makeWebServiceCall($mainkeyword, $subkeyword, $sessionID, $language);
				
	$design->setPath("/home/www/wwwartikelschreiber/tplv3");
	$HtmlOutputDesign 	= $design->display_cache('loadempty'."_".$language, $content_create, false, false, 3600*3);
	echo $HtmlOutputDesign;
	//$sqllite_db=null; 
	exit(0);
}// if (strlen($sessionID) < 30 and strlen($mainkeyword) >= 3 and strlen($subkeyword) >= 2){

$pos1 		= stripos($sessionID, "ARTIKELSCHREIBER");
$title 		= $Func->getContent($sessionID, $language, "title");
$summary	= $Func->getContent($sessionID, $language, "summary");
if (strlen($sessionID) > 25 and $pos1 !== false and strlen($language) >= 2 and strlen($title) > 5 and strlen($summary) > 12){
	$seconds_to_cache 			= 75000;
	$ts 						= gmdate("D, d M Y H:i:s", time() + $seconds_to_cache) . " GMT";
	header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
	header("Cache-Control: post-check=0, pre-check=0", false);
	header("Pragma: no-cache");
	header("Content-Type: text/html; charset=UTF-8");
	header("Expires: $ts");
	//header("Cache-Control: public, max-age=$seconds_to_cache, pre-check=$seconds_to_cache");
	header("X-UA-Compatible: IE=edge,chrome=1");
	
	$image 						= $Func->getContent($sessionID, $language, "image");
	$imageStatus 				= $Func->checkForValidImage($image);
	if ($imageStatus !== True){
		$image 					= $alternativeImg;
	} // if ($imageStatus !== True){

	$uri 						= $Func->getContent($sessionID, $language, "url");
	$title 						= $Func->getContent($sessionID, $language, "title");
	$description 				= $Func->getContent($sessionID, $language, "description");
	if (strlen($description) < 3){
		$description			= $title;
	} // if (strlen($description) < 3){
	$canonical	 				= $Func->getContent($sessionID, $language, "canonical");
	$summary	 				= $Func->getContent($sessionID, $language, "summary");
	$keywords 					= $Func->getContent($sessionID, $language, "keywords");
	$topics	 					= $Func->getContent($sessionID, $language, "topics");
	$topics_html				= $Func->topicsToList($topics);
	$article_text	 			= $Func->getContent($sessionID, $language, "article_text");
	$article_text_ai	 		= $Func->getContent($sessionID, $language, "article_text_ai");
	$author				 		= $Lang->writeAuthorText($language);
	$reading_time 				= $Func->lesezeit($article_text, $language);
	$external_links 			= $Func->randomWikiLink($topics, $keywords, $language);
	//$suggestions	 			= $Func->getContent($sessionID, $language, "suggestions");
	$similar_content			= $Func->getContent($sessionID, $language, "serp_related_searches");
	$serp_mainkeyword			= $Func->getContent($sessionID, $language, "serp_mainkeyword");
	$serp_subkeywords			= $Func->getContent($sessionID, $language, "serp_subkeywords");
	$similarContent				= $Func->createRelatedArticles($similar_content, $serp_mainkeyword, $serp_subkeywords, $language); 
	//$similarContent				= $Func->createSimilarArticles($suggestions, $language);
	
	$article_source 			= $Func->getSourceHiddenLink($sessionID, $uri, $language);
	$uri_description 			= $Func->getSourceHiddenLinkDescription($uri);
	$additionalContentLinks		= $Func->createAddLinkServiceAdvanced($language, $sessionID);
	$imageHTML 					= $Func->getImageHtml($image, $description);
	$seoArticleSchemaorg 		= $Func->createStructuredSEOData($title, $summary, $description, $topics, $language, $canonical, $image);
	$og_topics					= str_replace(";",",",$topics);
	$og_datetime				= date(DATE_ISO8601, time());
	$og_main_topic				= explode(";",$topics)[0];
	$seoSpeakingSchemaorg 		= $Func->createStructuredSEODataSpeaking($title, $canonical);		
	$seoBreadcrumbSchemaorg 	= $Func->createStructuredSEODataBreadcrumb($canonical, $topics, $keywords, $sessionID, $language);	
			
	$h1_headline 				= $Func->getContent($sessionID, $language, "h1");
	$h1_text	 				= $Func->getContent($sessionID, $language, "h1_text");
	$h1_text_ai	 				= $Func->getContent($sessionID, $language, "h1_text_ai");
	$h1_tag 					= $Func->getHeadlineTags($topics, $keywords, 1);
	$h1_text_till_end			= $Func->getContent($sessionID, $language, "h1_text_till_end");

	$h2_headline 				= $Func->getContent($sessionID, $language, "h2");
	$h2_text	 				= $Func->getContent($sessionID, $language, "h2_text");
	$h2_text_ai	 				= $Func->getContent($sessionID, $language, "h2_text_ai");
	$h2_tag 					= $Func->getHeadlineTags($topics, $keywords, 2);
	$h2_text_till_end			= $Func->getContent($sessionID, $language, "h2_text_till_end");

	$h3_headline 				= $Func->getContent($sessionID, $language, "h3");
	$h3_text	 				= $Func->getContent($sessionID, $language, "h3_text");
	$h3_text_ai	 				= $Func->getContent($sessionID, $language, "h3_text_ai");
	$h3_tag 					= $Func->getHeadlineTags($topics, $keywords, 3);
	$h3_text_till_end			= $Func->getContent($sessionID, $language, "h3_text_till_end");

	$h4_headline 				= $Func->getContent($sessionID, $language, "h4");
	$h4_text	 				= $Func->getContent($sessionID, $language, "h4_text");
	$h4_text_ai	 				= $Func->getContent($sessionID, $language, "h4_text_ai");
	$h4_tag 					= $Func->getHeadlineTags($topics, $keywords, 4);
	$h4_text_till_end			= $Func->getContent($sessionID, $language, "h4_text_till_end");

	$h5_headline 				= $Func->getContent($sessionID, $language, "h5");
	$h5_text	 				= $Func->getContent($sessionID, $language, "h5_text");
	$h5_text_ai	 				= $Func->getContent($sessionID, $language, "h5_text_ai");
	$h5_tag 					= $Func->getHeadlineTags($topics, $keywords, 5);
	$h5_text_till_end			= $Func->getContent($sessionID, $language, "h5_text_till_end");

	$h6_headline 				= $Func->getContent($sessionID, $language, "h6");
	$h6_text	 				= $Func->getContent($sessionID, $language, "h6_text");
	$h6_text_ai	 				= $Func->getContent($sessionID, $language, "h6_text_ai");
	$h6_tag 					= $Func->getHeadlineTags($topics, $keywords, 6);
	$h6_text_till_end			= $Func->getContent($sessionID, $language, "h6_text_till_end");

	$article_textblock 			= $article_text;
	if (strlen($article_text_ai) > 7){
		$article_textblock 	= $article_text_ai . "<!-- 1 -->";
	}

	$h1_headline_textblock 		= $h1_text ." ". $h1_text_till_end;
	$h1_headline_textblock_ai 	= $h1_text_ai . "<!-- 1 -->";
	$h2_headline_textblock 		= $h2_text ." ". $h2_text_till_end;
	$h2_headline_textblock_ai 	= $h2_text_ai . "<!-- 1 -->";
	$h3_headline_textblock 		= $h3_text ." ". $h3_text_till_end;
	$h3_headline_textblock_ai 	= $h3_text_ai . "<!-- 1 -->";
	$h4_headline_textblock 		= $h4_text  ." ". $h4_text_till_end;
	$h4_headline_textblock_ai 	= $h4_text_ai . "<!-- 1 -->";
	$h5_headline_textblock 		= $h5_text  ." ". $h5_text_till_end;
	$h5_headline_textblock_ai 	= $h5_text_ai . "<!-- 1 -->";
	$h6_headline_textblock 		= $h6_text  ." ". $h6_text_till_end;
	$h6_headline_textblock_ai 	= $h6_text_ai . "<!-- 1 -->";
	
	$openai 					= $Func->getContent($sessionID, $language, "openai");
	$openai_lastchar 			= substr(trim($openai), -1);
		
	switch ($openai_lastchar){
		case $openai_lastchar != '.': $openai .= ".";
		case $openai_lastchar != '!': $openai .= ".";
		case $openai_lastchar != '?': $openai .= ".";
		break;
	};
	
	$word_count1 = str_word_count($h1_text, 0);
	$word_count2 = str_word_count($h2_text, 0);
	$word_count3 = str_word_count($h3_text, 0);
	$word_count4 = str_word_count($h4_text, 0);
	$word_count5 = str_word_count($h5_text, 0);
	$word_count6 = str_word_count($h6_text, 0);
	
	if ($word_count1 < 120){
		$h1_headline="";
		$h1_headline_textblock="";
		$h1_headline_textblock_ai="";
		$h1_text_ai="";
		$h1_text="";
		$h1_text_till_end="";
	}
	if ($word_count2 < 120){
		$h2_headline="";
		$h2_headline_textblock="";
		$h2_headline_textblock_ai="";
		$h2_text_ai="";
		$h2_text="";
		$h2_text_till_end="";
	}
	if ($word_count3 < 120){
		$h3_headline="";
		$h3_headline_textblock="";
		$h3_headline_textblock_ai="";
		$h3_text_ai="";
		$h3_text="";
		$h3_text_till_end="";
	}
	if ($word_count4 < 120){
		$h4_headline="";
		$h4_headline_textblock="";
		$h4_headline_textblock_ai="";
		$h4_text_ai="";
		$h4_text="";
		$h4_text_till_end="";
	}
	if ($word_count5 < 120){
		$h5_headline="";
		$h5_headline_textblock="";
		$h5_headline_textblock_ai="";
		$h5_text_ai="";
		$h5_text="";
		$h5_text_till_end="";
	}
	if ($word_count6 < 120){
		$h6_headline="";
		$h6_headline_textblock="";
		$h6_headline_textblock_ai="";
		$h6_text_ai="";
		$h6_text="";
		$h6_text_till_end="";
	}
	
	//$imageHTML_Final = "<a href=\"$canonical\" title=\"$description\" hreflang=\"$language\" targe=\"_self\">$imageHTML</a>";
	
	$content = array_merge(
		array('startpage_url_de'=>$langArray["de"]['url']),
		array('startpage_url_en'=>$langArray["en"]['url']),
		array('startpage_header_h1'=>$langArray[$language]['startpage_header_h1']),
		array('startpage_header_h2'=>$langArray[$language]['startpage_header_h2']),
		array('index_title_short_de'=>$langArray["de"]['index_title_short']),
		array('index_description_de'=>$langArray["de"]['index_description']),
		array('index_title_short_en'=>$langArray["en"]['index_title_short']),
		array('index_description_en'=>$langArray["en"]['index_description']),
		array('robots'=>"index,follow,all"),
		array('title'=>$title),
		array('language'=>$language),
		array('description'=>$description),
		array('canonical'=>$canonical),
		array('summary'=>$summary),
		array('social_tags'=>$topics_html),
		array('article_text'=>$article_textblock),
		array('author'=>$author),
		array('reading_time'=>$reading_time),
		array('external_links'=>$external_links),
		array('suggestions'=>$similarContent),
		array('article_source'=>$article_source),
		array('article_source_description'=>$uri_description),
		array('contentLinkNewDiv'=>$additionalContentLinks),
		array('image_code'=>$imageHTML),
		array('schemaorg_article'=>$seoArticleSchemaorg),
		array('schemaorg_speaking'=>$seoSpeakingSchemaorg),
		array('schemaorg_breadcrumb'=>$seoBreadcrumbSchemaorg),
		array('image'=>$image),
		array('og_topics'=>$og_topics),
		array('og_datetime'=>$og_datetime),
		array('og_main_topic'=>$og_main_topic),
		array('title_linking'=>$langArray[$language]['index_title']),
		array('description_linking'=>$langArray[$language]['index_description']),
		array('url_linking'=>$canonical),
		array('h1_tag'=>$h1_tag),
		array('h1_headline'=>$h1_headline),
		array('h1_headline_textblock'=>$h1_headline_textblock),
		array('h1_headline_textblock_ai'=>$h1_headline_textblock_ai),
		array('h2_tag'=>$h2_tag),
		array('h2_headline'=>$h2_headline),
		array('h2_headline_textblock'=>$h2_headline_textblock),
		array('h2_headline_textblock_ai'=>$h2_headline_textblock_ai),
		array('h3_tag'=>$h3_tag),
		array('h3_headline'=>$h3_headline),
		array('h3_headline_textblock'=>$h3_headline_textblock),
		array('h3_headline_textblock_ai'=>$h3_headline_textblock_ai),
		array('h4_tag'=>$h4_tag),
		array('h4_headline'=>$h4_headline),
		array('h4_headline_textblock'=>$h4_headline_textblock),
		array('h4_headline_textblock_ai'=>$h4_headline_textblock_ai),
		array('h5_tag'=>$h5_tag),
		array('h5_headline'=>$h5_headline),
		array('h5_headline_textblock'=>$h5_headline_textblock),
		array('h5_headline_textblock_ai'=>$h5_headline_textblock_ai),
		array('h6_tag'=>$h6_tag),
		array('h6_headline'=>$h6_headline),
		array('h6_headline_textblock'=>$h6_headline_textblock),
		array('h6_headline_textblock_ai'=>$h6_headline_textblock_ai),
		array('language'=>$language),
		array('ai_adv'=>$openai),
		array('enabled_ads'=>$alternativeAds)
	);

	$design->setPath("/home/www/wwwartikelschreiber/tplv3/v4");
	if (strcasecmp($language,"de") == 0){
		$HtmlOutputDesign 	= $design->display_cache('index_show_dev4', $content, false, false, 3600*3);
	} else {
		$HtmlOutputDesign 	= $design->display_cache('index_show_env4', $content, false, false, 3600*3);
	}
	$myCookieTime = time()-360000;
	$arr_cookie_options = $Func->setCookieOptions($myCookieTime);
	setcookie("DemoArtikelSessionID", "", $arr_cookie_options);
	unset($_COOKIE["DemoArtikelSessionID"]);
	//echo $Minify->doMinify($HtmlOutputDesign);
	echo $HtmlOutputDesign;
	exit(0);

} // if (strlen($content['lang']) >= 2 or strlen($content['headline']) > 5 or strlen($content['text']) > 120 ){
exit(0);