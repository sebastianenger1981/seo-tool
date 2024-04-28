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
#error_reporting(E_ALL);
#ini_set('display_errors', 1);
// setting error logging to be active
//ini_set("log_errors", TRUE); 
// setting the logging file in php.ini
#ini_set('error_log', "/tmp/phperrors.txt");

require_once("/home/www/wwwartikelschreiber/libraryv3/Language.inc.php");
require_once("/home/www/wwwartikelschreiber/libraryv3/Security.inc.php");
//require_once("/home/www/wwwartikelschreiber/libraryv3/Sphinx.inc.php");
//require_once("/home/www/wwwartikelschreiber/libraryv3/GeoIP2/vendor/autoload.php");
//use GeoIp2\Database\Reader;

class Functions {
	public function getAdditionalNewsLinks($myLanguage){
		$Secu		= new Security();
		$dom 		= new DOMDocument();
		//$Func		= new Functions();
		libxml_use_internal_errors(true);

		$blog_path 	= "/home/www/wwwartikelschreiber/texts/";
		$files 		= scandir($blog_path);
		shuffle($files);
		$url 		= "https://www.artikelschreiber.com/texts/";

		//$myLanguage = "de";
		//$myLanguageAvailable = array("de","it","es","en","fr");
		$myHTML 	= '<ul role="list">';
		$myMaxLinks = 7;
		$myMaxLinksCounter = 0;

		for ($y=0; $y<count($files) - 1; $y++){
			$myFile 	= $files[$y];
			$myfinfile 	= $blog_path."/".$myFile;
			
			if ($myMaxLinksCounter > $myMaxLinks){
				break;
			};
			
			if (strlen($myFile) < 33){
				continue;
			};
			
			preg_match('/-(\w{2})-(\w{3})\.html/i', $myFile, $matches, PREG_OFFSET_CAPTURE);
			if (count($matches) > 0){
				continue;
			};
			
			$pos_de	= strpos($myFile, "artikel");
			$pos_en	= strpos($myFile, "article");
			$pos_it	= strpos($myFile, "articolo");
			$pos_es	= strpos($myFile, "articulo");
					
			$lang = "en";
			if ($pos_de !== false){
				$lang = "de";
			}
			if ($pos_en !== false){
				$lang = "en";
			}
			if ($pos_it !== false){
				$lang = "it";
			}
			if ($pos_es !== false){
				$lang = "es";
			}
			
			$pos_de_not	= strpos($myfinfile, $lang);
			$pos_en_not	= strpos($myfinfile, $lang);
			$pos_it_not	= strpos($myfinfile, $lang);
			$pos_es_not	= strpos($myfinfile, $lang);
					
			if (strlen($myFile) > 10 and stripos($myFile, '.html') !== false and ($pos_de_not === false or $pos_en_not === false or $pos_it_not === false or $pos_es_not === false) and ($pos_de !== false or $pos_en !== false or $pos_it !== false or $pos_es !== false) ){			
				// $dom->loadHTMLFile(mb_convert_encoding($myfinfile, 'HTML-ENTITIES', 'UTF-8'));
				//if($dom->loadHTMLFile($myfinfile)) { 
				if($dom->loadHTMLFile($myfinfile)) { 
					$list_title			= $dom->getElementsByTagName("title"); #title
					$title 				= utf8_decode($list_title->item(0)->textContent);
					$myfinurl 			= $url.$myFile;
					$title 				= $Secu->sanitizeForJsonOption($title);
					$title 				= preg_replace('/[\x00-\x1F\x80-\xFF]/', '', $title);
					
					if (strlen($title) > 7 and $this->endsWith($myfinurl,".html") and $myMaxLinksCounter <= $myMaxLinks and strcasecmp($myLanguage,$lang) == 0 ) { 
						// https://www.php.net/manual/en/language.operators.php
						$myHTML 	.= "<li role=\"listitem\"><a href=\"$myfinurl\" rel=\"me\" target=\"_self\" hreflang=\"$lang\" title=\"$title -> $myfinurl\">$title</a></li>";
						$myMaxLinksCounter++;
					}; // if (strlen($title) < 3 and endsWith($myfinurl,".html")){; // if (strlen($title) < 3 and endsWith($myfinurl,".html")){
				}; // if($dom->loadHTMLFile($myfinfile)) { 
			}; // if (strlen($myFile) > 10 and stripos($myFile, '.html') !== false and ($pos_de_not 
		}; //for ($y=0; $iy<count($files) - 1; $y++){

		$myHTML 	.= "</ul>";
		return $myHTML;
	} // function getAdditionalNewsLinks(){
	
	public function schema_faq_for_html($faq){
		$fq = $faq['faq_question'];
		$fa = $faq['faq_answer'];
		if (strlen($fq) > 1 and strlen($fa) > 1){
			return "<li role=\"listitem\"><b>$fq</b> - $fa</li><li role=\"listitem\" style=\"list-style-type: none;\"><br /></li>";
		}
		return "";
	} // function schema_faq($faq){
	
	public function schema_faq($faq){
		$fq = $faq['faq_question'];
		$fa = $faq['faq_answer'];
		if (strlen($fq) > 1 and strlen($fa) > 1){
			return array(
				'@type' 	=> 'Question',
				'name' 		=> $fq,
				'acceptedAnswer' => array(
					'@type' => 'Answer',
					'text' 	=> $fa
				)
			);
		} else {
			return array();
		}
	} // function schema_faq($faq){
			
	public function generateFAQSchema($faq_content){
		$schema_faqs = array();
		foreach ($faq_content as $faq) {
			$my_item 	= $this->schema_faq($faq);
			$json 		= json_encode($my_item); 
			if (strlen($json) > 10){
				array_push($schema_faqs, $my_item);
			};
		}; // foreach ($faq_content as $faq) {
			
		if (count($schema_faqs) > 0){
			$data1 = array(
				'@context' => 'https://schema.org/',
				'@type' => 'FAQPage',
				'mainEntity' => [
					$schema_faqs
				],
			);

			$data2 = json_encode($data1);
			return '<script type="application/ld+json">' . $data2 . '</script>';
		}; // if (count($schema_faqs) > 0){
		return '';
	} // function generateFAQSchema($faq_content){
	
	public function checkForValidImage($url){
		$ch 			= curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_NOBODY, true);
		curl_setopt($ch, CURLOPT_HEADER, true);
		curl_setopt($ch, CURLOPT_VERBOSE, true);
		$resp 			= curl_exec($ch);
		$header_size 	= curl_getinfo($ch, CURLINFO_HEADER_SIZE);
		$headers 		= substr($resp, 0, $header_size);
		//$body 		= substr($resp, $header_size);
		//$response	=json_decode(curl_exec($ch),true);
		curl_close($ch);
		//echo gettype($headers), "\n";
		
		$response 		= explode("\r\n", $headers);
		//print("<pre>".print_r($response,true)."</pre>");	
		if (is_array($response)){
			foreach($response as $key => $val){
				$pos1 = stripos($val,"content-type: image");		
				if (strlen($val) >= 10 and strlen($val) <= 40 and $pos1 !== false and isset($val) and !empty($val)){
					return True;
				} // if (strlen($response[$key])) >= 7
			} // foreach($response as $key => $val) {
		} // if (is_array($response)){
		return False;
	} // function checkForValidImage($url){

	public function randWord($length=7){
		return substr(str_shuffle("qwertyuiopasdfghjklzxcvbnm"),0,$length);
	} // function randWord($length=7){
		
	public function getHeadlineTags($topics, $keywords, $count_element){
		$maxcounter = 0;
		if (strlen($keywords) > 7){ 
			foreach(explode(';',$keywords) as $key) {
				if ($maxcounter == $count_element - 1){
					return $key;
				}// if ($maxcounter == $count_element - 1){
				$maxcounter++;
			} // foreach(explode(';',$keywords) as $key) {
		}//if (strlen($keywords) > 7){ 
		$maxcounter = 0;
		if (strlen($topics) > 7){ 
			foreach(explode(';',$topics) as $key) {
				if ($maxcounter == $count_element - 1){
					return $key;
				}// if ($maxcounter == $count_element - 1){
				$maxcounter++;
			} // foreach(explode(';',$topics) as $key) {
		} // if (strlen($topics) > 7){ 
		return randWord();
	} // function getHeadlineTags($topics, $keywords, $count_element){
	
	
	public function topicsToList($topics){
		$html = "<ul>";
		foreach(explode(';',$topics) as $key) {
			$html .= "<li>#$key</li>";
		} // foreach(explode(';',$topics) as $key) {
		$html .= "</ul>";
		return $html;
	} // function topicsToList($topics){

	function topicsToMetatags($topics){
		$html 	= "";
		$t1 	= explode(';',$topics);
		$t2 	= explode(',',$topics);
		foreach($t1 as $key1) {
			//$pos2		= strpos($key, ";");
			if (strlen($key1) > 1){ // and $pos2 === false){
				$html .= "<meta property=\"article:tag\" content=\"$key1\" />";
			};
		} // foreach(explode(';',$topics) as $key) {
		foreach($t2 as $key2) {
			//echo "DEBUG: $key\n";
			//$pos2		= strpos($key, ",");
			if (strlen($key2) > 1){ // and $pos2 === false){
				$html .= "<meta property=\"article:tag\" content=\"$key2\" />";
			};
		} // foreach(explode(';',$topics) as $key) {
		return $html;
	} // function topicsToList($topics){

	public function randomWikiLink($topics, $keywords, $language){
		$html = "<ul role=\"list\">";
		$maxcounter = 0;
		if (strlen($keywords) > 2){ 
			foreach(explode(';',$keywords) as $key) {
				if ($maxcounter < 1){ // 1 externer Link immer rel-follow
					$html .= "<li role=\"listitem\" style=\"padding: 1px;\"><a href=\"https://$language.wikipedia.org/w/index.php?search=$key\" title=\"$key in $language of Wikipedia\" hreflang=\"$language\" target=\"_blank\" rel=\"noreferrer\">https://$language.wikipedia.org/wiki/$key</a></li>";
					//$html .= "<li style=\"list-style-type: none;\"><br /></li>";
					$maxcounter++;
				} elseif ($maxcounter < 6){
					$html .= "<li role=\"listitem\" style=\"padding: 1px;\"><a href=\"https://$language.wikipedia.org/w/index.php?search=$key\" title=\"$key in $language of Wikipedia\" hreflang=\"$language\" target=\"_blank\" rel=\"nofollow noreferrer\">https://$language.wikipedia.org/wiki/$key</a></li>";
					//$html .= "<li style=\"list-style-type: none;\"><br /></li>";
					$maxcounter++;
				} // if ($maxcounter < 5){
			} // foreach(explode(';',$topics) as $key) {
		}//if (strlen($keywords) > 2){ 
		//$maxcounter = 0;
		if (strlen($topics) > 2){ 
			foreach(explode(';',$topics) as $key) {
				if ($maxcounter < 1){ // 1 externer Link immer rel-follow
					$html .= "<li role=\"listitem\" style=\"padding: 1px;\"><a href=\"https://$language.wikipedia.org/w/index.php?search=$key\" title=\"$key in $language of Wikipedia\" hreflang=\"$language\" target=\"_blank\" rel=\"noreferrer\">https://$language.wikipedia.org/wiki/$key</a></li>";
					//$html .= "<li style=\"list-style-type: none;\"><br /></li>";
					$maxcounter++;
				} elseif ($maxcounter < 6){
					$html .= "<li role=\"listitem\" style=\"padding: 1px;\"><a href=\"https://$language.wikipedia.org/w/index.php?search=$key\" title=\"$key in $language of Wikipedia\" hreflang=\"$language\" target=\"_blank\" rel=\"nofollow noreferrer\">https://$language.wikipedia.org/wiki/$key</a></li>";
					//$html .= "<li style=\"list-style-type: none;\"><br /></li>";
					$maxcounter++;
				} // if ($maxcounter < 5){
			} // foreach(explode(';',$topics) as $key) {
		} // if (strlen($topics) > 2){ 
		$html .= "</ul>";
		return $html;
	} // function randomWikiLink($topics, $keywords, $language){
	
	public function getImageHtml($image, $description){
		return "<img src=\"$image\" alt=\"$description\" title=\"$description\" class=\"responsive\" role=\"banner\" referrerpolicy=\"no-referrer\" loading=\"lazy\" style=\"border:2px solid black\">";
	} // function getImageHtml($image, $description){

	public function createRelatedArticles($similar_content, $serp_mainkeyword, $serp_subkeywords, $language){
		$Lang			= new Language();
		$langArray		= $Lang->getLanguageArray();
		$mainkeyword	= $langArray[$language]['mainkeyword'];
		$subkeyword		= $langArray[$language]['subkeyword'];
		$newarticle		= $langArray[$language]['request_action_create'];
		$buttontext		= $langArray[$language]['action_createtext'];

		$mkRes			= array();
		for ($s = 0; $s < count($similar_content); $s++) {
			$element 	= $similar_content[$s]["related_searches"];
			if (strlen($element) > 1){
				array_push($mkRes, $element);
			}
		} // for ($s = 0; $s < count($p_ai_similar); $s++) {
		
		$json_ld = "";
		shuffle($mkRes);	
		for ($s = 0; $s < 3; $s++) {
			// https://www.virendrachandak.com/techtalk/php-isset-vs-empty-vs-is_null/
			if (is_array($mkRes) and isset($mkRes[$s]) and !empty($mkRes[$s]) and strlen($mkRes[$s]) > 1){
				$mk = $mkRes[$s];
				$r1 = $this->randWord();
				$r2 = $this->randWord();
				$r3 = $this->randWord();
				if (!empty($mk) and !is_null($mk) and strlen($mk) > 3){
					$json_ld .= <<<NAMEN
						<div class="row">						
							<div class="col c8" style="border-style:hidden; margin: 5px;">
								<div class="col c3" style="margin: 1px;">
									<label for="$r1">$mainkeyword:&nbsp;&nbsp;&nbsp;</label> <input type="text" id="$r1" name="$r1" value="$mk" required />
								</div>
								<div class="col c3" style="margin: 1px;">
									<label for="$r2">$subkeyword:&nbsp;&nbsp;&nbsp;</label> <input type="text" id="$r2" name="$r2" value="$serp_mainkeyword" required />
								</div>
								<div class="col c1" style="margin: 1px;">
									<!-- <label for="button">$buttontext</label> --> &nbsp;&nbsp;&nbsp; <a href="https://www.artikelschreiber.com/textgenerator.php?lang=$language&mainkeyword=$mk&subkeyword=$serp_mainkeyword" target="_blank" rel="nofollow"><input type="submit" id="$r3" value="$buttontext" class="btn btn-b" style="font-size:16px;font-weight:bold;" /></a>
								</div>
							</div>
					</div>
NAMEN;
				} // if (!empty($mk) and !is_null($mk) and strlen($mk) > 3 and !empty($sk) and !is_null($sk) and strlen($sk)){
			} // if (is_array($mkRes) and is_array($skRes) and isset($mkRes[$s]) and isset($skRes[$s]) and !empty($mkRes[$s]) and !empty($skRes[$s]])){
		} // for ($s = 0; $s < 3; $s++) {
			
		for ($s = 2; $s < 5; $s++) {
			// https://www.virendrachandak.com/techtalk/php-isset-vs-empty-vs-is_null/
			if (is_array($mkRes) and isset($mkRes[$s]) and !empty($mkRes[$s]) and strlen($mkRes[$s]) > 1){
				$mk = $mkRes[$s];
				$r1 = $this->randWord();
				$r2 = $this->randWord();
				$r3 = $this->randWord();
				if (!empty($mk) and !is_null($mk) and strlen($mk) > 3){
					$json_ld .= <<<NAMEN
						<div class="row">						
							<div class="col c8" style="border-style:hidden; margin: 5px;">
								<div class="col c3" style="margin: 1px;">
									<label for="$r1">$mainkeyword:&nbsp;&nbsp;&nbsp;</label> <input type="text" id="$r1" name="$r1" value="$mk" required />
								</div>
								<div class="col c3" style="margin: 1px;">
									<label for="$r2">$subkeyword:&nbsp;&nbsp;&nbsp;</label> <input type="text" id="$r2" name="$r2" value="$serp_subkeywords" required />
								</div>
								<div class="col c1" style="margin: 1px;">
									<!-- <label for="button">$buttontext</label> --> &nbsp;&nbsp;&nbsp; <a href="https://www.artikelschreiber.com/textgenerator.php?lang=$language&mainkeyword=$mk&subkeyword=$serp_subkeywords" target="_blank" rel="nofollow"><input type="submit" id="$r3" value="$buttontext" class="btn btn-b" style="font-size:16px;font-weight:bold;" /></a>
								</div>
							</div>
					</div>
NAMEN;
				} // if (!empty($mk) and !is_null($mk) and strlen($mk) > 3 and !empty($sk) and !is_null($sk) and strlen($sk)){
			} // if (is_array($mkRes) and is_array($skRes) and isset($mkRes[$s]) and isset($skRes[$s]) and !empty($mkRes[$s]) and !empty($skRes[$s]])){
		} // for ($s = 0; $s < 3; $s++) {
		return $json_ld;
	} //function getSimilarContent($sessionID){

	public function createSimilarArticles($suggestions, $language){
		$Lang			= new Language();
		$langArray		= $Lang->getLanguageArray();
		$mainkeyword	= $langArray[$language]['mainkeyword'];
		$subkeyword		= $langArray[$language]['subkeyword'];
		$newarticle		= $langArray[$language]['request_action_create'];
		$buttontext		= $langArray[$language]['action_createtext'];

		$mkRes			= array();
		$skRes			= array();
		for ($s = 0; $s < count($suggestions); $s++) {
			$element 	= $suggestions[$s];
			$pos1		= strpos($element, "mk=");
			$pos2		= strpos($element, "sk=");
			if ($pos1 !== false){
				$w	= str_replace("mk=","", $element);
				array_push($mkRes, $w);
				//echo "element=$w<br>";
			} elseif ($pos2 !== false){
				$w	= str_replace("sk=","", $element);
				array_push($skRes, $w);
			} // if strpos("mk=", $element) === True){
		} // for ($s = 0; $s < count($p_ai_similar); $s++) {
		
		if (count($mkRes) > 10 and count($skRes) <5){
			$a1=array_pop($mkRes);
			$a2=array_pop($mkRes);
			$a3=array_pop($mkRes);
			$a4=array_pop($mkRes);
			$a5=array_pop($mkRes);
			array_push($skRes,$a1);
			array_push($skRes,$a2);
			array_push($skRes,$a3);
			array_push($skRes,$a4);
			array_push($skRes,$a5);
		} // if (count($mkRes) > 6 and count($skRes) <3){

		if (count($skRes) > 10 and count($mkRes) <5){
			$a1=array_pop($skRes);
			$a2=array_pop($skRes);
			$a3=array_pop($skRes);
			$a4=array_pop($skRes);
			$a5=array_pop($skRes);
			array_push($mkRes,$a1);
			array_push($mkRes,$a2);
			array_push($mkRes,$a3);
			array_push($mkRes,$a4);
			array_push($mkRes,$a5);
		} // if (count($mkRes) > 6 and count($skRes) <3){

		if (count($mkRes) < 5 and count($skRes) < 5){
			$mkRes = array_merge($mkRes,$skRes);
			$skRes = array_merge($mkRes,$skRes);
		} // if (count($mkRes) > 6 and count($skRes) <3){

		if (count($skRes) < 5 and count($mkRes) < 5){
			$mkRes = array_merge($mkRes,$skRes);
			$skRes = array_merge($mkRes,$skRes);
		} // if (count($mkRes) > 6 and count($skRes) <3){

		$json_ld = "";
		shuffle($skRes);
		shuffle($mkRes);	
		for ($s = 0; $s < 5; $s++) {
			// https://www.virendrachandak.com/techtalk/php-isset-vs-empty-vs-is_null/
			if (is_array($mkRes) and is_array($skRes) and isset($mkRes[$s]) and isset($skRes[$s]) and !empty($mkRes[$s]) and !empty($skRes[$s])){
				$mk = $mkRes[$s];
				$sk = $skRes[$s];
				$r1 = $this->randWord();
				$r2 = $this->randWord();
				$r3 = $this->randWord();
				if (!empty($mk) and !is_null($mk) and strlen($mk) > 3 and !empty($sk) and !is_null($sk) and strlen($sk)){
					$json_ld .= <<<NAMEN
						<div class="row">						
							<div class="col c8" style="border-style:hidden; margin: 5px;">
								<div class="col c3" style="margin: 1px;">
									<label for="$r1">$mainkeyword:&nbsp;&nbsp;&nbsp;</label> <input type="text" id="$r1" name="$r1" value="$mk" required />
								</div>
								<div class="col c3" style="margin: 1px;">
									<label for="$r2">$subkeyword:&nbsp;&nbsp;&nbsp;</label> <input type="text" id="$r2" name="$r2" value="$sk" required />
								</div>
								<div class="col c1" style="margin: 1px;">
									<label for="button">$buttontext</label> &nbsp;&nbsp;&nbsp; <a href="https://www.artikelschreiber.com/textgenerator.php?lang=$language&mainkeyword=$mk&subkeyword=$sk" target="_blank" rel="nofollow"><input type="submit" id="$r3" value="$buttontext" class="btn btn-b" style="font-size:16px;font-weight:bold;" /></a>
								</div>
							</div>
					</div>
NAMEN;
				} // if (!empty($mk) and !is_null($mk) and strlen($mk) > 3 and !empty($sk) and !is_null($sk) and strlen($sk)){
			} // if (is_array($mkRes) and is_array($skRes) and isset($mkRes[$s]) and isset($skRes[$s]) and !empty($mkRes[$s]) and !empty($skRes[$s]])){
		} // for ($s = 0; $s < 3; $s++) {
		return $json_ld;
	} //function getSimilarContent($sessionID){

	public function getSourceHiddenLinkDescription($uri){
		$parse 	= parse_url($uri);
		return $parse['host'];
	} // function getSourceHiddenLinkDescription($uri){

	public function getSourceHiddenLink($sessionID, $article_source, $language){
		$c1 							= uniqid (rand (),true);
		$c2 							= uniqid (rand (),true);
		$c3 							= uniqid (rand (),true);
		$c4 							= uniqid (rand (),true);
		$c5 							= uniqid (rand (),true);
		$c6 							= uniqid (rand (),true);
		$c7 							= uniqid (rand (),true);
		$c8 							= uniqid (rand (),true);
		$fake_redirect 					= $c1.$c2.$c3.$c4.$c5.$c6.$c7.$c8;
		return "/redirect.php?sid=$fake_redirect&l=$language&s=$sessionID&q=$article_source";
	} // function getSourceHiddenLink(){


	public function createStructuredSEODataSpeaking($title, $canonical){
		$Secu			= new Security();
		$p_headline		= $Secu->sanitizeForJsonOption($title);
		$html =<<<NAME
			<script type="application/ld+json" async>
			{
				"@context": "https://schema.org/",
				"@type": "WebPage",
				"name": "$title",
				"speakable":
			{
				"@type": "SpeakableSpecification",
				"xpath": [
					"/html/head/title",
					"/html/head/meta[@name='description']/@content"
				]
			},
			"url": "$canonical"
			}
			</script>
NAME;
		return $html;
	} // function createStructuredSEODataSpeaking($title){


	public function createStructuredSEODataBreadcrumb($canonical, $topics, $keywords, $sessionID, $language){
		$Secu			= new Security();
		
		$h1_tag 		= $this->getHeadlineTags($topics, $keywords, 1);
		$h2_tag 		= $this->getHeadlineTags($topics, $keywords, 2);
		$h3_tag 		= $this->getHeadlineTags($topics, $keywords, 3);
		$h1_headline 	= $this->getContent($sessionID, $language, "h1");
		$h2_headline 	= $this->getContent($sessionID, $language, "h2");
		$h3_headline 	= $this->getContent($sessionID, $language, "h3");
		
		$p_headline1	= $Secu->sanitizeForJsonOption($h1_headline);
		$p_headline2	= $Secu->sanitizeForJsonOption($h2_headline);
		$p_headline3	= $Secu->sanitizeForJsonOption($h3_headline);
		
		if (strlen($p_headline1) == 0){
			$p_headline1 = $h1_tag;
		}
		if (strlen($p_headline2) == 0){
			$p_headline2 = $h2_tag;
		}
		if (strlen($p_headline3) == 0){
			$p_headline3 = $h3_tag;
		}
		
		$html =<<<NAME
			<script type="application/ld+json" async>
			{
			  "@context": "http://schema.org",
			  "@type": "BreadcrumbList",
			  "itemListElement": [{
				"@type": "ListItem",
				"position": 1,
				"item": {
				  "@id": "$canonical#$h1_tag",
				  "name": "$p_headline1"
				}
			  },{
				"@type": "ListItem",
				"position": 2,
				"item": {
				  "@id": "$canonical#$h2_tag",
				  "name": "$p_headline2"
				}
			  },{
				"@type": "ListItem",
				"position": 3,
				"item": {
				  "@id": "$canonical#$h3_tag",
				  "name": "$p_headline3"
				}
			  }]
			}
			</script>
NAME;
		return $html;
	} // function createStructuredSEODataBreadcrumb(){
	
	// Function to read the json Content from ArtikelSchreiber Results
	public function getContent($sessionID, $language, $id){
		//"/home/www/security/unaiqueASCOM/"+str(session)+"_"+str(language)+".json"
		$filename 			= "/home/www/security/unaiqueASCOM/$sessionID"."_"."$language.json";
		//echo "<!-- $filename -->";
		if (file_exists($filename)){
			$filecontent 	= file_get_contents($filename);
			$json_file 		= json_decode($filecontent, true);
			
			foreach($json_file as $key => $val) {
				//echo "key=$key, id=$id<br>";
				if (strcasecmp($key,$id)==0) {
				//echo "key=$key, id=$id<br>";				
					return $val; 
				} // if (strcasecmp($key,$id)==0) {
			} // foreach($json_file as $key => $val) {
		} // if (file_exists($filename)){
	} // function getTitle($sessionID, $language){
	
	// Function to check the string is ends 
	// with given substring or not
	public function endsWith($string, $endString){
		$len = strlen($endString);
		if ($len == 0) {
			return true;
		}
		return (substr($string, -$len) === $endString);
		 /* 
		// Driver code
		if(endsWith("abcde","de"))
			echo "True";
		else
			echo "False";
		*/
	} // public function endsWith($string, $endString){
	
	//public function checkStopwordList($mainkw,$subkw){
	public function isBadBlogContent($text){
		$stoplist 	= array();	// quelle: https://gist.github.com/ryanlewis/a37739d710ccdb4b406d
		$stoplist 	= file('/home/unaique/library3/blacklists/pornstopwordlist.txt'); // /home/www/wwwartikelschreiber/libraryv3/pornstopwordlist.txt
		$text		= trim(strtolower($text));
		
		//var_dump($stoplist);
		foreach ($stoplist as $word){
			$word = trim(strtolower($word));
			if (strlen($word) > 0 and stripos($word, '#') !== True){
				//////////////$pos1 = stripos($word, $word);		
				if(preg_match("/\s{$word}/i", $text) or preg_match("/{$word}\s/i", $text) or preg_match("/\b{$word}\b/i", $text)) {	
					// https://stackoverflow.com/questions/4366730/how-do-i-check-if-a-string-contains-a-specific-word
					//return True;
					return 1;
				}; // if(preg_match("/\s{$word}/i", $text) or preg_match("/{$word}\s/i", $text) or preg_match("/\b{$word}\b/i", $text)) {	
			//////////////	if ($pos1 === True) {
			//////////////		//echo "pos1 $mainkw match with $word<br />";
			//////////////		//file_put_contents("/home/www/logs/ARTIKELSCHREIBER/porn.log", date("Y-m-d H:i:s") . " |$mainkw|mainkw porn Match\n", FILE_APPEND | LOCK_EX);
			//////////////		return True;
			//////////////	}
			}; // if ((strlen($word) > 0){
		}; // foreach ($word in stoplist){
		#return false;
		return 0;
	} // public function isBadBlogContent($text){
	
	public function makeWebServiceYoutube2TextCall($SessionID, $Link){
		$Security 	= new Security();
		$myIP 		= $Security->getRealUserIP();
		$socket 	= stream_socket_client('unix:///home/unaique/FlaskApp/gunicorn.sock', $errno, $errstr);
		$array_data = array('sess' => $SessionID, 'link' => $Link, 'ip' => $myIP);
		$json_data 	= json_encode($array_data);

		//Source: https://varunver.wordpress.com/2013/02/13/php-using-fsockopen-to-post-json-data/
		$out ="POST /createTextsbyYoutube/ HTTP/1.1\r\n";
		//$out.= "Host: ".$parts['host']."\r\n";
		$out.= "Host: [Server-IP]\r\n";
		$out.= "Content-Type: application/json\r\n";
		$out.= "Content-Length: ".strlen($json_data)."\r\n";
		$out.= "Connection: Close\r\n\r\n";
		$out .= $json_data;
		fwrite($socket, $out);
		fclose($socket);
		return True;
	} // public function makeWebServiceYoutube2TextCall($SessionID, $Link){
	
	public function createAddLinkService($language){
		$Langua			= new Language();
		$language_array	= $Langua->getLanguageArray();
		$valid_langs 	= array('de','en','es','fr','it','jp','in','sa','cn','ru','tr','pt');
		shuffle($valid_langs);
		$languageRandom = $valid_langs[0];
		if ($languageRandom == $language){
			$languageRandom = $valid_langs[1];
		}
		$title_create 		= $language_array[$language]['index_title'];
		$description 		= $language_array[$language]['index_description'];
		$index_descr 		= $language_array[$language]['summary'];
		$url				= $language_array[$language]['url'];

		//return "$title_create1 : $description1 &nbsp;&nbsp;-&nbsp;&nbsp; $title_create2 : $description2 &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.unaique.net/' title='Text Generator deutsch - KI Text Generator | UNAIQUE.NET' target='_self' hreflang='de'>KI Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.unaique.net/en/' title='CopyWriting: Generator for Marketing Content by AI | UNAIQUE.NET' target='_self' hreflang='en'>AI Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.artikelschreiber.com/' title='Dein automatischer ArtikelSchreiber | ArtikelSchreiber.com' hreflang='de' target='_self'>ArtikelSchreiber</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.artikelschreiber.com/en/' title='Text Generator: Aritcle Writer for Marketing | ArtikelSchreiber.com' hreflang='en' target='_self'>Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://rechthaben.net/' title='rechthaben.net' hreflang='de' target='_self'>rechthaben.net</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.unaique.com/' title='www.unaique.com' hreflang='en' target='_self'>www.unaique.com</a>";
		
		return "<a href='$url' title='$description' target='_self' hreflang='$language'>$title_create</a>";
	} // public function createAddLinkService($language){
		
	public function createAddLinkServiceAdvanced($language, $sessionID){
		$Langua			= new Language();
		$language_array	= $Langua->getLanguageArray();
		$valid_langs 	= array('de','en','es','fr','it','jp','in','sa','cn','ru','tr','pt');
		shuffle($valid_langs);
		$languageRandom = $valid_langs[0];
		if ($languageRandom == $language){
			$languageRandom = $valid_langs[1];
		}
		$title_create 		= $language_array[$language]['index_title'];
		$description 		= $language_array[$language]['index_description'];
		$index_descr 		= $language_array[$language]['summary'];
		$url				= $language_array[$language]['url'];

		$title1 			= $this->getContent($sessionID, $language, "title");
		$description1 		= $this->getContent($sessionID, $language, "description");
		$canonical1	 		= $this->getContent($sessionID, $language, "canonical");
		$language_canonical1	= $this->getContent($sessionID, $language, "language");
		
		if (strlen($description1) < 3){
			$description1 = $title1;
		}

		//return "$title_create1 : $description1 &nbsp;&nbsp;-&nbsp;&nbsp; $title_create2 : $description2 &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.unaique.net/' title='Text Generator deutsch - KI Text Generator | UNAIQUE.NET' target='_self' hreflang='de'>KI Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.unaique.net/en/' title='CopyWriting: Generator for Marketing Content by AI | UNAIQUE.NET' target='_self' hreflang='en'>AI Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.artikelschreiber.com/' title='Dein automatischer ArtikelSchreiber | ArtikelSchreiber.com' hreflang='de' target='_self'>ArtikelSchreiber</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.artikelschreiber.com/en/' title='Text Generator: Aritcle Writer for Marketing | ArtikelSchreiber.com' hreflang='en' target='_self'>Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://rechthaben.net/' title='rechthaben.net' hreflang='de' target='_self'>rechthaben.net</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.unaique.com/' title='www.unaique.com' hreflang='en' target='_self'>www.unaique.com</a>";
		
		//return "<a href='https://www.unaique.net/' title='Text Generator deutsch - KI Text Generator | UNAIQUE.NET' target='_self' hreflang='de'>KI Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.artikelschreiber.com/' title='Dein automatischer ArtikelSchreiber | ArtikelSchreiber.com' hreflang='de' target='_self'>Text schreiben</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.artikelschreiben.com/' title='Artikel schreiben mit ChatGPT KI | ArtikelSchreiben.com' hreflang='de' target='_self'>Artikel schreiben</a> &nbsp;&nbsp;-&nbsp;&nbsp <a href='https://www.unaique.com/' title='AI WRITER - Content Generator | UNAIQUE.COM' target='_self' hreflang='en'>AI WRITER</a>";
		
		return "<a href='$url' title='$description' target='_self' hreflang='$language'>$title_create</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='$canonical1' title='$description1' hreflang='$language_canonical1' target='_self'>$title1</a>";
	} // public function createAddLinkService($language){
		
	public function makeWebServiceNFTCall($SessionID){
		$Security 	= new Security();
		$myIP 		= $Security->getRealUserIP();
				
		$socket 	= stream_socket_client('unix:///home/unaique/FlaskApp/gunicorn.sock', $errno, $errstr);

		$array_data = array('sess' => $SessionID, 'ip' => $myIP);
		$json_data 	= json_encode($array_data);

		//Source: https://varunver.wordpress.com/2013/02/13/php-using-fsockopen-to-post-json-data/
		$out ="POST /createNFT/ HTTP/1.1\r\n";
		//$out.= "Host: ".$parts['host']."\r\n";
		$out.= "Host: [Server-IP]\r\n";
		$out.= "Content-Type: application/json\r\n";
		$out.= "Content-Length: ".strlen($json_data)."\r\n";
		$out.= "Connection: Close\r\n\r\n";
		$out .= $json_data;
		fwrite($socket, $out);
		fclose($socket);
		return True;
	} // public function makeWebServiceLink2TextCall($sessionID, $link){
		
	/*
	public function getGeoInformation(){
		$reader 	= new Reader('/home/www/wwwartikelschreiber/libraryv3/GeoIP2/GeoLite2-City.mmdb');

		#/home/www/wwwartikelschreiber/libraryv3/GeoIP2
		#curl -sS https://getcomposer.org/installer | php
		#php composer.phar require geoip2/geoip2:~2.0
		#https://github.com/maxmind/GeoIP2-php
		
		$Security 	= new Security();
		$myIP 		= $Security->getRealUserIP();
		$record 	= $reader->city($myIP);

		$content_create = array_merge(
			array('iso'=>$record->country->isoCode),
			array('nam'=>$record->country->name), 
			array('cna'=>$record->city->name), 
			array('cpc'=>$record->postal->code), 
			array('cla'=>$record->location->latitude), 
			array('clo'=>$record->location->longitude)
		);
		return json_encode($content_create);
	} // public function getGeoInformation(){
	*/
	
	/* Use it for json_encode some corrupt UTF-8 chars
	 * useful for = malformed utf-8 characters possibly incorrectly encoded by json_encode
	  Source https://stackoverflow.com/questions/46305169/php-json-encode-malformed-utf-8-characters-possibly-incorrectly-encoded
	 */
	public function utf8ize( $mixed ) {
		if (is_array($mixed)) {
			foreach ($mixed as $key => $value) {
				$mixed[$key] = $this->utf8ize($value);
			}
		} elseif (is_string($mixed)) {
			return mb_convert_encoding($mixed, "UTF-8", "UTF-8");
		}
		return $mixed;
	} // public function utf8ize( $mixed ) {
	
	public function setCookieOptions($myTime){
		$arr_cookie_options = array (
			'expires' 	=> $myTime, //time() + 60*60*24*30,
			'path' 		=> '/',
			'domain' 	=> 'www.artikelschreiber.com', // leading dot for compatibility or use subdomain
			'secure' 	=> true,     // or false
			'httponly' 	=> false,    // or false
			'samesite' 	=> 'Strict' // None || Lax  || Strict
		);
		return $arr_cookie_options;
	} // function setCookieOptions(){
	
	public function startsWith($string, $startString){
		$len = strlen($startString);
		return (substr($string, 0, $len) === $startString);
	} // function startsWith ($string, $startString){
		
	public function makeWebServiceParaphraseCall($SessionID, $MainKeyword, $Language){
		$Security 	= new Security();
		
		//$SessionID	= urlencode($SessionID);
		//$Language	= urlencode($Language);
		//$MainKeyword= urlencode($MainKeyword);
		$myIP 		= $Security->getRealUserIP();
		
		$socket 	= stream_socket_client('unix:///home/unaique/FlaskApp/gunicorn.sock', $errno, $errstr);

		$array_data = array('sess' => $SessionID, 'lang' => $Language, 'query' => $MainKeyword, 'ip' => $myIP);
		$json_data 	= json_encode($array_data);

		//Source: https://varunver.wordpress.com/2013/02/13/php-using-fsockopen-to-post-json-data/
		$out ="POST /createTextsbyParaphrase/ HTTP/1.1\r\n";
		//$out.= "Host: ".$parts['host']."\r\n";
		$out.= "Host: [Server-IP]\r\n";
		$out.= "Content-Type: application/json\r\n";
		$out.= "Content-Length: ".strlen($json_data)."\r\n";
		$out.= "Connection: Close\r\n\r\n";
		$out .= $json_data;
		fwrite($socket, $out);
		fclose($socket);
		return True;
	} // public function makeWebServiceLink2TextCall($sessionID, $link){
		
	public function makeWebServiceSloganCall($SessionID, $MainKeyword, $Language){
		$Security 	= new Security();
		
		//$SessionID	= urlencode($SessionID);
		//$Language	= urlencode($Language);
		//$MainKeyword= urlencode($MainKeyword);
		$myIP 		= $Security->getRealUserIP();
		
		$socket 	= stream_socket_client('unix:///home/unaique/FlaskApp/gunicorn.sock', $errno, $errstr);

		$array_data = array('sess' => $SessionID, 'lang' => $Language, 'query' => $MainKeyword, 'ip' => $myIP);
		$json_data 	= json_encode($array_data);

		//Source: https://varunver.wordpress.com/2013/02/13/php-using-fsockopen-to-post-json-data/
		$out ="POST /createTextsbySlogan/ HTTP/1.1\r\n";
		//$out.= "Host: ".$parts['host']."\r\n";
		$out.= "Host: [Server-IP]\r\n";
		$out.= "Content-Type: application/json\r\n";
		$out.= "Content-Length: ".strlen($json_data)."\r\n";
		$out.= "Connection: Close\r\n\r\n";
		$out .= $json_data;
		fwrite($socket, $out);
		fclose($socket);
		return True;
	} // public function makeWebServiceLink2TextCall($sessionID, $link){
	
	public function makeWebServiceLink2TextCall($SessionID, $Link){
		$Security 	= new Security();
		
		//$SessionID	= urlencode($sessionID);
		//$Link		= urlencode($link);
		$myIP 		= $Security->getRealUserIP();
				
		$socket 	= stream_socket_client('unix:///home/unaique/FlaskApp/gunicorn.sock', $errno, $errstr);

		$array_data = array('sess' => $SessionID, 'link' => $Link, 'ip' => $myIP);
		$json_data 	= json_encode($array_data);

		//Source: https://varunver.wordpress.com/2013/02/13/php-using-fsockopen-to-post-json-data/
		$out ="POST /createTextsbyLink/ HTTP/1.1\r\n";
		//$out.= "Host: ".$parts['host']."\r\n";
		$out.= "Host: [Server-IP]\r\n";
		$out.= "Content-Type: application/json\r\n";
		$out.= "Content-Length: ".strlen($json_data)."\r\n";
		$out.= "Connection: Close\r\n\r\n";
		$out .= $json_data;
		fwrite($socket, $out);
		fclose($socket);
		return True;
	} // public function makeWebServiceLink2TextCall($sessionID, $link){
	
	public function createLanguageFlagsHmtl(){
		$Lang			= new Language();
		$langArray		= $Lang->getLanguageArray();
		$lan 			= array("de","en","fr","es","it","ru","pt","sa","in","jp","cn","tr");
		$htmlContent	='<ul style="list-style: none;">';
		
		foreach ($lan as $v){
			$desc_more 	= $langArray[$v]['description_create'];
			$desc 		= $langArray[$v]['description'];
			$url 		= $langArray[$v]['url'];
			$sumry 		= $langArray[$v]['summary'];
			$blog_descr	= $langArray[$v]['email_body'];
			
			$htmlContent .= "<li><a hreflang=\"$v\" href=\"$url\" title=\"$desc_more\" target=\"_self\"><img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" loading=\"lazy\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /> $sumry</a></li>";
			
			//$htmlContent .= "<li><a hreflang=\"$v\" href=\"$url\" title=\"$desc_more\" target=\"_self\"><img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" loading=\"lazy\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /> $sumry</a>&nbsp;&nbsp;&nbsp - &nbsp;&nbsp;&nbsp<a href=\"https://www.artikelschreiber.com/$v/blog/\" hreflang=\"$v\" title=\"$blog_descr\" target=\"_self\">Blog ($v)</a></li>";
			
			/*
			$htmlContent .= "<li><a hreflang=\"$v\" href=\"$url\" title=\"$desc_more\" target=\"_self\"><img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" loading=\"lazy\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /> $sumry</a>&nbsp;&nbsp;&nbsp - &nbsp;&nbsp;&nbsp<a href=\"https://www.artikelschreiber.com/$v/blog/\" hreflang=\"$v\" title=\"$blog_descr\" target=\"_self\"><img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" loading=\"lazy\" width=\"32\" height=\"32\" title=\"$blog_descr\" alt=\"$desc_more\" /> Blog</a>
			</li>";
			
			$htmlContent .= "<li><a hreflang=\"$v\" href=\"$url\" onclick=\"jsLinksFunction('linkto_flag_$v');\" title=\"$desc_more\" target=\"_self\"><img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" loading=\"lazy\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /> $sumry <img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" loading=\"lazy\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /></a></li>";
			
			if ($v == 'hi'){
				$mv 	= "in";
				$htmlContent .= "<li><a hreflang=\"$mv\" href=\"$url\" onclick=\"jsLinksFunction('linkto_flag_$v');\" title=\"$desc_more\" target=\"_blank\"><img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /> $sumry <img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /></a></li>";
			} else {
				$htmlContent .= "<li><a hreflang=\"$v\" href=\"$url\" onclick=\"jsLinksFunction('linkto_flag_$v');\" title=\"$desc_more\" target=\"_blank\"><img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /> $sumry <img src=\"https://www.artikelschreiber.com/images/flags/$v.png\" width=\"32\" height=\"32\" title=\"$desc_more\" alt=\"$desc_more\" /></a></li>";
			};
			*/
			//$htmlContent .= "<fieldset lang=\"$language\" class=\"content\">$desc<br /></fieldset>";
		} // foreach ($lan as $v){
		$htmlContent.="</ul>";
	return $htmlContent;
	} // public function createLanguageFlagsHmtl(){
	/*
	public function getH1Headlines($sessionID){
		$pdo 			= $this->prepareQuery();
		$stmt 			= $pdo->prepare("SELECT * FROM unaique_cache WHERE p_sessionid = ? LIMIT 1;");
		$stmt->execute(array($sessionID));
		while($rows 	= $stmt->fetch(PDO::FETCH_ASSOC)) {
			$p_aitext 	= json_decode($rows["p_aitext"], true);
		} // while($rows = $stmt->fetch(PDO::FETCH_ASSOC)) {
		$p_meta_headlines= $p_aitext["meta_headlines"];

		$html			="<ol>";
		foreach ($p_meta_headlines as $key => $value){
			if (strlen($value) > 1){
				$html	.="<li>$key: <$key>$value</$key></li>";
			} // if (strlen($value) > 1){
		} // foreach ($p_meta_headlines as $key => $value){
		$html			.="</ol>";
		if (strlen($html) < 30){
			return "";
		} else {
			return $html;
		} // if (strlen($html) < 50){
	} // public function getH1Headlines($sessionID){
	*/
	
	// neu: 26.4.2022
	public function getH1Headlines($p_meta_headlines){
		$html			="<ol>";
		foreach ($p_meta_headlines as $key => $value){
			if (strlen($value) > 1){
				$html	.="<li>$key: <$key>$value</$key></li>";
			} // if (strlen($value) > 1){
		} // foreach ($p_meta_headlines as $key => $value){
		$html			.="</ol>";
		if (strlen($html) < 30){
			return "";
		} else {
			return $html;
		} // if (strlen($html) < 50){
	} // public function getH1Headlines($sessionID){
	
	public function getSimilarContent($sessionID, $language){
		$Lang			= new Language();
		$langArray		= $Lang->getLanguageArray();
		$mainkeyword	= $langArray[$language]['mainkeyword'];
		$subkeyword		= $langArray[$language]['subkeyword'];
		$newarticle		= $langArray[$language]['request_action_create'];
		$buttontext		= $langArray[$language]['action_createtext'];

		//$sessionID		= "dfb58aa45671077520d95c6d043b493e-UNAIQUENET";
		$json_ld 		= "";
		$pdo 			= $this->prepareQuery();
		$stmt 			= $pdo->prepare("SELECT * FROM unaique_cache WHERE p_sessionid = ? LIMIT 1;");
		$stmt->execute(array($sessionID));
		while($rows 	= $stmt->fetch(PDO::FETCH_ASSOC)) {
			$p_aitext 	= json_decode($rows["p_aitext"], true);
		} // while($rows = $stmt->fetch(PDO::FETCH_ASSOC)) {

		$p_ai_similar	= $p_aitext["similar"];
		if (count($p_ai_similar) < 1){
			return "";
		} // if (count($p_ai_similar) < 1){

		$mkRes			= array();
		$skRes			= array();
		for ($s = 0; $s < count($p_ai_similar); $s++) {
			$element 	= $p_ai_similar[$s];
			$pos1		= strpos($element, "mk=");
			$pos2		= strpos($element, "sk=");
			if ($pos1 !== false){
				$w	= str_replace("mk=","", $element);
				array_push($mkRes, $w);
				//echo "element=$w<br>";
			} elseif ($pos2 !== false){
				$w	= str_replace("sk=","", $element);
				array_push($skRes, $w);
			} // if strpos("mk=", $element) === True){
		} // for ($s = 0; $s < count($p_ai_similar); $s++) {
		
		//$skRes = $mkRes;

		//print("skRes1 ". count($skRes)."<br>");
		//print("mkRes1 ". count($mkRes)."<br>");

		if (count($mkRes) > 10 and count($skRes) <5){
			$a1=array_pop($mkRes);
			$a2=array_pop($mkRes);
			$a3=array_pop($mkRes);
			$a4=array_pop($mkRes);
			$a5=array_pop($mkRes);
			array_push($skRes,$a1);
			array_push($skRes,$a2);
			array_push($skRes,$a3);
			array_push($skRes,$a4);
			array_push($skRes,$a5);
		} // if (count($mkRes) > 6 and count($skRes) <3){

		if (count($skRes) > 10 and count($mkRes) <5){
			$a1=array_pop($skRes);
			$a2=array_pop($skRes);
			$a3=array_pop($skRes);
			$a4=array_pop($skRes);
			$a5=array_pop($skRes);
			array_push($mkRes,$a1);
			array_push($mkRes,$a2);
			array_push($mkRes,$a3);
			array_push($mkRes,$a4);
			array_push($mkRes,$a5);
		} // if (count($mkRes) > 6 and count($skRes) <3){

		if (count($mkRes) < 5 and count($skRes) < 5){
			$mkRes = array_merge($mkRes,$skRes);
			$skRes = array_merge($mkRes,$skRes);
		} // if (count($mkRes) > 6 and count($skRes) <3){

		if (count($skRes) < 5 and count($mkRes) < 5){
			$mkRes = array_merge($mkRes,$skRes);
			$skRes = array_merge($mkRes,$skRes);
		} // if (count($mkRes) > 6 and count($skRes) <3){

		//print("skRes2 ". count($skRes)."<br>");
		//print("mkRes2 ". count($mkRes)."<br>");

		$json_ld = <<<NAMEN
		<div class="row">
			<div class="col c8" xstyle="border-width:1px; border-style:double; margin: 5px;">
				<!--<p><b>$newarticle:</b></p>-->
				<div class="col c3" xstyle="margin: 10px;">
					<label for="mainkeyword">$mainkeyword:&nbsp;&nbsp;&nbsp;</label>
				</div>
				<div class="col c3" xstyle="margin: 10px;">
					<label for="subkeyword">$subkeyword:&nbsp;&nbsp;&nbsp;</label>
				</div>
				<div class="col c3" xstyle="margin: 10px;">
					<label for="button">$buttontext &nbsp;&nbsp;&nbsp;</label>
				</div>
			</div>
		</div>
NAMEN;

		shuffle($skRes);
		shuffle($mkRes);	
		for ($s = 0; $s < 5; $s++) {
			// https://www.virendrachandak.com/techtalk/php-isset-vs-empty-vs-is_null/
			$mk = $mkRes[$s];
			$sk = $skRes[$s];
			if (!empty($mk) and !is_null($mk) and strlen($mk) > 3 and !empty($sk) and !is_null($sk) and strlen($sk)){
				$json_ld .= <<<NAMEN
					<div class="row">
						<form action="https://www.artikelschreiber.com/articletexts.php" method="POST" autocomplete="on" target="_blank">
							<input type="hidden" name="lang" maxlength="2" size="2" value="$language" required>
							<div class="col c8" xstyle="border-width:1px; border-style:double; margin: 5px;">
								<div class="col c3" style="margin: 1px;">
									<input type="text" id="mainkeyword" name="mainkeyword" value="$mk" required />
								</div>
								<div class="col c3" style="margin: 1px;">
									<input type="text" id="subkeyword" name="subkeyword" value="$sk" required />
								</div>
								<div class="col c1" style="margin: 1px;">
									<input type="submit" id="button" xclass="nm-button" value="$buttontext" class="btn btn-b" style="font-size:16px;font-weight:bold;" onclick="jsLinksFunction('create_show_similar_$language');" />
								</div>
							</div>
						</form>
				</div>
NAMEN;
			} // if (!empty($mk) and !is_null($mk) and strlen($mk) > 3 and !empty($sk) and !is_null($sk) and strlen($sk)){
		} // for ($s = 0; $s < 3; $s++) {

	return $json_ld;
	
	} //function getSimilarContent($sessionID){
	
	// neu: 26.4.2022
	public function createStructuredSEOData($p_headline, $p_summary, $p_description, $p_topics, $language, $canonical, $image){
		if (strlen($p_headline) < 1 or strlen($p_summary) < 1){
			return "";
		} // if (strlen($p_headline) < 1 or strlen($p_summary) < 1 or strlen($p_description) < 1){
			
		//$Func			= new Functions();
		$Lang			= new Language();
		$Secu			= new Security();
		$langArray		= $Lang->getLanguageArray();

		//$use_ai		= True;
		//$language		= "de";
		//$sessionID	= "ac1226019dae6cbba0c115ab3a23c518-ARTIKELSCHREIBER";
		$myASCOMURL		= $langArray[$language]['url'];
		$myASCOMURLDESC	= $langArray[$language]['title_create'];
		/*
		$pdo 			= $this->prepareQuery();
		$stmt 			= $pdo->prepare("SELECT * FROM `unaique_cache` WHERE p_sessionid=:p_sessionid LIMIT 1;");
		$stmt->execute(array(':p_sessionid' => $sessionID));
				
		while($rows = $stmt->fetch(PDO::FETCH_ASSOC)) {
			$p_mainkeyword	= $rows["p_mainkeyword"];
			$p_subkeyword	= $rows["p_subkeyword"];
			$p_beautifytext	= $rows["p_beautifytext"];
			$p_extractedtext= $rows["p_extractedtext"];
			$p_textlanguage	= $rows["p_textlanguage"];
			$p_lang			= $rows["p_textlanguage"];
			$p_language		= $rows["p_textlanguage"];
			$p_topics		= $rows["p_topics"];
			$p_summary		= $rows["p_summary"];
			$p_articleurl	= $rows["p_articleurl"];
			$p_description	= $rows["p_description"];
			$p_sprachprofil = $rows["p_sprachprofil"];
			$p_simpletext 	= $rows["p_simpletext"];
			$p_headline		= $rows["p_headline"];
			$p_articlescore	= $rows["p_articlescore"];
			$p_sessionid	= $rows["p_sessionid"];
			$p_aitext		= json_decode($rows["p_aitext"], true);
		} // while($rows = $stmt->fetch(PDO::FETCH_ASSOC)) {
		*/
		//$p_headline1	= preg_replace("/&#?!.,;[a-z0-9]{2,8};/i","", $p_headline); // preg_replace("/&#?[a-z0-9]{2,8};/i","", $p_headline);
		//$p_headline2	= preg_replace("/[^A-Za-z0-9äöüÄÖÜß?!.,; ]/", '', $p_headline);
		$p_headline3	= $Secu->sanitizeForJsonOption($p_headline);

		//$p_summary1	= preg_replace("/&#?!.,;[a-z0-9]{2,8};/i","", $p_summary);
		//$p_summary2	= preg_replace("/[^A-Za-z0-9äöüÄÖÜß?!.,; ]/", '', $p_summary1);
		$p_summary3		= $Secu->sanitizeForJsonOption($p_summary);
		
		if (strlen($p_description) < 1){
			$l = explode('.', $p_summary);
			$p_description = $l[0];
		} // if (strlen($p_description) < 1){

		$p_description1	= preg_replace("/&#?[a-z0-9]{2,8};/i","", $p_description);
		$p_description2	= preg_replace("/[^A-Za-z0-9äöü ]/", '', $p_description1);
		$p_description3	= $Secu->sanitizeForJsonOption($p_description2);	// The meta description length is between 120 – 158 characters
		$p_description4 = $this->charLimitDescription($p_description3);
		//$word_counts 	= $Func->str_word_count_utf8($p_beautifytext);

		$t 				= explode(";",$p_topics);
		$keywords 		= implode(", ", $t);
				
		$myDate			= date(DATE_ATOM);
		$json_ld = <<<NAMEN
		<!--<p style="display: none;">-->
		<script type="application/ld+json">{
				"@context": "https://schema.org",
				"@type": "Article",
				"image": {
					"@type": "ImageObject",
					"url": "$image",
					"width": 531,
					"height": 628
				},
				"name": "Article",
				"url": "$canonical",
				"description": "$p_description4 ... $myASCOMURL",
				"headline": "$p_headline3",
				"dateCreated": "$myDate",
				"datePublished": "$myDate",
				"dateModified": "$myDate",
				"articleBody": "$p_summary3\nSource: $myASCOMURL.",
				"mainEntityOfPage": {
					"@type": "WebPage",
					"@id": "$myASCOMURL#webpage"
				},
				"publisher": {
					"@type": "Organization",
					"@id": "$myASCOMURL#organization",
					"url": "$myASCOMURL",
					"name": "ArtikelSchreiber.com",
					"description": "$myASCOMURLDESC",
					"logo": {
						"@type": "ImageObject",
						"@id": "$myASCOMURL#logo",
						"url": "https://www.artikelschreiber.com/images/logo.png",
						"width": 531,
						"height": 628
					},
					"image": {
						"@type": "ImageObject",
						"@id": "$myASCOMURL#logo",
						"url": "$image",
						"width": 531,
						"height": 628
					},
					"sameAs": [
						"https://www.unaique.net/"
					]
				},
				"keywords": "$keywords",
				"author": {
					"@type": "Person",
					"name": "ArtikelSchreiber.com",
					"url": "$myASCOMURL",
					"sameAs": [
						"https://www.unaique.net/"
					]
				},
				"@id": "$myASCOMURL#links",
				"commentCount": "0",
				"sameAs": [
					"https://www.artikelschreiber.com/",
					"https://www.artikelschreiber.com/en/",
					"https://www.artikelschreiber.com/es/",
					"https://www.artikelschreiber.com/fr/",
					"https://www.artikelschreiber.com/it/",
					"https://www.artikelschreiber.com/ru/",
					"https://www.artikelschreiber.com/cn/",
					"https://www.artikelschreiber.com/jp/",
					"https://www.artikelschreiber.com/sa/",
					"https://www.artikelschreiber.com/in/",
					"https://www.artikelschreiber.com/pt/",
					"https://www.artikelschreiber.com/tr/"
				],
				"speakable": {
					"@type": "SpeakableSpecification",
					"xpath": [
						"/html/head/title",
						"/html/head/meta[@name='description']/@content"
					]
				}
			}
		</script>
		<!--</p><br /><br />-->
NAMEN;

		//echo "<textarea rows=23 style=\"background:#fff; border:dashed #bc2122 1px; height:auto; width:100%;\">$json_ld</textarea>";
		return $json_ld;
	} // public function createStructuredSEOData($sessionID,$language,$use_ai){
	
	// cut string to 850 chars
	public function charLimitDescription($content){
		$upto = 150 - 42;
		if (strlen($content)>$upto){
			return substr($content,0,110);
		} else {
			return $content;
		};
	} // function charLimitDescription($content){
		
	public function charLimitMetaDescription($content, $upto){
		//$upto = 150;
		if (strlen($content)>$upto){
			return substr($content,0,$upto);
		} else {
			return $content;
		};
	} // public function charLimitMetaDescription($content){
	
	public function str_word_count_utf8($str) {
		return count(preg_split('~[^\p{L}\p{N}\']+~u',$str));
	} // function str_word_count_utf8($str) {
		
	
	public function getContentFromSQLviaDocinfo($docid, $language){
		if (is_numeric($docid)){
			$pdo 			= $this->prepareQuery();
			$stmt 			= $pdo->prepare("SELECT * FROM unaique_cache WHERE uid = ? LIMIT 1;");
			$stmt->execute(array($docid));
				
			while($rows = $stmt->fetch(PDO::FETCH_ASSOC)) {
				$p_beautifytext	= $rows["p_beautifytext"];
				$p_textlanguage	= $rows["p_textlanguage"];
				$p_simpletext 	= $rows["p_simpletext"];
				$p_sessionid	= $rows["p_sessionid"];
				$p_articlescore	= $rows["p_articlescore"];
				$p_headline 	= $rows["p_headline"];
			} // while($rows = $stmt->fetch(PDO::FETCH_ASSOC)) {
			//return "p_headline=$p_headline, p_textlanguage=$p_textlanguage, p_articlescore=$p_articlescore\n";
			return trim($p_sessionid);
		} else {
			$sessionIDFake = trim(file_get_contents("/home/www/wwwartikelschreiber/libraryv3/sessionfake_$language.txt"));
			return $sessionIDFake;
		} // if (is_numeric($docid)){
	} // function getContentFromSQLviaDocinfo($docid, $language){
	
	public function makeWebServiceCall($MainKeyword, $SubKeywords, $SessionID, $Language){
		$Security 		= new Security();
		
		// use the streaming unix server socket
		//$MainKeyword	= urlencode($mainkeyword);
		//$SubKeywords	= urlencode($subkeyword);
		//$SessionID		= urlencode($sessionID);
		//$Language		= urlencode($language);
		$myIP 		= $Security->getRealUserIP();
		
		if (file_exists('/home/unaique/FlaskApp/gunicorn.sock')) {
			//echo "The file $filename exists";
			//$socket = stream_socket_client('unix:///home/unaique/FlaskApp/gunicorn.sock', $errno, $errstr);
			//fwrite($socket, "GET /createTexts/mk/$MainKeyword/sk/$SubKeywords/sid/$SessionID/lg/$Language HTTP/1.1\r\nhost:    'www.artikelschreiber.com'\r\nAccept: */*\r\n\r\n");
			//fclose($socket);
			
			$socket 	= stream_socket_client('unix:///home/unaique/FlaskApp/gunicorn.sock', $errno, $errstr);
			$array_data = array('sid' => $SessionID, 'lg' => $Language, 'mk' => $MainKeyword, 'sk' => $SubKeywords, 'ip' => $myIP);
			$json_data 	= json_encode($array_data);

			//Source: https://varunver.wordpress.com/2013/02/13/php-using-fsockopen-to-post-json-data/
			$out ="POST /createTexts/ HTTP/1.1\r\n";
			//$out.= "Host: ".$parts['host']."\r\n";
			$out.= "Host: [Server-IP]\r\n";
			$out.= "Content-Type: application/json\r\n";
			$out.= "Content-Length: ".strlen($json_data)."\r\n";
			$out.= "Connection: Close\r\n\r\n";
			$out .= $json_data;
			fwrite($socket, $out);
			fclose($socket);
			
			$Security1 = new Security();
			$Security1->writeIPToFile(); # Erst die IP festschreiben, wenn auch wirklich ein Artikel erstellt wurde
		} else {
			//echo "The file $filename does not exist";
			setcookie("DemoArtikelSessionID", "", time()-36000);
			unset($_COOKIE["DemoArtikelSessionID"]);
			$sessionIDFake = trim(file_get_contents("/home/www/wwwartikelschreiber/libraryv3/sessionfake_$language.txt"));
			setcookie("DemoArtikelSessionID", $sessionIDFake, time()+36000);  /* verfällt in 1 Stunde */
		} // if (file_exists('/home/unaique/FlaskApp/gunicorn.sock')) {
		return True;
	} // function makeWebServiceCall($mainkeyword, $subkeyword, $sessionID, $language, $Func){
	
	// neu: 26.4.2022
	public function makeMysqlCall($sessionID){
		//https://www.php-einfach.de/mysql-tutorial/crashkurs-pdo/
		$Secu			= new Security();
		$langua			= new Language();
		$language_array	= $langua->getLanguageArray();
		$content		= array();
		$pdo 			= $this->prepareQuery();
		$stmt 			= $pdo->prepare("SELECT * FROM unaique_cache WHERE p_sessionid = ? LIMIT 1;");
		$stmt->execute(array($sessionID));
		$myRowCount 	= $stmt->rowCount();
		
		while($rows = $stmt->fetch(PDO::FETCH_ASSOC)) {
			//$p_spinnertext		= spinText($rows["p_spinnertext"]);
			$p_mainkeyword			= $rows["p_mainkeyword"];
			$p_subkeyword			= $rows["p_subkeyword"];
			$p_beautifytext			= $rows["p_beautifytext"];
			$p_originaltext			= $rows["p_originaltext"];
			$p_textlanguage			= $rows["p_textlanguage"];
			$p_lang					= $rows["p_textlanguage"];
			$p_language				= $rows["p_textlanguage"];
			$p_topics				= $rows["p_topics"];
			$p_summary				= $rows["p_summary"];
			$p_articleurl			= $rows["p_articleurl"];
			$p_description			= $rows["p_description"];
			$p_sprachprofil 		= $rows["p_sprachprofil"];
			$p_simpletext 			= $rows["p_simpletext"];
			$p_headline				= $rows["p_headline"];
			$p_aitext				= json_decode($rows["p_aitext"], true);
		} // while($rows = $stmt->fetch(PDO::FETCH_ASSOC)) {
		
		$finished_processing 		= False;
		if ($myRowCount > 0){
			$finished_processing 	= True;
		};
		
		//echo "results: $p_topics <br />";
		
		$structured_data_normal		= "";
		$structured_data_ai 		= "";	
		$structured_info			= "";
		//$p_ai_text					= $p_aitext['p_aitext'];
						
		$tv1						= explode(";",$p_topics);
		$descr_topics				= implode(" ✓ ", $tv1);
		$p_beautifytext3 			= str_replace(array("\n", "\r", "\r\n"), '<br />', $p_beautifytext);
		$reading_time 				= $this->estimate_reading_time($p_beautifytext3, $p_textlanguage);
				
		$language_sprache_artikel	= $langua->getLanguageArtikelSprache();
		$p_score_get				= $p_aitext['plagscore'];
		$p_ai_text					= $p_aitext['p_aitext'];
		$cpc_aitext					= $p_aitext['cpc_aitext'];
		$better_article				= $p_aitext['better_article'];
		#echo '<pre>' . var_export($better_article, true) . '</pre>';
		
		$p_score_html				= "";	
	
		$og_topics					= str_replace(";",",",$p_topics);
		$og_datetime				= date(DATE_ISO8601, time());
		$similarContent				= $this->getSimilarContent($sessionID, $p_textlanguage);
		$p_meta_headlines			= $p_aitext["meta_headlines"];
		$H1HeadlineHTML 			= $this->getH1Headlines($p_meta_headlines);
		$p_description				= $this->charLimitMetaDescription($p_description, 150);
		
		if ( strlen($p_headline) < 3 and strlen($p_description) > 3){
			$p_headline 			= $this->charLimitMetaDescription($p_description, 60);
		} elseif ( strlen($p_headline) < 3 and strlen($p_description) < 3){
			$p_headline				= $this->charLimitMetaDescription("$p_mainkeyword ✓ $p_subkeyword", 60);
		};
		
		if (strlen($p_headline) < 25){
			$p_headline				= implode('.', array_slice(explode(".", $p_summary1), 0, 1)). ".";
			$p_headline				= $this->charLimitMetaDescription($p_headline, 60);
			
		} elseif (strlen($p_headline) > 60){
			$p_headline				= $this->charLimitMetaDescription($p_headline, 60);
		};
		
		if (strlen($p_description) < 25){
			$p_description			= implode('.', array_slice(explode(".", $p_summary1), 1, 2)). ".";
			$p_description			= $this->charLimitMetaDescription($p_description, 150);
			
		} elseif (strlen($p_description) > 110){
			$p_description			= $this->charLimitMetaDescription("$p_mainkeyword ✓ $p_subkeyword", 150);
		};
		
		$p_summary1					= $Secu->sanitizeForJsonOption($p_summary);
		$p_description1				= $this->charLimitMetaDescription($p_description, 110);
		$p_description1				= $Secu->sanitizeForJsonOption($p_description1);
		$p_headline1				= $Secu->sanitizeForJsonOption($p_headline);
		$as1						= $this->createStructuredSEOData($p_headline1, $p_summary1, $p_description1, $p_topics, $p_textlanguage);
		$structured_info 			= $as1;
		$structured_data_normal 	= htmlentities($as1, ENT_COMPAT, 'UTF-8');
		
		if (strlen($p_ai_text) > 12){
			$p_summary1 			= implode('.', array_slice(explode(".", $p_ai_text), 0, 3)). ".";
			//$p_summary1			= preg_replace("/&#?!.,;[a-z0-9]{2,8};/i","", $p_summary1);
			//$p_summary1			= preg_replace("/[^A-Za-z0-9äöüÄÖÜß?!.,; ]/", '', $p_summary1);
			$p_summary1				= $Secu->sanitizeForJsonOption($p_summary1);
			$p_description			= $this->charLimitMetaDescription($p_description, 110);
			$p_description1			= $Secu->sanitizeForJsonOption($p_description);
			$p_headline1			= $Secu->sanitizeForJsonOption($p_headline);
			$as2					= $this->createStructuredSEOData($p_headline1, $p_summary1, $p_description1, $p_topics, $p_textlanguage);
			$structured_info 		= $as2;
			$structured_data_ai 	= htmlentities($as2, ENT_COMPAT, 'UTF-8');
			
			$my_plagscore			= 100-intval($p_score_get);
			if ($my_plagscore >= 50){
				$p_score_html		= "<span style=\"color: green; font-size: 16px;\">$my_plagscore%</span>";
			} else {
				$p_score_html		= "<span style=\"color: red; font-size: 16px;\">$my_plagscore%</span>";
			}
		} else {
			$p_score_html 			= "'Not available'";
			$p_ai_text 				= "<b>'Unique Article Text' Currently not available (Server overload & busy)</b>";
		} // if (strlen($p_ai_text) > 12){
				
		if (strlen($cpc_aitext) > 10){
			$p_ai_text				= $cpc_aitext;
		};
		
		$json_ld_faq = <<<NAMEN
			<script type="application/ld+json">{
			  "@context": "https://schema.org",
			  "@type": "FAQPage",
			  "mainEntity": [
	  
NAMEN;

		$show_questions				= $language_array[$p_textlanguage]['show_questions'];
		$p_faq						= $better_article['faq_antworten'];
		$p_faq_count_entry			= count($p_faq);
		$p_faq_html					= "<ul>";
		$p_faq_show_html			= "$show_questions: ".'<ul id="FAQTab">';
		$my_count 					= 0;
		foreach ($p_faq as $element){
			//echo '<pre>' . var_export($element, true) . '</pre>';
			$q 	= trim($element['question']);
			$a 	= trim($element['answer']);
			$q1 = $Secu->sanitizeForJsonOption($q);
			$a1 = $Secu->sanitizeForJsonOption($a);
				
			if (strlen($q) > 1 and strlen($a) > 1){
				$p_faq_html			.="<li>$q</li>";
				$p_faq_show_html 	.="<li><span id='question'><h2>$q</h2></span> - <span id='answer'><strong><h3>$a</h3></strong></span></li>";
				
				if ($my_count < $p_faq_count_entry - 1){	// -1 muss da so!
					$json_ld_faq .= <<<NAMEN1
						{
							"@type": "Question",
							"name": "$q1",
							"acceptedAnswer": {
							  "@type": "Answer",
							  "text": "$a1" 
							  }
						},
NAMEN1;
				} else {
					$json_ld_faq .= <<<NAMEN1
						{
							"@type": "Question",
							"name": "$q1",
							"acceptedAnswer": {
							  "@type": "Answer",
							  "text": "$a1" 
							  }
						}
NAMEN1;
					
				} // if ($my_count < $p_faq_count_entry){
			} // if (strlen($value) > 1){
			$my_count++;
		}; // foreach ($p_faq as $key => $value){
			
		$json_ld_faq .=	<<<NAMEN
]}</script>
NAMEN;

		$p_faq_html					.="</ul>";
		$p_faq_show_html			.="</ul>";
		
		$p_topics_html				= 'Social Media HashTags: <ol type="1">';
		$topics 					= explode(";",$p_topics);
		foreach ($topics as $element){
			if (strlen($element) > 1){
				$p_topics_html		.="<li>#$element</li>";
			} // if (strlen($value) > 1){
		}; // foreach ($p_faq as $key => $value){
		$p_topics_html				.="</ol>";

		$sent3_summary 	= $better_article['3_sentence_summary'];	
		$sentAI_summary = $better_article['end_ai_sentences'];				
		$h1_headl 		= $p_meta_headlines['h1'];
		$h2_headl 		= $p_meta_headlines['h2'];
		
		$ad_block		= $language_array[$p_textlanguage]['description'];
		$ad_block		= "<b><strong>$ad_block</b></strong>";
		
		$my_result_textblock = "";
		
		//START ERGEBNIS
		$my_result_textblock .=$as1;
		$my_result_textblock .="<title>$p_headline</title>";
		$my_result_textblock .="<h1>$h1_headl</h1>";
		$my_result_textblock .="<br />";
		$my_result_textblock .=$sent3_summary;													
		$my_result_textblock .="<br />";
		$my_result_textblock .="<h2>$h2_headl</h2>";
		$my_result_textblock .="<br />";
		$my_result_textblock .=$p_faq_show_html;
		$my_result_textblock .="<br />";
		$my_result_textblock .=$p_beautifytext;
		$my_result_textblock .="<br />";
		$my_result_textblock .=$sentAI_summary;
		$my_result_textblock .="<br /><br />";
		$my_result_textblock .=$p_topics_html;
		$my_result_textblock .="<br />";
		//$my_result_textblock .=$p_faq_show_html;
		//$my_result_textblock .="<br />";
		//$my_result_textblock .=$ad_block;
		//$my_result_textblock .="<br />";
		$my_result_textblock .=$json_ld_faq;
		//ENDE ERGEBNIS
		
		$my_result_textblock1 		= htmlentities($my_result_textblock, ENT_COMPAT, 'UTF-8');
		$tadditionalContentLinks	= $this->createAddLinkServiceAdvanced($p_language, $sessionID);
		$ecodedString 				= htmlentities($tadditionalContentLinks, ENT_QUOTES, 'UTF-8');
		$parse 						= parse_url($p_articleurl);
		$content 	= array_merge(
			array('robots'=>"index,follow,all"),
			array('title'=>$p_headline),
			array('description'=>$p_description),
			array('text'=>$p_beautifytext3 ."<br /><br />". $ecodedString),
			array('unique_text'=>$p_ai_text ."<br /><br />". $ecodedString),
			array('unique_score'=>$p_score_html),
			array('reading_time'=>$reading_time),
			array('language_text'=>$language_sprache_artikel[$p_lang]),
			array('lang'=>$p_lang),
			array('subkeyword'=>$p_subkeyword),
			array('mainkeyword'=>$p_mainkeyword),
			array('language'=>$p_language),
			array('summary'=>$p_summary),
			array('article_description'=>$p_description),
			array('simpletext'=>ucfirst($p_simpletext)),
			array('uniqueidentifier'=>$sessionID),
			array('headline'=>$p_headline),
			array('h1headlines'=>$H1HeadlineHTML),
			array('suchanfrage'=>$maintext),
			array('article_source'=>$p_articleurl),
			array('article_source_description'=>$parse['host']),
			array('structured_data_normal'=>$structured_data_normal),
			array('structured_data_ai'=>$structured_data_ai),
			array('structured_data_faq'=>$json_ld_faq),
			array('faq_data'=>$p_faq_show_html),
			array('full_seo_article'=>$my_result_textblock1 ."<br /><br />". $ecodedString),
			array('similar_content_create_article'=>$similarContent),
			array('og_datetime'=>$og_datetime),
			array('og_topics'=>$og_topics),
			array('og_main_topic'=>$tv1[0]),
			array('contentLinkNewDiv'=>"$tadditionalContentLinks"),
			array('structured_data_article'=>$structured_info),
			array('finished_processing'=>$finished_processing),
			array('topics'=>$descr_topics)
		);
		$pdo=null;
		return $content;
	} // public function makeMysqlCall($sessionID){
	
	public function prepareQuery(){
		$hostname		= "localhost";
		$dbname 		= "###";
		$username		= "###";
		$password		= "###";
		try {
			$db 			= new PDO("mysql:host=$hostname;dbname=$dbname;charset=utf8", $username, $password , array(PDO::ATTR_PERSISTENT => false)); //, array(PDO::ATTR_EMULATE_PREPARES => false, PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
		} catch (PDOException $e) {
			//throw new Exception('Could not connect to database');
			echo "artikelschreiber.com - cannot connect to database";
			return "";
		}
		return $db;
	} // function prepareQuery(){
	
	public function str_replace_first($from, $to, $content){
		$from = '/'.preg_quote($from, '/').'/';
		return preg_replace($from, $to, $content, 1);
	} // function str_replace_first($from, $to, $content){

	/**
	 * Returns an estimated reading time in a string
	 * idea from @link http://briancray.com/posts/estimated-reading-time-web-design/
	 * @param  string $content the content to be read
	 * @return string          estimated read time eg. 1 minute, 30 seconds
	 */
	public function estimate_reading_time($content) {
		$word_count = str_word_count(strip_tags($content));

		$minutes = floor($word_count / 200);
		$seconds = floor($word_count % 200 / (200 / 60));

		if (strcasecmp("","de")==0){
			$str_minutes = ($minutes == 1) ? "Minute" : "Minuten";
			$str_seconds = ($seconds == 1) ? "Sekunde" : "Sekunden";
		} else {
			$str_minutes = ($minutes == 1) ? "Minute" : "Minutes";
			$str_seconds = ($seconds == 1) ? "Second" : "Seconds";
		}
		if ($minutes == 0) {
			return "{$seconds} {$str_seconds}";
		}
		else {
			return "{$minutes} {$str_minutes}, {$seconds} {$str_seconds}";
		}
	} // function estimate_reading_time($content) {
		
	public function lesezeit($content, $p_textlanguage) {
		$word_count = str_word_count(strip_tags($content));

		$minutes = floor($word_count / 200);
		$seconds = floor($word_count % 200 / (200 / 60));

		if (strcasecmp($p_textlanguage,"de")==0){
			$str_minutes = ($minutes == 1) ? "Minute" : "Minuten";
			$str_seconds = ($seconds == 1) ? "Sekunde" : "Sekunden";
		} else {
			$str_minutes = ($minutes == 1) ? "Minute" : "Minutes";
			$str_seconds = ($seconds == 1) ? "Second" : "Seconds";
		}
		if ($minutes == 0) {
			return "{$seconds} {$str_seconds}";
		}
		else {
			return "{$minutes} {$str_minutes}, {$seconds} {$str_seconds}";
		}
	} // function estimate_reading_time($content) {
	
	public function getSingleValue($conn, $sql, $parameters){
		$q = $conn->prepare($sql);
		$q->execute($parameters);
		return $q->fetchColumn();
	} // function getSingleValue($conn, $sql, $parameters){
		
	public function getUpperCaseWords($text){
		$array_tocheck 	= array();
		$headl_list 	= explode(" ",$text);
		foreach($headl_list AS $word) {
		   $is_upper 	= preg_match('~^\p{Lu}~u', $word) ? 1 : 0;
		   if ($is_upper == 1 and ctype_alpha($word)){
			array_push($array_tocheck, $word);
		   } // if ($is_upper == 1 and ctype_alpha($word)){
		} // foreach($headl_list AS $word) {
		return $array_tocheck;
	} // function getUpperCaseWords($text){
	
	public function getLongTailKeywords($str, $len = 2, $min = 2){ 
	   $keywords = array();
	  $common = array('i','a','about','an','and','are','as','at','be','by','com','de','en','for','from','how','in','is','it','la','of','on','or','that','the','this','to','was','what','when','where','who','will','with','und','the','www');
	  //$str = preg_replace('/[^a-z0-9\s-]+/', '', strtolower(strip_tags($str)));
	  // $str = preg_replace('/[^a-z0-9\s-]+/', '', strip_tags($str));
	  $str = preg_split('/\s+-\s+|\s+/', $str, -1, PREG_SPLIT_NO_EMPTY);
	  while(0<$len--) for($i=0;$i<count($str)-$len;$i++){ 
		$word = array_slice($str, $i, $len+1);
		if(in_array($word[0], $common)||in_array(end($word), $common)) continue;
		$word = implode(' ', $word);
		if(!isset($keywords[$len][$word])) $keywords[$len][$word] = 0;
		$keywords[$len][$word]++;
	  }
	  $return = array();
	  foreach($keywords as &$keyword){
		$keyword = array_filter($keyword, function($v) use($min){ return !!($v>$min); });
		arsort($keyword);
		//if (strlen($keyword)>=12){
			$return = array_merge($return, $keyword);
		//}
	  }
	  return $return;
	} // public function getLongTailKeywords($str, $len = 2, $min = 2){ 

	public function isMainPortAvailable(){
		$host = '127.0.0.1';
		$port = 8080;	// fallback port: 3381
		$connection = @fsockopen($host, $port);
		if (is_resource($connection)){
			fclose($connection);
			return True;
		} // if (is_resource($connection)){
		fclose($connection);
		return False;
	} // public function checkMainPort(){
	
	//public function checkStopwordList($mainkw,$subkw){
	public function isWordInStopwordList($mainkw,$subkw){
		$stoplist 	= array();	// quelle: https://gist.github.com/ryanlewis/a37739d710ccdb4b406d
		//$stoplist 	= file('/home/www/wwwartikelschreiber/libraryv3/pornstopwordlist.txt');
		$stoplist 	= file('/home/www/wwwartikelschreiber/libraryv3/pornstopwordlist.txt');
		//$stoplist 	= array_map('trim', $stoplist);
		$mainkw		= trim(strtolower($mainkw));
		$subkw		= trim(strtolower($subkw));
		
		//var_dump($stoplist);
		foreach ($stoplist as $word){
			$word = trim(strtolower($word));
			//echo "'$word' and '$mainkw' und '$subkw'<br>";
			if (strlen($word) > 0 and stripos($word, '#') !== True){
				$pos1 = stripos($mainkw, $word);
				$pos2 = stripos($subkw, $word);
				//echo "$pos1 $mainkw match with $word<br />";
				//echo "$pos2 $subkw match with $word<br />";
				//var_dump($pos1); var_dump($pos2);
				if ($pos1 === True) {
					//echo "pos1 $mainkw match with $word<br />";
					//file_put_contents("/home/www/logs/ARTIKELSCHREIBER/porn.log", date("Y-m-d H:i:s") . " |$mainkw|mainkw porn Match\n", FILE_APPEND | LOCK_EX);
					return True;
				}
				if ($pos2 === True) {
					//echo "pos2 $subkw match with $word<br />";
					//file_put_contents("/home/www/logs/ARTIKELSCHREIBER/porn.log", date("Y-m-d H:i:s") . " |$subkw|subkw porn Match\n", FILE_APPEND | LOCK_EX);
					return True;
				}
			}; // if ((strlen($word) > 0){
		}; // foreach ($word in stoplist){
		return false;
	} // public function checkStopwordList($mainkw,$subkw){
	
	public function makeArticleSchreiberLink($mk, $sk){
		$p_link				= trim($mk)."!".trim($sk);
		$words				= implode(' ', array_slice(explode(' ',$p_link), 0, 18));
		$words				= str_replace(array('ä','ö','ü','ß','Ä','Ö','Ü'),array('ae','oe','ue','ss','Ae','Oe','Ue'),$words);  
		$words				= trim($words);
		$words				= str_replace(' ','-',$words);
		$words				= strtolower(preg_replace('/[^a-zA-Z0-9-!]/', '', trim($words)));
		return $words;
	} // function makeArticleLink($shortcode){
		
	public function makeArticleLinkArtikelSchreiber($shortcode){
		$pdo				= prepareQuery();
		$stmt 				= $pdo->prepare("SELECT p_mainkeyword,p_subkeyword FROM unaique_cache WHERE p_sessionid=:shortcode  LIMIT 1"); // AND 
		$stmt->bindValue(':shortcode', $shortcode, PDO::PARAM_STR);
		$stmt->execute();
		$rows 				= $stmt->fetchAll(PDO::FETCH_ASSOC);
		//$p_headline			= trim($rows["p_mainkeyword"])." ".trim($rows["p_subkeyword"]);
		$p_headline			= trim($rows[0]["p_mainkeyword"])." ".trim($rows[0]["p_subkeyword"]);
		$p_link				= trim($rows[0]["p_mainkeyword"])."!".trim($rows[0]["p_subkeyword"]);
		//echo "p_shortcode=$shortcode<br />";
		//echo "p_headline1=$p_headline<br />";
		//echo "p_headline2=$p_headline1<br />";
		//$p_headline		= preg_replace('/\s{1,}-\s{1,}/', ' ', trim($p_headline));
		//$p_headline		= str_replace('-','',$p_headline);
		$words				= implode(' ', array_slice(explode(' ',$p_link), 0, 18));
		//echo "words=$words<br />";
		$words				= str_replace(array('ä','ö','ü','ß','Ä','Ö','Ü'),array('ae','oe','ue','ss','Ae','Oe','Ue'),$words);  
		$words				= trim($words);
		$words				= str_replace(' ','-',$words);
		$words				= strtolower(preg_replace('/[^a-zA-Z0-9-!]/', '', trim($words)));
		
		$stmt 				= null; // doing this is mandatory for connection to get closed
		$pdo 				= null;
		
		//return "$words"."!"."$shortcode/";
		return $words;
	} // public function makeArticleLinkArtikelSchreiber($shortcode){
	
	public function file_get_contents_with_timeout($path, $timeout=3){
		// http://php.net/manual/de/function.file-get-contents.php
		$ctx = stream_context_create(array('http'=>
			array('timeout' => $timeout)  
		));
		return file_get_contents($path, false, $ctx);
	} // public function file_get_contents_with_timeout($path, $timeout = 30) {

	public function make7LOLArticleLink(){
	
		$pdo 				= new PDO("mysql:host=localhost;dbname=7lol;charset=utf8", "root","rouTer99");
		$table 				= "publish_de";
		
		$p_rand 			= (int)rand(1, 240000);
		$stmt 				= $pdo->prepare("SELECT p_headline, p_shortcode FROM $table WHERE id=:id AND p_isonline=:p_isonline LIMIT 1");
		$stmt->bindValue(':p_isonline', 1, PDO::PARAM_INT);
		$stmt->bindValue(':id', $p_rand, PDO::PARAM_INT);
		$stmt->execute();
		//echo "SELECT p_headline, p_shortcode FROM $table WHERE id=:id AND p_isonline=1 LIMIT 1";
		//echo "id: $p_rand";
		$rows 				= $stmt->fetchAll(PDO::FETCH_ASSOC);
		$p_headline			= trim($rows[0]["p_headline"]);
		$p_shortcode		= trim($rows[0]["p_shortcode"]);
		$stmt 				= null; // doing this is mandatory for connection to get closed
		$pdo 				= null;
		
		$arr_ret = array(
			"l" => "https://7lol.de/$p_shortcode.html",
			"a" => "https://7lol.de/$p_shortcode.amp.html",
			"h"	=> $p_headline,
		);
		return $arr_ret;
	} // public function make7LOLArticleLink(){
	
	public function getArticleHeadline($shortcode){
	
		$config 			= new Config();
		$conn 				= new Connection();
		$pdo				= $conn->prepareQuery();
		
		$table 				= $config->sql_tablename_publish_de();
		$stmt 				= $pdo->prepare("SELECT p_headline FROM $table WHERE p_shortcode=:shortcode AND p_isonline='1' LIMIT 1"); // AND 
		$stmt->bindValue(':shortcode', $shortcode, PDO::PARAM_STR);
		$stmt->execute();
		$rows 				= $stmt->fetchAll(PDO::FETCH_ASSOC);
		$p_headline			= trim($rows[0]["p_headline"]);
		
		/*
		$p_headline			= preg_replace('/\s{1,}-\s{1,}/', ' ', trim($p_headline));
		//$p_headline			= str_replace('-','',$p_headline);
		$words				= implode(' ', array_slice(explode(' ', $p_headline), 0, 18));
		$words				= str_replace(array('ä','ö','ü','ß','Ä','Ö','Ü','-'),array('ae','oe','ue','ss','Ae','Oe','Ue',''),$words);  
		$words				= trim($words);
		$words				= str_replace(' ','-',$words);
		$words				= strtolower(preg_replace('/[^a-zA-Z0-9-]/', '', trim($words)));
		*/
		$stmt 				= null;
		$pdo 				= null;
		
		return $p_headline;
	} // public function getArticleHeadline($shortcode){
	
	public function detectLanguage($input){
		// https://github.com/wikimedia/wikimedia-textcat
		$dir 		= "/home/www/wwwbuzzerstar/libraryv3/textcat/LM"; // later config file
		$options 	= "de,en";
		$lang 		= "de";
		
		$cat 		= new TextCat( $dir );
		$cat->setMaxNgrams( intval( 3000 ) );
		$cat->setMinFreq( intval( 0 ) );
		$result 	= $cat->classify( $input, explode( ",", $options ) );
		$max 		= reset( $result ) * 1.05;
		$result = array_filter( $result, function ( $res ) use( $max ) { return $res < $max;} );
		$retArray = array_keys($result);
		$lang 	  = $retArray[0];
		return $lang;
	} // public function detectLanguage($input){
	
	public function getAmazonContentAMP($search){
		return;
		
		$prime_ad_DE = '<a href="https://www.amazon.de/gp/prime/pipeline/landing?primeCampaignId=prime_assoc_ft&rw_useCurrentProtocol=1&tag=buzzerstar-21" rel="nofollow" target="_blank" title="Beschreibung: Jetzt Amazon Prime 30 Tage kostenlos testen">Jetzt Amazon Prime 30 Tage kostenlos testen</a>';
		
		$prime_ad_EN = '<a href="https://www.amazon.de/gp/prime/pipeline/landing?primeCampaignId=prime_assoc_ft&rw_useCurrentProtocol=1&tag=buzzerstar-21" rel="nofollow" target="_blank" title="Beschreibung: Jetzt Amazon Prime 30 Tage kostenlos testen">Jetzt Amazon Prime 30 Tage kostenlos testen</a>';
		
		$max_ad_results = 2;
		$current_count	= 0;
		
		$RelatedMoreContent = "";
		$RelatedMoreContent =<<<END
		$prime_ad_DE
END;

		//the category could also come from a GET if you wanted. 
		$category = "All"; 

		define('AWS_API_KEY', '###');
		define('AWS_API_SECRET_KEY', '####');
		define('AWS_ASSOCIATE_ID', 'buzzerstar-21');

		//declare the amazon ECS class
		$amazonEcs = new AmazonECS(AWS_API_KEY, AWS_API_SECRET_KEY, 'DE', AWS_ASSOCIATE_ID);

		//tell the amazon class that we want an array, not an object
		$amazonEcs->setReturnType(AmazonECS::RETURN_TYPE_ARRAY);

		//create the amazon object (array)
		$response = $amazonEcs->category($category)->responseGroup('Small,Images,Offers')->search($search);
		
		//check that there are items in the response
		if (isset($response['Items']['Item']) ) {

			//loop through each item
			foreach ($response['Items']['Item'] as $result) {
				
				//check that there is a ASIN code - for some reason, some items are not
				//correctly listed. Im sure there is a reason for it, need to check.
				if (isset($result['ASIN'])) {

					//store the ASIN code in case we need it
					$asin = $result['ASIN'];

					//check that there is a URL. If not - no need to bother showing
					//this one as we only want linkable items
										
					if (isset($result['DetailPageURL']) && $current_count < $max_ad_results ) {						
						$current_count++;
						$add_text 	= "";
						$detailurl 	= $result['DetailPageURL'];
						$title 		= $result['ItemAttributes']['Title'];
						$image 		= $result['MediumImage']['URL'];
						$hi 		= $result['SmallImage']['Height'][_];
						$wi 		= $result['SmallImage']['Width'][_]; 
						$ma 		= $result['ItemAttributes']['Manufacturer'];
						$pg 		= $result['ItemAttributes']['ProductGroup'];
						$lp 		= $result['OfferSummary']['LowestUsedPrice']['FormattedPrice'];
						$lnp 		= $result['OfferSummary']['LowestNewPrice']['FormattedPrice'];
						$pr 		= $result['Offer']['OfferListing']['IsEligibleForPrime']; 
						$pr_sav 	= $result['Offer']['OfferListing']['PercentageSaved']; 
						
						if (strlen($lp) <= 1){
							$lp = $lnp;
						}
						
						if ($pr == 1){
							$add_text = "- als <b>Prime Kunde</b> profitierst du von $pr_sav Prozent <strong>Ersparnis</strong>!";							
						}
						
						$title_amp = $this->clear_description($title);
						
						if (strlen($image) >= 10 && strlen($hi) >=2 && strlen($wi) >=2){
						
							$RelatedMoreContent .=<<<END
								<amp-img alt="$title_amp" src="$image" width="$wi" height="$hi" title="$title_amp - $ma - $pg" layout="responsive"></amp-img>
								<br />
								<a href="$detailurl" hreflang="de" rel="nofollow" target="_blank" title="Deutsche Zusammenfassung: $title_amp">$title_amp ($pg von $ma für $lp $add_text)</a>
								<br />
END;
						} // if (strlen($image) >= 10 && strlen($hi) >=2 && strlen($wi) >=2){
					
					} // if (isset($result['DetailPageURL'])
				} // if (isset($result['ASIN'])) {
			} // foreach ($response['Items']['Item'] as $result) {

		} else {

			//display that nothing was found - should no results be found
			//echo "<p  style='". IE_BACKGROUND . "'>No Amazon suggestions found</p>";

		} //

		return $RelatedMoreContent;
	} // public function getAmazonContentAMP($search){
		
	public function pushPictureToKeyCDN($shortcode){
	
		$config 			= new Config();
			
		$cdn_ftpusername 	= $config->cdn_ftpusername();
		$cdn_ftppassword 	= $config->cdn_ftppassword();
		$cdn_ftppath 		= $config->cdn_ftppath();
		$cdn_ftpserver 		= $config->cdn_ftpserver();
		
		//$ftp 				= new FTP($cdn_ftpusername, $cdn_ftppassword, $cdn_ftpserver, $cdn_ftppath);
		
		$pictureUri 		= "https://www.buzzerstar.com/image/$shortcode.png";
				
		$filename  			= "/tmp/$shortcode.png";
		unlink($filename);
		
		//echo "Downloading image to cdn.buzzerstar.com\n<br/>";
		$f	 				= @fopen($filename, 'w');
		$ch 				= curl_init();
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 2);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $pictureUri);
		curl_setopt($ch, CURLOPT_TIMEOUT, 50);
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT,50);
		curl_setopt($ch, CURLOPT_USERAGENT, "cdn.buzzerstar.com Image Loader v0.1");
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
		curl_setopt($ch, CURLOPT_AUTOREFERER, true);
		curl_setopt($ch, CURLOPT_BINARYTRANSFER, true);
		curl_setopt($ch, CURLOPT_HEADER, 0); 
		curl_setopt($ch, CURLOPT_FILE, $f);
		curl_exec($ch);
		if(curl_errno($ch)){
			echo 'Class Function - pushPictureToKeyCDN() -> error:' . curl_error($ch);
			echo "Error Downloading : ^$pictureUri^<br />";
		}
		curl_close($ch);
		fclose($f); 
			
		//echo "PNGCrush Image to cdn.buzzerstar.com\n<br/>";
		exec("/usr/local/bin/pngquant --quality=65-88 --speed 1 $filename -o $filename --force");
		
		chmod($filename, 0755);
		
		//echo "FTP Upload to cdn: $cdn_ftppath/$shortcode.png this file: $filename\n<br/>";
		//$ftp->upload("$cdn_ftppath/$shortcode.png",$filename);
		
	
		$conn_id = ftp_connect($cdn_ftpserver);

		// Login mit Benutzername und Passwort
		$login_result = ftp_login($conn_id, $cdn_ftpusername, $cdn_ftppassword);

		// Datei hochladen
		ftp_chdir($conn_id, $cdn_ftppath);
		if (ftp_put($conn_id, "$shortcode.png", $filename, FTP_BINARY)) {
		// echo "$filename erfolgreich hochgeladen\n";
		} else {
		 echo "Ein Fehler trat beim Hochladen von $filename auf -> Manuell auf CDN kopieren : $pictureUri <br />\n";
		}
		//var_dump($conn_id);

		// Verbindung schließen
		ftp_close($conn_id);
		
	
		return;
	}
		
	public function getJavaScriptInlineContent(){
		$buffer = "";
		$buffer .= file_get_contents("/home/www/wwwbuzzerstar/js-new/jquery-buzzerstar2016.js"); // 
		return "<script language=\"JavaScript\" type=\"text/javascript\" async>$buffer</script>";
	}
		
	public function getDeepLinkContent(){#new
		
		return;
		
		$RelatedMoreContent	= "";
		$ResultsArray		= array();
		
		$RelatedMoreContent =<<<END
		<div class="blog__post">
			<div class="post__info" lang="en">
END;

		$cache				= new FileCache();
		$key 				= 'getContent:RandomContent:BuzzerStarNet';
		
		if (!$content 		= $cache->fetch($key)) {
			$content 		= $this->get_html('https://www.buzzerstar.net/api.php?r=1');	
			$cache->store($key,$content,3600*24); // 1 tag cache
		}
		$ResultsArray		= explode("\n",$content);
		$count				= count($ResultsArray);
		for ( $ArrayCount=0; $ArrayCount<=2; $ArrayCount++ ) {
			$rand_f1 = rand(1,8);
			$rand_f2 = rand(10,60);
			list($shortcode,$headline,$keywords,$linkingcode,$sentences) = explode('###', $ResultsArray[$ArrayCount]);
		
			//echo "RA: $ResultsArray[$ArrayCount]<br>";
			
		$RelatedMoreContent .=<<<END
				<a itemprop="url" href="$linkingcode" hreflang="en" target="_blank" title="English Summary: $sentences" style="text-decoration: underline; ">
					<h2 class="heading--secondary">
						<mark style="color:#2196F3;"><strong>$headline</strong></mark>
					</h2>
				</a>
				<p class="post__paragraph">
					$sentences
					<br />
					Keywords of Article: $keywords
				</p>
END;
			
		} // for
		$RelatedMoreContent .=<<<END
					</div>
				</div>
END;
		return $RelatedMoreContent;
	}
	
	public function get_html($url) {#new
		$ch 		= curl_init();
		$timeout 	= 5;
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch,CURLOPT_SSL_VERIFYPEER,true); 
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
		$data = curl_exec($ch);
		curl_close($ch);
		return $data;
	}

	public function GetNewRelatedContent($searchInputFromShowPHP){
		
		$search 			= new Search();
		$SearchContent		= $search->SphinxSearch( $searchInputFromShowPHP );

		//echo "Sphinx in: $searchInputFromShowPHP";
		//print_r($SearchContent);
		
		$re = '/# Split sentences on whitespace between them.
			(?<=                # Begin positive lookbehind.
			  [.!?]             # Either an end of sentence punct,
			| [.!?][\'"]        # or end of sentence punct and quote.
			)                   # End positive lookbehind.
			(?<!                # Begin negative lookbehind.
			  Mr\.              # Skip either "Mr."
			| Mrs\.             # or "Mrs.",
			| Ms\.              # or "Ms.",
			| Jr\.              # or "Jr.",
			| Dr\.              # or "Dr.",
			| Prof\.            # or "Prof.",
			| Sr\.              # or "Sr.",
			| T\.V\.A\.         # or "T.V.A.",
			| [\d{1,}]
			| [0-9{1,}]
								# or... (you get the idea).
			)                   # End negative lookbehind.
			\s+                 # Split on whitespace between sentences.
			/ix';
		
		$RelatedMoreContent =<<<END
		<div class="blog__post">
			<div class="post__info" lang="de">
END;

		$imageRetArray 		= $this->getScreenResolutionFromUA($startpage);
		$x 					= $imageRetArray["x"];
		$y 					= $imageRetArray["y"];
		$fontsize 			= $imageRetArray["fontsize"];
		$picQuality 		= $imageRetArray["picQuality"];
				
		for ( $ArrayCount=1; $ArrayCount<=7; $ArrayCount++ ) {				
			
			$rand_f1 = rand(1,8);
			$rand_f2 = rand(10,60);
			
			list( $headline,$shortcode,$article1,$pic_desc) = explode('#####', $SearchContent[$ArrayCount] );
			if (strlen($headline)<10){
				break 1;
			}
			
			$shortcode			= trim($shortcode);
			$headline			= trim($headline);
			$pic_desc			= trim($pic_desc);
			//$article 			= substr($article1,0,125).' ...';
			$articleLink		= "https://www.buzzerstar.com/".$this->makeArticleLink($shortcode);
			$sentences 			= preg_split($re, $article1, -1, PREG_SPLIT_NO_EMPTY);

			$RelatedMoreContent .=<<<END
				<a itemprop="url" href="$articleLink" hreflang="de" title="Deutsche Zusammenfassung: $headline - $sentences[0]" style="text-decoration: underline; ">
					<h2 class="heading--secondary">
						<mark style="color:#2196F3;"><strong>$headline</strong></mark>
					</h2>
				</a>
				<p class="post__paragraph">
					$sentences[0] $sentences[1]
				</p>
END;

		}
	
		$RelatedMoreContent .=<<<END
					</div>
				</div>
END;
		return $RelatedMoreContent;
	}
			
	public function getIndexNewInlineCSS(){
		$css = new Minifier();
		
		$buffer = "";
		$buffer .= file_get_contents("/home/www/wwwbuzzerstar/cssv3/main.min.css");
		$buffer .= file_get_contents("/home/www/wwwbuzzerstar/cssv3/jssocials.min.css");
		$buffer .= file_get_contents("/home/www/wwwbuzzerstar/cssv3/jssocials-theme-classic.min.css");
		
		// Minifier anwenden
		$buffer = $css->minifyCSS($buffer);
		
		//Remove comments
		$buffer = preg_replace('!/\*[^*]*\*+([^/][^*]*\*+)*/!', '', $buffer);
		
		//Remove space after colons
		$buffer = str_replace(": ", ":", $buffer);
		
		//Remove whitespace
		$buffer = str_replace(array("\r\n", "\r", "\n", "\t", '  ', '    ', '    '), '', $buffer);
		
		return "<style rel=\"stylesheet\" type=\"text/css\" media=\"all\">$buffer</style>";
	}
	
	//http://darcyclarke.me/development/get-image-for-youtube-or-vimeo-videos-from-url/
	public function getLinks($text){
		if(filter_var($text, FILTER_VALIDATE_URL))
		{
			//echo "Yes it is url";
			//exit; // die well
			return array(1,$text);
		//} else {
			//echo "No it is not url";
			//return array(0,0);
			// my else codes goes
		}
		
		$regex = "((https?|ftp)\:\/\/)?"; // SCHEME 
		$regex .= "([a-z0-9+!*(),;?&=\$_.-]+(\:[a-z0-9+!*(),;?&=\$_.-]+)?@)?"; // User and Pass 
		$regex .= "([a-z0-9-.]*)\.([a-z]{2,3})"; // Host or IP 
		$regex .= "(\:[0-9]{2,5})?"; // Port 
		$regex .= "(\/([a-z0-9+\$_-]\.?)+)*\/?"; // Path 
		$regex .= "(\?[a-z+&\$_.-][a-z0-9;:@&%=+\/\$_.-]*)?"; // GET Query 
		$regex .= "(#[a-z_.-][a-z0-9+\$_.-]*)?"; // Anchor 

		if(preg_match("/^$regex$/", $text)) 
		{ 
			return array(1,$text);
		} 
		
		// The Regular Expression filter
		$reg_exUrl = "/(http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,6}(\/\S*)?/";

		// Check if there is a url in the text
		if(preg_match($reg_exUrl, $text, $url)) {
			return array(1, $url[0]);
			// make the urls hyper links
			// echo preg_replace($reg_exUrl, "<a href="{$url[0]}">{$url[0]}</a> ", $text);
		//} else {
			// if no urls in the text just return the text
		//	return array(0,0);
		}
		return array(0,0);
	}

	public function getScreenResolutionFromUA(){
		
		$returnvalues 		= array();
		
		$detect 			= new Mobile_Detect;
		$deviceTypeMobile 	= $detect->isMobile();
		$deviceTypeTablet 	= $detect->isTablet();
		
		//320x240, 480x320, 800x480, 960x480, 1024x800, and 1024x768
		$picQuality = 55;

		if (strpos($startpage, '1') !== FALSE){
			$x = 320;
			$y = 260;
			$xImage = 320;
			$yImage = 260;
			$fontsize = 9;
			$picQuality = 35;
		} elseif (strpos($startpage, '2') !== FALSE){
			$x = 60;
			$y = 75;
			$xImage = 60;
			$yImage = 75;
			$fontsize = 7;
			$picQuality = 35;
		} elseif ($deviceTypeTablet === TRUE){
			// we have a tablet device
			$x = 540; 
			$y = 320;
			$xImage = 460;
			$yImage = 320;
			$fontsize = 12;
			$picQuality = 45;
		} elseif ($deviceTypeMobile === TRUE){
			// we have a mobile device
			$x = 320;
			$y = 260;
			$xImage = 420;
			$yImage = 360;
			$fontsize = 10;
			$picQuality = 41;
		} else {
			// we have a desktop device
			$x = 640;
			$y = 480;
			$xImage = 620;
			$yImage = 480;
			/*
			$xImage = 540;
			$yImage = 430;
			*/
			$fontsize = 15;
			$picQuality = 53;
		}
		/*
		if(strstr(strtolower($_SERVER['HTTP_USER_AGENT']), "google")){
			$x = 480;
			$y = 320;
			$xImage = 480;
			$yImage = 320;
			$fontsize = 12;
			$picQuality = 65;
		}
		*/
		$returnvalues["x"] = $x;
		$returnvalues["y"] = $y;
		$returnvalues["xImage"] = $xImage;
		$returnvalues["yImage"] = $yImage;
		$returnvalues["fontsize"] = $fontsize;
		$returnvalues["picQuality"] = $picQuality;
		
		return $returnvalues;
	}

// embedding code: <iframe width="640" height="390" src="http://www.youtube.com/embed/G1aWk9Y9cMA" frameborder="0" allowfullscreen></iframe>

	public function request_headers() {
	  $arh = array();
	  $rx_http = '/\AHTTP_/';
	  foreach($_SERVER as $key => $val) {
		if( preg_match($rx_http, $key) ) {
		  $arh_key = preg_replace($rx_http, '', $key);
		  $rx_matches = array();
		  // do some nasty string manipulations to restore the original letter case
		  // this should work in most cases
		  $rx_matches = explode('_', $arh_key);
		  if( count($rx_matches) > 0 and strlen($arh_key) > 2 ) {
			foreach($rx_matches as $ak_key => $ak_val) $rx_matches[$ak_key] = ucfirst($ak_val);
			$arh_key = implode('-', $rx_matches);
		  }
		  $arh[$arh_key] = $val;
		}
	  }
	  return( $arh );
	}

	public function clear_description($description_text){		
		
		$description_text = trim(substr($description_text, 0, 142));
		$description_text = str_replace(array('ä','ö','ü','ß','Ä','Ö','Ü',' '),array('ae','oe','ue','ss','Ae','Oe','Ue',' '),$description_text);
		$description_text = strip_tags($description_text);
		$trans = array('-' => ' ');
		$description_text = strtr($description_text, $trans);
		$description_text = preg_replace("/[^a-zA-Z0-9\s\.\!\?\,\;]/", '', $description_text);

		return $description_text;
	}

	public function clear_string($str, $how = ' '){
		$search = array("ä", "ö", "ü", "ß", "Ä", "Ö", 
						"Ü", "&", "é", "á", "ó", 
						" :)", " :D", " :-)", " :P", 
						" :O", " ;D", " ;)", " ^^", 
						" :|", " :-/", ":)", ":D", 
						":-)", ":P", ":O", ";D", ";)", 
						"^^", ":|", ":-/", "(", ")", "[", "]", 
						"<", ">", "!", "\"", "§", "$", "%", "&", 
						"/", "(", ")", "=", "?", "`", "´", "*", "'", 
						"_", ":", ";", "²", "³", "{", "}", 
						"\\", "~", "#", "+", ".", ",", 
						"=", ":", "=)");
		$replace = array("ae", "oe", "ue", "ss", "Ae", "Oe", 
						 "Ue", "und", "e", "a", "o", "", "", 
						 "", "", "", "", "", "", "", "", "", 
						 "", "", "", "", "", "", "", "", "", 
						 "", "", "", "", "", "", "", "", "", 
						 "", "", "", "", "", "", "", "", "", 
						 "", "", "", "", "", "", "", "", "", 
						 "", "", "", "", "", "", "", "", "", "");
		$str = str_replace($search, $replace, $str);
		//$str = strtolower(preg_replace("/[^a-zA-Z0-9]+/", trim($how), $str));
		return $str;
	}

	public function sendKontaktformularMail($nachricht){

		$empfaenger = '#####';
		$betreff = 'Neue Kontaktanfrage über das BuzzerStar.com Kontaktformular am '.date("d-m-Y h:i:sa");

		$header  = 'MIME-Version: 1.0' . "\r\n";
		$header .= 'Content-type: text/html; charset=utf-8' . "\r\n";
		$header .= 'To: Sebastian Enger <########>'. "\r\n";
		$header .= 'From: BuzzerStar-New Article <kontaktformular@buzzerstar.com>' . "\r\n";

		mail($empfaenger, $betreff, $nachricht, $header);

	} // public function sendKontaktformularMail($nachricht){

	public function getTextBetweenTags($string, $start, $end){
    
		$start	= trim($start);
		$end	= trim($end);
		$result = array();
		$string = " ".trim($string);
		$offset = 0;
		
		while(true){
			$ini = strpos($string,$start,$offset);
			if ($ini == 0)
				break;
			$ini += strlen($start);
			$len = strpos($string,$end,$ini) - $ini;
			$result[] = trim(substr($string,$ini,$len));
			$offset = $ini+$len;
		}
		return $result;
	}

	public function autolink($str, $attributes=array()) {
		$attrs = '';
		foreach ($attributes as $attribute => $value) {
			$attrs .= " {$attribute}=\"{$value}\"";
		}
		$parse = parse_url($str);
		$str = ' ' . $str;
		$domainname = $parse['host']; 

		$str = preg_replace(
			'`([^"=\'>])((http|https|ftp|mailto)://[^\s<]+[^\s<\.)])`i',
			'$1<a href="$2" class="tunder"'.$attrs.">[Link: $domainname]</a>",
			$str
		);
		$str = substr($str, 1);
		
		return $str;
	}
	/*
	public function autolink($str, $attributes=array()) {
		$attrs = '';
		foreach ($attributes as $attribute => $value) {
			$attrs .= " {$attribute}=\"{$value}\"";
		}

		$str = ' ' . $str;
		$str = preg_replace(
			'`([^"=\'>])((http|https|ftp|mailto)://[^\s<]+[^\s<\.)])`i',
			'$1<a href="$2"'.$attrs.'>$2</a>',
			$str
		);
		$str = substr($str, 1);
		
		return $str;
	}
	*/

	public function getNavigationContent($searchInputFromShowPHP){
		//echo "Search for $searchInputFromShowPHP<br />";
			
		$search 			= new Search();
		$SearchContent		= $search->SphinxSearch( $searchInputFromShowPHP );
	//	echo "DEBUG: Sphinx Intelligent Related Result Count:" . count($SearchContent). "<br /";
	//	print_r($SearchContent);
		
		$imageRetArray 		= $this->getScreenResolutionFromUA($startpage);
		$x 					= $imageRetArray["x"];
		$y 					= $imageRetArray["y"];
		$fontsize 			= $imageRetArray["fontsize"];
		$picQuality 		= $imageRetArray["picQuality"];

		$MyAdContent =<<<END
			<div id="set_border">
				<a target="_blank" href="http://www.amazon.de/b?_encoding=UTF8&camp=1638&creative=6742&linkCode=ur2&node=562066&site-redirect=de&tag=buzzerstar-21&linkId=65PDFW4KUUMHBJ3E" rel="nofollow" class="url" itemprop="url" id="transform">Gönn dir endlich mal wieder was und geh Shoppen!</a><img src="http://ir-de.amazon-adsystem.com/e/ir?t=buzzerstar-21&l=ur2&o=3" width="1" height="1" border="0" alt="" style="border:none !important; margin-left: 23px; !important;" />
				<p />
				<iframe src="https://rcm-eu.amazon-adsystem.com/e/cm?t=buzzerstar-21&o=3&p=12&l=bn1&mode=ce-de&browse=562066&fc1=000000&lt1=_blank&lc1=3366FF&bg1=FFFFFF&f=ifr" marginwidth="0" marginheight="0" width="300" height="250" border="0" frameborder="0" style="border:none; margin-top: 15px; margin-left: 23px;" scrolling="no"></iframe>
				<p />
				Klickt euch bei Amazon rein und gönnt euch endlich mal wieder was. Ihr habt es euch verdient. Als Fan von BuzzerStar solltest Du auch mal wieder an Dich denken - Du bist der wichtigste Mensch der Welt.
			</div>
END;

		if (count($SearchContent) >= 1){
			
			$ReturnHTMLContent =<<<END
				Noch mehr coole und unglaubliche Neuigkeiten: <p />
			<ul>
				<li>
				<div id="set_border">
					<a href="https://www.buzzerstar.com/" hreflang="de" title="BuzzerStar News Community" class="url" itemprop="url"><figure itemtype="http://schema.org/ImageObject"><img src="https://www.buzzerstar.com/images/logo_header.png" itemprop="image" alt="BuzzerStar.com Logo - Willkommen auf der News Publishing Plattform, bei der du einen Artikel schreibst und einen Backlink bekommst" title="BuzzerStar - Werde zum Journalisten und veröffentliche deine eigene Storys auf deiner News Plattform" />
					<figcaption>Suchbox: Schau hier nach weiteren spannenden Nachrichten:</figcaption>
					</figure></a>
				
					<!-- main navigation -->
					<nav id="topnav" role="navigation">
						<ol>
							<li>
								<form>
									<input type="text" class="search" id="searchid" placeholder="Suchbegriff eingeben: " /><p /> 
									<input type="reset" id="reset" value="Suche löschen" />
									<div id="result"></div>
								</form>
							</li>
						</ol>
					</nav>
				<div class="clear"></div>
				</div>
				</li>
	
END;
			$myccount = 0;
			$random = rand(0,4);
			for ( $ArrayCount=0; $ArrayCount<=4; $ArrayCount++ ) {
							
				list( $headline,$shortcode, $article1 ) = explode('#####', $SearchContent[$ArrayCount] );
				$shortcode			= trim($shortcode);
				$headline			= trim($headline);
				$article 			= substr($article1,0,125).' ...';
				$articleLink		= "https://www.buzzerstar.com/".$this->makeArticleLink($shortcode);
			
				if ( $myccount == 0 ){
					$ReturnHTMLContent .= "<li>";
				}
				if ( $myccount == 2 ){
					$ReturnHTMLContent .= "</li>";
					$myccount = 0;
				}
				
			//	if ($random == $ArrayCount){
			//		$ReturnHTMLContent .= $MyAdContent;
			//	}			

				$ReturnHTMLContent .=<<<END
					<div id="set_border">
						<a href="$articleLink" class="url" itemprop="url" id="transform" title="Lies hier den Artikel $headline auf www.BuzzerStar.com">
						<figure itemtype="http://schema.org/ImageObject">
							<img class="lazy" data-original="https://www.buzzerstar.com/i.php?s=$shortcode" width="$x" height="$y" itemprop="image" alt="Kostenlose Bild zum downloaden, teilen und lachen: $picdescr" lazyload="1" />
							<noscript><img src="https://www.buzzerstar.com/i.php?s=$shortcode" width="$x" height="$y" itemprop="image" alt="Bildbeschreibung: $picdescr" title="Bildbeschreibung: $picdescr" lazyload="1" /></noscript>
							<figcaption>$headline</figcaption>
						</figure>
						</a>
						$article
						<div class="clear"></div>
					</div>
END;
			} // for ( $ArrayCount=0; $ArrayCount<=count($SearchContent) - 1; $ArrayCount++ ) {
			
			$ReturnHTMLContent .= "</ul>";
			$myccount++;
			

			return $ReturnHTMLContent;
			
		} else { // if (count($SearchContent) >= 1){
		
			$config 			= new Config();
			$conn 				= new Connection();
			$pdo				= $conn->prepareQuery();
			$table 				= $config->sql_tablename_publish_de();
			
			$stmt1 = $pdo->query("SELECT id FROM $table WHERE id>0 LIMIT 5000;");
			$randomMax = $stmt1->rowCount();
		
			$docids = array();
			mt_srand ((double)microtime()*1000000);
			for ($i=0;$i<=5;$i++){
				array_push($docids,mt_rand(1,$randomMax));
			}
			
			$SqlQuery	= "SELECT p_headline,p_shortcode,p_picture_1_description FROM $table WHERE";
			for ($i=0;$i<=count($docids) - 1;$i++){
				if ($i>0){
					$SqlQuery .= "\"$docids[$i]\",";
				} elseif($i<=0){
					$SqlQuery .= " `id` IN (\"$docids[$i]\",";
				};
			};
			$SqlQuery = substr($SqlQuery,0,(strlen($SqlQuery)-1));
			$SqlQuery .=") AND p_isonline=1 ORDER BY p_timestamp DESC LIMIT 5;";
				
			$stmt2 = $pdo->prepare($SqlQuery); // AND p_online=1
			$stmt2->execute();
			
			$ReturnHTMLContent =<<<END
				Noch mehr coole und unglaubliche Neuigkeiten (D): <p />
				<ul>
END;
			
			$myccount = 0;
			while($rows = $stmt2->fetch(PDO::FETCH_ASSOC)) {
			
				$headline			= $rows["p_headline"];
				$shortcode			= $rows["p_shortcode"];
				$picdescr			= $rows["p_picture_1_description"];
				$headline_print 	= substr($headline,0,85).' ...';
				//$picdescr_print 	= substr($picdescr,0,45).' ...';
				$articleLink		= "https://www.buzzerstar.com/".$this->makeArticleLink($shortcode);

				if ( $myccount == 0 ){
					$ReturnHTMLContent .= "<li>";
				}
				if ( $myccount == 2 ){
					$ReturnHTMLContent .= "</li>";
					$myccount = 0;
				}
				$myccount++;
				
	$ReturnHTMLContent .=<<<END
				<div id="set_border">
					<a href="$articleLink" class="url" itemprop="url" id="transform" title="Lies hier den Artikel $headline auf www.BuzzerStar.com">
					<figure itemtype="http://schema.org/ImageObject">
						<img src="https://www.buzzerstar.com/i.php?s=$shortcode" itemprop="image" alt="Kostenlose Bild Beschreibung: $picdescr" />
						<figcaption>$headline_print</figcaption>
					</figure>
					</a>
				</div>
END;
			
			} // while($rows = $stmt2->fetch(PDO::FETCH_ASSOC)) {
		
			$ReturnHTMLContent .= "</ul>";

			$stmt = null; 
			$pdo = null;
			
			return $ReturnHTMLContent;
		} // else if count sphinxsearch
	}

	public function ogTagsYoutubeVideo($string){
		if (stripos($string,'&') === TRUE ){
			list($string,$tmp) = explode('&',$string);
		}
		list($yt,$yt_ID) = explode('v=',$string);
		//return "https://www.youtube.com/v/$yt_ID?version=3&autohide=1";
		return "https://www.youtube.com/embed/$yt_ID";
	}

	public function buildCategoryLink($id){
		$idName = $this->categoryIDtoName($id);
		return "https://www.buzzerstar.com/kategorie/".ucfirst($idName);
	}
	
	public function categoryIDtoName($category_id){
		$config 			= new Config();
		$catg_array			= $config->array_category();
		
		if (is_numeric($category_id)){
			return $catg_array[$category_id];
		} else {
			return; // fallback
		}		
	}
	
	public function categoryNametoID($category_id){
		$config 			= new Config();
		$catg_array			= $config->array_category();
		
		if ( !is_numeric($category_id)) {
			return array_search(strtolower($category_id),array_map('strtolower',$catg_array)); 
		} else {
			return $catg_array[$category_id];
		}
	}

	public function getPostForCategory($id){
	
		$config 			= new Config();
		$conn 				= new Connection();
		
		$pdo				= $conn->prepareQuery();
		$table 				= $config->sql_tablename_publish_de();

		$catg_array			= $config->array_category();
		if ( !is_numeric($id)) {
			//$id = array_search($id, $catg_array);
			$id = array_search(strtolower($id),array_map('strtolower',$catg_array)); 
		}
		
		$stmt 				= $pdo->prepare("SELECT * FROM $table WHERE id>0 AND p_isonline=1 AND p_category=:p_category ORDER BY p_timestamp DESC;");
		$stmt->bindValue(':p_category', $id, PDO::PARAM_INT);
		$stmt->execute();
		$retVal = $stmt->rowCount();
		
		$stmt 				= null; // doing this is mandatory for connection to get closed
		$pdo 				= null;

		$stmt = null; 
		$pdo = null;
		
		if (!is_numeric($retVal)){
			return 0;
		} else {
			return $retVal;
		}
	}

	public function sendmyMail($autor, $headline){

		$empfaenger = '#######';

		// Betreff
		$betreff = 'Neuer Artikel auf BuzzerStar fertig zur Administration '.date("d-m-Y h:i:sa");

	// Nachricht
		$nachricht =<<<END
			<html>
			<head>
			  <title>$betreff</title>
			</head>
			<body>
			Betreff: $betreff<br />
			Autor: $autor<br />
			Schlagzeile: <a href="https://www.buzzerstar.com/manage/">$headline</a><br />
			<br /><br />
			</body>
			</html>
END;

		$header  = 'MIME-Version: 1.0' . "\r\n";
		$header .= 'Content-type: text/html; charset=utf-8' . "\r\n";

		// zusätzliche Header
		$header .= 'To: Sebastian Enger <#####>'. "\r\n";
		$header .= 'From: BuzzerStar-New Article <noreply@buzzerstar.com>' . "\r\n";

		// verschicke die E-Mail
		mail($empfaenger, $betreff, $nachricht, $header);

	} // public function sendmail($autor, $headline){

	public function getDuration(){

		$minute 		= rand(1,6);
		$seconds 		= rand(10,60);
		return "PT".$minute."M".$seconds."S";

	}
	
	public function makeArticleLinkTest($shortcode){
	
		$config 			= new Config();
		$conn 				= new Connection();
		$pdo				= $conn->prepareQuery();
		
		$table 				= $config->sql_tablename_publish_de();
		$stmt 				= $pdo->prepare("SELECT p_headline FROM $table WHERE p_shortcode=:shortcode AND p_isonline='1' LIMIT 1"); // AND 
		$stmt->bindValue(':shortcode', $shortcode, PDO::PARAM_STR);
		$stmt->execute();
		$rows 				= $stmt->fetchAll(PDO::FETCH_ASSOC);
		$p_headline			= trim($rows[0]["p_headline"]);
		$p_headline			= preg_replace('/\s{1,}-\s{1,}/', ' ', trim($p_headline));
		$words				= implode(' ', array_slice(explode(' ', $p_headline), 0, 18));
		$words				= str_replace(array('ä','ö','ü','ß','Ä','Ö','Ü','-'),array('ae','oe','ue','ss','Ae','Oe','Ue',''),$words);  
		$words				= trim($words);
		$words				= str_replace(' ','-',$words);
		$words				= strtolower(preg_replace('/[^a-zA-Z0-9-]/', '', trim($words)));
		
		$stmt 				= null; // doing this is mandatory for connection to get closed
		$pdo 				= null;
				
		return "$words-$shortcode.html";
	}
	
	
	public function makeArticleLink($shortcode){
	
		$config 			= new Config();
		$conn 				= new Connection();
		$pdo				= $conn->prepareQuery();
		
		$table 				= $config->sql_tablename_publish_de();
		$stmt 				= $pdo->prepare("SELECT p_headline FROM $table WHERE p_shortcode=:shortcode AND p_isonline='1' LIMIT 1"); // AND 
		$stmt->bindValue(':shortcode', $shortcode, PDO::PARAM_STR);
		$stmt->execute();
		$rows 				= $stmt->fetchAll(PDO::FETCH_ASSOC);
		$p_headline			= trim($rows[0]["p_headline"]);
		$p_headline			= preg_replace('/\s{1,}-\s{1,}/', ' ', trim($p_headline));
		//$p_headline			= str_replace('-','',$p_headline);
		$words				= implode(' ', array_slice(explode(' ', $p_headline), 0, 18));
		$words				= str_replace(array('ä','ö','ü','ß','Ä','Ö','Ü','-'),array('ae','oe','ue','ss','Ae','Oe','Ue',''),$words);  
		$words				= trim($words);
		$words				= str_replace(' ','-',$words);
		$words				= strtolower(preg_replace('/[^a-zA-Z0-9-]/', '', trim($words)));
		
		$stmt 				= null; // doing this is mandatory for connection to get closed
		$pdo 				= null;
		
		return "$words-$shortcode.html";
	}
	
	public function GetLanguageFromString($string){
	/*
		try{  
			$l = new Text_LanguageDetect();  
			$l->setNameMode(2); //return 2-letter language codes only  
			$result = $l->detect($string, 4);  
			//return array_keys(strtolower($result[0]));
			$ret = array_keys($result)[0];
			return strtolower($ret);
			//print_r($result) ;
		}  
		catch (Text_LanguageDetect_Exception $e)   
		{     
		  
		}
		*/
		return "de";
	}

	public function file_put_contents_atomic($filename, $content) { 
	 
		define("FILE_PUT_CONTENTS_ATOMIC_TEMP", dirname(__FILE__)."/cache"); 
		define("FILE_PUT_CONTENTS_ATOMIC_MODE", 0777); 
	
		if (!is_dir(FILE_PUT_CONTENTS_ATOMIC_TEMP)) {
			mkdir( FILE_PUT_CONTENTS_ATOMIC_TEMP, 0777, true );
		}		
		$temp = tempnam(FILE_PUT_CONTENTS_ATOMIC_TEMP, 'temp'); 
		if (!($f = @fopen($temp, 'w'))) { 
			$temp = FILE_PUT_CONTENTS_ATOMIC_TEMP . DIRECTORY_SEPARATOR . uniqid('temp'); 
			if (!($f = @fopen($temp, 'w'))) { 
				trigger_error("file_put_contents_atomic() : error writing temporary file '$temp'", E_USER_WARNING); 
				return false; 
			} 
		} 
	   
		fwrite($f, $content); 
		fclose($f); 
	   
	  	if (!rename($temp, $filename)) { 
			unlink($filename); 
			rename($temp, $filename); 
		} 
		
		chmod($filename, FILE_PUT_CONTENTS_ATOMIC_MODE); 
		return true; 
	   
	} 

	public function randomString(){
		
		$internLength 	= 1024;
		$chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
		$str = "";    

		for ($i = 0; $i < $internLength; $i++) {
			$str .= $chars[mt_rand(0, strlen($chars) - 1)];
		}
		return md5(uniqid(rand(), true).$str.mt_rand());
	}

	public function uniqueID($in){
	
		require_once("/home/www/wwwartikelschreiber/libraryv3/Config.inc.php"); 
		$config = new Config();
		
		//set the random id length 
		$random_id_length = $config->max_unique_id(); 
		
		$chars 	= "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
		$md5c 	= md5($in);
		$c 		= uniqid(rand(), true);
		
		//generate a random id encrypt it and store it in $rnd_id 
		$rnd_id = md5(uniqid(rand(),true).mt_rand(0, strlen($chars) - 1).$chars.$in.$md5c.$c.time()); 

		//to remove any slashes that might have come 
		$rnd_id = strip_tags(stripslashes($rnd_id)); 

		//Removing any . or / and reversing the string 
		$rnd_id = str_replace(".","",$rnd_id); 
		$rnd_id = strrev(str_replace("/","",$rnd_id)); 

		//finally I take the first $random_id_length characters from the $rnd_id 
		return substr($rnd_id,0,$random_id_length); 
	}
	
	public function alphaID($in, $to_num = false, $pad_up = false, $pass_key_in){
				
		$out   = '';
		$index = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
		$base  = strlen($index);

		if ($pass_key_in !== null) {
			// Although this function's purpose is to just make the
			// ID short - and not so much secure,
			// with this patch by Simon Franz (http://blog.snaky.org/)
			// you can optionally supply a password to make it harder
			// to calculate the corresponding numeric ID

			for ($n = 0; $n < strlen($index); $n++) {
				$i[] = substr($index, $n, 1);
			}

			$pass_hash = hash('sha512',$pass_key_in);
			$pass_hash = (strlen($pass_hash) < strlen($index) ? hash('sha512', $pass_key) : $pass_hash);

			for ($n = 0; $n < strlen($index); $n++) {
				$p[] =  substr($pass_hash, $n, 1);
			}

			array_multisort($p, SORT_DESC, $i);
			$index = implode($i);
		}

		if ($to_num) {
			// Digital number  <<--  alphabet letter code
			$len = strlen($in) - 1;

			for ($t = $len; $t >= 0; $t--) {
				$bcp = bcpow($base, $len - $t);
				$out = $out + strpos($index, substr($in, $t, 1)) * $bcp;
			}

			if (is_numeric($pad_up)) {
				$pad_up--;

				if ($pad_up > 0) {
					$out -= pow($base, $pad_up);
				}
			}
		} else {
			// Digital number  -->>  alphabet letter code
			if (is_numeric($pad_up)) {
				$pad_up--;

				if ($pad_up > 0) {
					$in += pow($base, $pad_up);
				}
			}

			for ($t = ($in != 0 ? floor(log($in, $base)) : 0); $t >= 0; $t--) {
				$bcp = bcpow($base, $t);
				$a   = floor($in / $bcp) % $base;
				$out = $out . substr($index, $a, 1);
				$in  = $in - ($a * $bcp);
			}
		}

		return strtolower($out);
	}

	public function stripHtml($string){
		
		$config = new Config();
			
		$sql_code = array ( 
			'SELECT', 
			'UPDATE', 
			'DELETE', 
			'INSERT', 
			'VALUES', 
			'FROM', 
			'LEFT', 
			'JOIN', 
			'WHERE', 
			'LIMIT', 
			'ORDER BY', 
			'DESC'
		  );
						  
		$content = strip_tags($string,$config->allow_content_tags());
		//$content = preg_replace('/<[^>]*>/', '', $content);
		$content = str_ireplace($sql_code,'',$content);
		
		return trim($content);
	}

	public function isVideoLink($string){
		
		$video_title		= "";
		$SSDTube 			= new SSDTube();
		$SSDTube->identify($string);
		$video_title		= $SSDTube->title;
		$regYoutube = "/^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/i";
		
		//if ( strlen($video_title)>=5||preg_match('/(\w{5,})/i',$video_title)){
		if ( strlen($video_title)>=3 || preg_match($regYoutube,$string)){	
			return 1;
		} else {
			return 0;
		}
		
		//$regYoutube = "/^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/i";
		//$regYoutube = "/^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/";
		//$regVimeo = "/^.*(vimeo\.com\/)((channels\/[A-z]+\/)|(groups\/[A-z]+\/videos\/))?([0-9]+)/";
		//$regDailymotion = "/^.+dailymotion.com\/(video|hub)\/([^_]+)[^#]*(#video=([^_&]+))?/";
		//$regMetacafe = "/^.*(metacafe\.com)(\/watch\/)(\d+)(.*)/i";
		/*
		if (preg_match($regYoutube,$string) ){
			return 1;
		} else {
			return 0;
		}
		*/
	}
	
	// HTML Minifier
public function minify_html($input) {
    if(trim($input) === "") return $input;
    // Remove extra white-spaces between HTML attributes
    $input = preg_replace_callback('#<([^\/\s<>!]+)(?:\s+([^<>]*?)\s*|\s*)(\/?)>#s', function($matches) {
        return '<' . $matches[1] . preg_replace('#([^\s=]+)(\=([\'"]?)(.*?)\3)?(\s+|$)#s', ' $1$2', $matches[2]) . $matches[3] . '>';
    }, $input);
    // Minify inline CSS declarations
    if(strpos($input, ' style=') !== false) {
        $input = preg_replace_callback('#\s+style=([\'"]?)(.*?)\1(?=[\/\s>])#s', function($matches) {
            return ' style=' . $matches[1] . minify_css($matches[2]) . $matches[1];
        }, $input);
    }
    return preg_replace(
        array(
            // Remove HTML comments except IE comments
            '#\s*(<\!--(?=\[if).*?-->)\s*|\s*<\!--.*?-->\s*#s',
            // Do not remove white-space after image and
            // input tag that is followed by a tag open
            '#(<(?:img|input)(?:\/?>|\s[^<>]*?\/?>))\s+(?=\<[^\/])#s',
            // Remove two or more white-spaces between tags
            '#(<\!--.*?-->)|(>)\s{2,}|\s{2,}(<)|(>)\s{2,}(<)#s',
            // Proofing ...
            // o: tag open, c: tag close, t: text
            // If `<tag> </tag>` remove white-space
            // If `</tag> <tag>` keep white-space
            // If `<tag> <tag>` remove white-space
            // If `</tag> </tag>` remove white-space
            // If `<tag>    ...</tag>` remove white-spaces
            // If `</tag>    ...<tag>` remove white-spaces
            // If `<tag>    ...<tag>` remove white-spaces
            // If `</tag>    ...</tag>` remove white-spaces
            // If `abc <tag>` keep white-space
            // If `<tag> abc` remove white-space
            // If `abc </tag>` remove white-space
            // If `</tag> abc` keep white-space
            // TODO: If `abc    ...<tag>` keep one white-space
            // If `<tag>    ...abc` remove white-spaces
            // If `abc    ...</tag>` remove white-spaces
            // TODO: If `</tag>    ...abc` keep one white-space
            '#(<\!--.*?-->)|(<(?:img|input)(?:\/?>|\s[^<>]*?\/?>))\s+(?!\<\/)#s', // o+t | o+o
            '#(<\!--.*?-->)|(<[^\/\s<>]+(?:>|\s[^<>]*?>))\s+(?=\<[^\/])#s', // o+o
            '#(<\!--.*?-->)|(<\/[^\/\s<>]+?>)\s+(?=\<\/)#s', // c+c
            '#(<\!--.*?-->)|(<([^\/\s<>]+)(?:>|\s[^<>]*?>))\s+(<\/\3>)#s', // o+c
            '#(<\!--.*?-->)|(<[^\/\s<>]+(?:>|\s[^<>]*?>))\s+(?!\<)#s', // o+t
            '#(<\!--.*?-->)|(?!\>)\s+(<\/[^\/\s<>]+?>)#s', // t+c
            '#(<\!--.*?-->)|(?!\>)\s+(?=\<[^\/])#s', // t+o
            '#(<\!--.*?-->)|(<\/[^\/\s<>]+?>)\s+(?!\<)#s', // c+t
            '#(<\!--.*?-->)|(\/>)\s+(?!\<)#', // o+t
            // Replace `&nbsp;&nbsp;&nbsp;` with `&nbsp; &nbsp;`
            '#(?<=&nbsp;)(&nbsp;){2}#',
            // Proofing ...
            '#(?<=\>)&nbsp;(?!\s|&nbsp;|<\/)#',
            '#(?<=--\>)(?:\s|&nbsp;)+(?=\<)#'
        ),
        array(
            '$1',
            '$1&nbsp;',
            '$1$2$3$4$5',
            '$1$2&nbsp;', // o+t | o+o
            '$1$2', // o+o
            '$1$2', //c+c
            '$1$2$4', // o+c
            '$1$2', // o+t
            '$1$2', // t+c
            '$1$2 ', // t+o
            '$1$2 ', // c+t
            '$1$2 ', // o+t
            ' $1',
            ' ',
            ""
        ),
    trim($input));
}

	// CSS Minifier => http://ideone.com/Q5USEF + improvement(s)
	public function minify_css($input) {
		if(trim($input) === "") return $input;
		return preg_replace(
			array(
				// Remove comments
				'#("(?:[^"\\\]++|\\\.)*+"|\'(?:[^\'\\\\]++|\\\.)*+\')|\/\*(?!\!)(?>.*?\*\/)#s',
				// Remove unused white-spaces
				'#("(?:[^"\\\]++|\\\.)*+"|\'(?:[^\'\\\\]++|\\\.)*+\'|\/\*(?>.*?\*\/))|\s*+;\s*+(})\s*+|\s*+([*$~^|]?+=|[{};,>~+]|\s*+-(?![0-9\.])|!important\b)\s*+|([[(:])\s++|\s++([])])|\s++(:)\s*+(?!(?>[^{}"\']++|"(?:[^"\\\]++|\\\.)*+"|\'(?:[^\'\\\\]++|\\\.)*+\')*+{)|^\s++|\s++\z|(\s)\s+#si',
				// Replace `0(cm|em|ex|in|mm|pc|pt|px|vh|vw|%)` with `0`
				'#(?<=[:\s])(0)(cm|em|ex|in|mm|pc|pt|px|vh|vw|%)#si',
				// Replace `:0 0 0 0` with `:0`
				'#:(0\s+0|0\s+0\s+0\s+0)(?=[;\}]|\!important)#i',
				// Replace `background-position:0` with `background-position:0 0`
				'#(background-position):0(?=[;\}])#si',
				// Replace `0.6` with `.6`, but only when preceded by `:`, `-`, `,` or a white-space
				'#(?<=[:\-,\s])0+\.(\d+)#s',
				// Minify string value
				'#(\/\*(?>.*?\*\/))|(?<!content\:)([\'"])([a-z_][a-z0-9\-_]*?)\2(?=[\s\{\}\];,])#si',
				'#(\/\*(?>.*?\*\/))|(\burl\()([\'"])([^\s]+?)\3(\))#si',
				// Minify HEX color code
				'#(?<=[:\-,\s]\#)([a-f0-6]+)\1([a-f0-6]+)\2([a-f0-6]+)\3#i',
				// Remove empty selectors
				'#(\/\*(?>.*?\*\/))|(^|[\{\}])(?:[^\s\{\}]+)\{\}#s'
			),
			array(
				'$1',
				'$1$2$3$4$5$6$7',
				'$1',
				':0',
				'$1:0 0',
				'.$1',
				'$1$3',
				'$1$2$4$5',
				'$1$2$3',
				'$1$2'
			),
		trim($input));
	}

	// JavaScript Minifier
	public function minify_js($input) {
		if(trim($input) === "") return $input;
		return preg_replace(
			array(
				// '#(?<!\\\)\\\\\"#',
				// '#(?<!\\\)\\\\\'#',
				// Remove comments
				'#\s*("(?:[^"\\\]++|\\\.)*+"|\'(?:[^\'\\\\]++|\\\.)*+\')\s*|\s*\/\*\s*(?!\!|@cc_on)(?>[\s\S]*?\*\/)\s*|\s*(?<![\:\=])\/\/.*[\n\r]*#',
				// Remove unused white-space characters outside the string and regex
				'#("(?:[^"\\\]++|\\\.)*+"|\'(?:[^\'\\\\]++|\\\.)*+\'|\/\*(?>.*?\*\/)|\/(?!\/)[^\n\r]*?\/(?=[\.,;]|[gimuy]))|\s*([+\-\=\/%\(\)\{\}\[\]<>\|&\?\!\:;\.,])\s*#s',
				// Remove the last semicolon
				'#;+\}#',
				// Replace `true` with `!0`
				// '#\btrue\b#',
				// Replace `false` with `!1`
				// '#\bfalse\b#',
				// Minify object attribute except JSON attribute. From `{'foo':'bar'}` to `{foo:'bar'}`
				'#([\{,])([\'])(\d+|[a-z_][a-z0-9_]*)\2(?=\:)#i',
				// --ibid. From `foo['bar']` to `foo.bar`
				'#([a-z0-9_\)\]])\[([\'"])([a-z_][a-z0-9_]*)\2\]#i'
			),
			array(
				// '\\u0022',
				// '\\u0027',
				'$1',
				'$1$2',
				'}',
				// '!0',
				// '!1',
				'$1$3',
				'$1.$3'
			),
		trim($input));
	}

	public function getAmazonContent($search){
		$flagGood=0;
		
		$prime_ad_DE = '<a href="https://www.amazon.de/gp/prime/pipeline/landing?primeCampaignId=prime_assoc_ft&rw_useCurrentProtocol=1&tag=buzzerstar-21" rel="nofollow" target="_blank" title="Beschreibung: Jetzt Amazon Prime 30 Tage kostenlos testen" style="text-decoration: underline; color: #000; font-size: 20px;">Jetzt Amazon Prime 30 Tage kostenlos testen</a>';
		
		$prime_ad_EN = '<a href="https://www.amazon.de/gp/prime/pipeline/landing?primeCampaignId=prime_assoc_ft&rw_useCurrentProtocol=1&tag=buzzerstar-21" rel="nofollow" target="_blank" title="Beschreibung: Jetzt Amazon Prime 30 Tage kostenlos testen" style="text-decoration: underline; color: #000; font-size: 20px;">Jetzt Amazon Prime 30 Tage kostenlos testen</a>';
		
		$max_ad_results = 3;
		$current_count	= 0;
		
		$RelatedMoreContent = "";
		$RelatedMoreContent =<<<END
		<div class="blog__post" style="border: 2px solid #2196F3;">
			$prime_ad_DE
			<div class="post__info row" lang="de">
END;

		//the category could also come from a GET if you wanted. 
		$category = "All"; 

		define('AWS_API_KEY', '###');
		define('AWS_API_SECRET_KEY', '####');
		define('AWS_ASSOCIATE_ID', 'buzzerstar-21');

		//declare the amazon ECS class
		$amazonEcs = new AmazonECS(AWS_API_KEY, AWS_API_SECRET_KEY, 'DE', AWS_ASSOCIATE_ID);

		//tell the amazon class that we want an array, not an object
		$amazonEcs->setReturnType(AmazonECS::RETURN_TYPE_ARRAY);

		//create the amazon object (array)
		$response = $amazonEcs->category($category)->responseGroup('Small,Images,Offers')->search($search);
		
		//check that there are items in the response
		if (isset($response['Items']['Item']) ) {

			//loop through each item
			foreach ($response['Items']['Item'] as $result) {
				
				//check that there is a ASIN code - for some reason, some items are not
				//correctly listed. Im sure there is a reason for it, need to check.
				if (isset($result['ASIN'])) {

					//store the ASIN code in case we need it
					$asin = $result['ASIN'];

					//check that there is a URL. If not - no need to bother showing
					//this one as we only want linkable items
										
					if (isset($result['DetailPageURL']) && $current_count < $max_ad_results ) {						
						$flagGood=1;
						$current_count++;
						$add_text 	= "";
						$detailurl 	= $result['DetailPageURL'];
						$title 		= $result['ItemAttributes']['Title'];
						$image 		= $result['MediumImage']['URL'];
						$hi 		= $result['MediumImage']['Height'][_];
						$wi 		= $result['MediumImage']['Width'][_]; 
						$ma 		= $result['ItemAttributes']['Manufacturer'];
						$pg 		= $result['ItemAttributes']['ProductGroup'];
						$lp 		= $result['OfferSummary']['LowestUsedPrice']['FormattedPrice'];
						$lnp 		= $result['OfferSummary']['LowestNewPrice']['FormattedPrice'];
						$pr 		= $result['Offer']['OfferListing']['IsEligibleForPrime']; 
						$pr_sav 	= $result['Offer']['OfferListing']['PercentageSaved']; 
						
						if (strlen($lp) <= 1){
							$lp = $lnp;
						}
						
						if ($pr == 1){
							$add_text = "- als <b>Prime Kunde</b> profitierst du von $pr_sav Prozent <strong>Ersparnis</strong>!";							
						}
						
						$title_amp = $this->clear_description($title);
						
						$RelatedMoreContent .=<<<END
							<div class="col one">
								<a itemprop="url" href="$detailurl" hreflang="de" rel="nofollow" target="_blank" title="Beschreibung: $title_amp - $ma - $pg" style="text-decoration: underline; ">
									<img xclass="thumbnail__image" src="$image" alt="$title_amp" width="$wi" height="$hi" title="$title_amp - $ma - $pg" xid="catp" style="border-radius: 90px;   -moz-border-radius:90px;-webkit-border-radius: 90px; border-style: solid; border-width: 2px; border-color: #2196F3; height: auto; width: auto; max-width: 400px;" />
								</a>
								<a itemprop="url" href="$detailurl" hreflang="de" rel="nofollow" target="_blank" title="Deutsche Zusammenfassung: $title_amp" style="text-decoration: underline; ">
									<h3 class="heading--secondary">
										<span xstyle="background-color: #e6e6ff; color:#000000;">
											<strong>$title_amp</strong>
										</span>
									</h3>
								</a>
								
								<p class="post__paragraph">
									$title ($pg von $ma für $lp $add_text)
								</p>
							</div>
END;

					/*
						//set up a container for the details - this could be a DIV
						echo "<p style='". IE_BACKGROUND . ";min-height: 60px; font-size: 90%;'>";

						//create the URL link
						echo "<a target='_Blank' href='" . $result['DetailPageURL'] ."'>";

						//if there is a small image - show it
						if (isset($result['MediumImage']['URL'] )) {
							echo "<img class='shadow' style=' margin: 0px; margin-left: 10px; border: 1px solid black; max-height: 55px;' align='right' src='". $result['MediumImage']['URL'] ."'>";
						}
						//$result['MediumImage']['Height']
						//$result['MediumImage']['Width']
						//$result['ItemAttributes']['Manufacturer']
						//$result['ItemAttributes']['ProductGroup']
						//$result['LowestUsedPrice']['FormattedPrice']	

									
						// if there is a title - show it
						if (isset($result['ItemAttributes']['Title'])) {
							echo $result['ItemAttributes']['Title'] . "<br/>";
						}

						//close the paragraph
						echo "</p>";
					*/
					
					}
				}
			}

		} else {

			//display that nothing was found - should no results be found
			//echo "<p  style='". IE_BACKGROUND . "'>No Amazon suggestions found</p>";

		} //

		$RelatedMoreContent .=<<<END
			</div>
			</div>
END;

		if ($flagGood==1){
			return $RelatedMoreContent;
		} else {
			return "";
		}
	} // public function getAmazonContent($search){

} // class
?>