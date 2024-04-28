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
//error_reporting(E_ALL);
//ini_set('display_errors', 1);
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
$langArray			= $Lang->getLanguageArray();
$base_dir 			= __DIR__;
$list 				= explode("/",$_SERVER["SCRIPT_FILENAME"]);
$language 			= $list[4];
$path 				= pathinfo($_SERVER["SCRIPT_FILENAME"]);
$files 				= scandir($path["dirname"]);
$url 				= "https://www.artikelschreiber.com".$_SERVER["REQUEST_URI"];

//$lan 				= array("de","en","fr","es","it","ru","pt","ar","it","jp","zh","tr");
$htmlContent1 		= $Func->createLanguageFlagsHmtl();
$htmlContent 		= "<fieldset class=\"content\">$htmlContent1</fieldset>";

$title_meta 		= $langArray[$language]['summary'];
$description_meta	= $langArray[$language]['email_body'] . ' ' . $langArray[$language]['url'];
$description_h1		= $langArray[$language]['description'];
$werbung 			= $langArray[$language]['werbung'];

$blogurl			= "https://www.artikelschreiber.com/$language/blog/";

$title_linking 		= $langArray[$language]['index_title'];
$description_linking= $langArray[$language]['index_description'];
$url_linking		= $langArray[$language]['url'];


shuffle($files);
echo <<<END
<!DOCTYPE html>
<html lang="$language">
	<head>
		<title>$title_meta | Blog</title>
		<meta charset="UTF-8" />
		<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
		<meta name="viewport" content="width=device-width, height=device-height, user-scalable=1, initial-scale=1" />
		<meta name="keywords" content="Blog, blogging, artikel, article, text, generator, text generator, text generation, text creator, text writer, article writer, artikel schreiben" />
		<meta name="description" content="$description_meta" />
		<link rel="canonical" href="https://www.artikelschreiber.com/$language/blog/" />
		<meta name="mobile-web-app-capable" content="yes" />

		<meta property="og:title" content="Blog $language | $title_meta" />
		<meta property="og:description" content="$description_meta" />
		<meta property="og:url" content="https://www.artikelschreiber.com/$language/blog/" />
		<meta property="og:image" content="https://www.artikelschreiber.com/images/logo.png" />
		<meta property="og:sitename" content="ArtikelSchreiber.com" />
		<meta property="og:locale" content="$language_$language" />
		<meta property="og:type" content="Website" />
		<meta property="og:locale:alternate" content="fr_FR" /> 
		<meta property="og:locale:alternate" content="es_ES" />
		<meta property="og:locale:alternate" content="en_US" />
		<meta property="og:locale:alternate" content="it_IT" />
		<meta property="og:locale:alternate" content="de_DE" />
		<meta property="og:locale:alternate" content="sa_SA" />
		<meta property="og:locale:alternate" content="jp_JP" />
		<meta property="og:locale:alternate" content="cn_CN" />
		<meta property="og:locale:alternate" content="pt_PT" />
		<meta property="og:locale:alternate" content="in_IN" />
		<meta property="og:locale:alternate" content="ru_RU" />
		<meta property="og:locale:alternate" content="tr_TR" />
		<meta property="og:image:type" content="image/png" />
		<meta property="og:image:width" content="531" />
		<meta property="og:image:height" content="628" />
		<meta property="og:image:alt" content="Blog $language | $title_meta" />

		<meta name="twitter:card" content="summary_large_image" />
		<meta name="twitter:site" content="https://www.artikelschreiber.com/" />
		<meta name="twitter:title" content="Blog $language | $title_meta" />
		<meta name="twitter:description" content="Blog $description_meta" />
		<meta name="twitter:creator" content="https://www.artikelschreiber.com/" />
		<meta name="twitter:image:src" content="https://www.artikelschreiber.com/images/logo.png" />
		<meta name="twitter:domain" content="www.artikelschreiber.com" />
		<meta name="twitter:url" content="https://www.artikelschreiber.com/$language/blog/" />
		<meta name="twitter:image" content="https://www.artikelschreiber.com/images/logo.png" />
		
		<link rel="icon" type="image/png" sizes="120x120" href="https://www.artikelschreiber.com/images/apple-icon-120x120.png" />
		<link rel="apple-touch-icon" type="image/png" href="https://www.artikelschreiber.com/images/logo.png" />
		<link rel="alternate" hreflang="de" href="https://www.artikelschreiber.com/de/blog/" />
		<link rel="alternate" hreflang="en" href="https://www.artikelschreiber.com/en/blog/" />
		<link rel="alternate" hreflang="fr" href="https://www.artikelschreiber.com/fr/blog/" />
		<link rel="alternate" hreflang="es" href="https://www.artikelschreiber.com/es/blog/" />
		<link rel="alternate" hreflang="it" href="https://www.artikelschreiber.com/it/blog/" />
		<link rel="alternate" hreflang="ru" href="https://www.artikelschreiber.com/ru/blog/" />
		<link rel="alternate" hreflang="zn" href="https://www.artikelschreiber.com/cn/blog/" />
		<link rel="alternate" hreflang="ja" href="https://www.artikelschreiber.com/jp/blog/" />
		<link rel="alternate" hreflang="pt" href="https://www.artikelschreiber.com/pt/blog/" />
		<link rel="alternate" hreflang="in" href="https://www.artikelschreiber.com/in/blog/" />
		<link rel="alternate" hreflang="ar" href="https://www.artikelschreiber.com/sa/blog/" />
		<link rel="alternate" hreflang="tr" href="https://www.artikelschreiber.com/tr/blog/" />
		<link rel="alternate" href="https://www.artikelschreiber.com/$language/blog/" hreflang="x-default" />
		<link rel="alternate" href="https://www.artikelschreiber.com/$language/blog/feed.php" title="RSS feed" type="application/rss+xml" />

		<style>
			body,textarea,input,select{background:0;border-radius:0;font:16px sans-serif;margin:0}.addon,.btn-sm,.nav,textarea,input,select{outline:0;font-size:14px}.smooth{transition:all .2s}.btn,.nav a{text-decoration:none}.container{margin:0 20px;width:auto}@media(min-width:1310px){.container{margin:auto;width:1270px}}.btn,h2{font-size:2em}h1{font-size:3em}.btn{background:#999;border-radius:6px;border:0;color:#fff;cursor:pointer;display:inline-block;margin:2px 0;padding:12px 30px 14px}.btn:hover{background:#888}.btn:active,.btn:focus{background:#777}.btn-a{background:#0ae}.btn-a:hover{background:#09d}.btn-a:active,.btn-a:focus{background:#08b}.btn-b{background:#3c5}.btn-b:hover{background:#2b4}.btn-b:active,.btn-b:focus{background:#2a4}.btn-c{background:#d33}.btn-c:hover{background:#c22}.btn-c:active,.btn-c:focus{background:#b22}.btn-sm{border-radius:4px;padding:10px 14px 11px}label>*{display:inline}form>*{display:block;margin-bottom:10px}textarea,input,select{border:1px solid #ccc;padding:8px}textarea:focus,input:focus,select:focus{border-color:#5ab}textarea,input[type=text]{-webkit-appearance:none;width:13em;outline:0}.addon{box-shadow:0 0 0 1px #ccc;padding:8px 12px}.nav,.nav .current,.nav a:hover{background:#000;color:#fff}.nav{height:24px;padding:11px 0 15px}.nav a{color:#aaa;padding-right:1em;position:relative;top:-1px}.nav .pagename{font-size:22px;top:1px}.btn.btn-close{background:#000;float:right;font-size:25px;margin:-54px 7px;display:none}@media(max-width:500px){.btn.btn-close{display:block}.nav{overflow:hidden}.pagename{margin-top:-11px}.nav:active,.nav:focus{height:auto}.nav div:before{background:#000;border-bottom:10px double;border-top:3px solid;content:'';float:right;height:4px;position:relative;right:3px;top:14px;width:20px}.nav a{display:block;padding:.5em 0;width:50%}}.table th,.table td{padding:.5em;text-align:left}.table tbody>:nth-child(2n-1){background:#ddd}.ico{font:33px Arial Unicode MS,Lucida Sans Unicode}.row{margin:1% 0;overflow:auto}.col{float:left}.table,.c12{width:100%}.c11{width:91.66%}.c10{width:83.33%}.c9{width:75%}.c8{width:66.66%}.c7{width:58.33%}.c6{width:50%}.c5{width:41.66%}.c4{width:33.33%}.c3{width:25%}.c2{width:16.66%}.c1{width:8.33%}@media(max-width:870px){.row .col{width:100%}}.msg{background:#def;border-left:5px solid #59d;padding:1.5em}
			.hero{background:#eee;padding:10px;border-radius:10px;margin-top:2px}h1{margin-top:0;margin-bottom:.3em;font-size:18px}h2{margin-top:0;margin-bottom:.3em;font-size:15px}h3{margin-top:0;margin-bottom:.3em;font-size:18px}h4{margin-top:0;margin-bottom:.3em;font-size:18px}h5{margin-top:0;margin-bottom:.3em;font-size:18px}.c4{padding:10px;box-sizing:border-box}.c4 h3{margin-top:0}.c4 a{margin-top:10px;display:inline-block}.divScroll{overflow-y:scroll;height:250px;width:650px}.nm-button{text-transform:uppercase;padding:5px;color:#000;font-weight:900}.video-container{position:relative;padding-bottom:3.25%;padding-top:30px;height:0;overflow:hidden}.video-container object,.video-container object,
								
			footer a{text-decoration:none;color:rgba(0,0,0,0.8)}
			
			.tooltip{position:relative;display:inline-block}.tooltip .tooltiptext{visibility:hidden;width:140px;background-color:#555;color:#fff;text-align:center;border-radius:6px;padding:5px;position:absolute;z-index:1;bottom:150%;left:50%;margin-left:-75px;opacity:0;transition:opacity 0.3s}.tooltip .tooltiptext::after{content:"";position:absolute;top:100%;left:50%;margin-left:-5px;border-width:5px;border-style:solid;border-color:#555 transparent transparent transparent}.tooltip:hover .tooltiptext{visibility:visible;opacity:1}

			textarea {-webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box; width: 100%; max-width:95%;}
			ledgend {max-width:95%;}

			.linkme {width: 100%; max-width:95%; height: 47px;}

			iamsmaller {font-size: 12px;}

			.input-res {width: 100%; max-width: 500px; box-sizing: border-box; }

			html { font-size: calc(1em + 1vw) }
			
			.responsive {	max-width: 100%; height: auto; }
			
			.center{display:block;margin-left:auto;margin-right:auto;width:50%,max-width: 100%; height: auto;}
			.footer {font-size:14px; position: sticky; bottom:0px;}
			.footer_ul {overflow-x:hidden;white-space:nowrap; width: 100%;}
			.footer_ul_li {display:inline; margin: 5px;}
			
			.active { background-color:#3c5;}
		</style>				
	</head>

	<body itemscope itemtype="https://schema.org/WebPage" class="hmedia" style="text-align: left; overflow-wrap: break-word; word-wrap: normal; word-break: break-word;" translate="yes" lang="$language">
		<p>
			<h1 class="content" role="heading" aria-level="1">
				<a href="https://www.artikelschreiber.com/$language/blog/">Blog $language | $title_meta</a>
			</h1>
		</p>
		<p><h2 class="content" role="heading" aria-level="2">$description_h1</h2></p>
		<p>
			<h3 class="content" role="list" role="heading" aria-level="3">Partner: 
				<li role="listitem"><a href="https://www.unaique.net/" target="_self" hreflang="de" title="Marketing: Copywriter">KI Text Generator</a></li> 
				<li role="listitem"><a href="https://rechthaben.net/" target="_self" hreflang="de" title="Recht Haben">Recht Haben</a></li> 
				<li role="listitem"><a href="$url_linking" hreflang="$language" title="$description_linking">$title_linking</a></li> 
			</h3>
		</p>
END;

for ($i=0; $i<21; $i++){
	$contains_sum 				= array();
	$myfinfile 					= $base_dir."/".$files[$i];
	if (strlen($files[$i]) > 10 and stripos($files[$i], '.html') !== false){
		if($dom->loadHTMLFile($myfinfile)) { // https://stackoverflow.com/questions/399332/fastest-way-to-retrieve-a-title-in-php
			$list 				= $dom->getElementsByTagName("span"); #title
			//$list_title		= $dom->getElementsByTagName("title"); #title		
			$contains_sum 		= array();
			for ($x=0; $x<$list->length - 1; $x++){
				$text 			= $list->item($x)->textContent;
				$isBadEntry 	= $Func->isBadBlogContent($text);
				#echo "isbad: $isBadEntry -> $title : myfinurl=$myfinurl: <br>";
				array_push($contains_sum, $isBadEntry);
			} // for ($x=0; $x<$list->length - 1; $x++){
		}; // if($dom->loadHTMLFile($myfinfile)) {
	}; // if (strlen($files[$i]) > 10){
	#echo "sum(a) = " . array_sum($contains_sum) . "<br>";
	if (array_sum($contains_sum) < 2){ // weniger als 2 Stopwort Listen Einträge bei ca. 16 <span></span> Content einträgen bei tplv3/index_show_en.tpl
		if($dom->loadHTMLFile($myfinfile)) { 
			$list_title			= $dom->getElementsByTagName("title"); #title
			$title 				= $list_title->item(0)->textContent;
			$myfinurl 			= $url.$files[$i];
			//echo "$myfinurl - $title<br />";
			if (strlen($title) > 7 and $Func->endsWith($myfinurl,".html")){
				//$title 	= $myfinurl;
				$title 		= $Secu->sanitizeForJsonOption($title);
				$title 		= preg_replace('/[\x00-\x1F\x80-\xFF]/', '', $title);
				//if ( strlen($title) == strlen($title1)){
					// title = 'Karten & Einladungen fÃ¼r besondere AnlÃ¤sse fÃ¼r den Geburt'	-> UTF8 Fehler
					// title1 = 'Karten & Einladungen fr besondere Anlsse fr den Geburt'
				echo "<fieldset lang=\"$language\" class=\"content\"><a href=\"$myfinurl\" rel=\"ugc\" target=\"_self\" hreflang=\"$language\" title=\"$title -> $myfinurl\">$title</a><br /></fieldset>";
				//}; // if ( strlen($title) == strlen($title1)){
			}; // if (strlen($title) < 3 and endsWith($myfinurl,".html")){
		}; // if($dom->loadHTMLFile($myfinfile)) { 
	}; // if (array_sum($contains_sum) < 2){
	$contains_sum 				= array();
}; // for ($i=0; $i<25; $i++){
	
/*
for ($i=0; $i<21; $i++){
	if (strlen($files[$i]) > 10){
		$myfinurl = $url.$files[$i];
		echo "<fieldset lang=\"$language\" class=\"content\"><a href=\"$myfinurl\" target=\"_self\" hreflang=\"$language\">$myfinurl</a><br /></fieldset>";
	}; // if (strlen($files[$i]) > 10){
} // foreach ($random_keys as $key => $value) {
*/

echo <<<END
	$htmlContent
	<br />	
	<fieldset lang="$language">
			<p>
				<b><u id="SocialShareButtons">Share:</u></b> &nbsp;&nbsp;&nbsp;
				
				<p>
					<ul role="list">
						<li role="listitem" id="shareFacebook"></li>
						<li role="listitem" id="shareTwitter"></li>
						<li role="listitem" id="shareWhatsApp"></li>
						<li role="listitem" id="shareTelegram"></li>
						<li role="listitem" id="shareLinkedIn"></li>
						<li role="listitem" id="shareEmail"></li>
						<li role="listitem" id="sharevKontakte"></li>
						<li role="listitem" id="shareTumblr"></li>
						<li role="listitem" id="shareXing"></li>
						<li role="listitem" id="shareLineit"></li>
						<li role="listitem" id="shareSkype"></li>
						<li role="listitem" id="shareSnapChat"></li>
						<li role="listitem" id="shareReddit"></li>
						<li role="listitem" id="shareFlipboard"></li>
					</ul>
				</p>
			</p>
	</fieldset>
	
	<br />
	<fieldset lang="en">
		<legend><b>Please link to us from high quality websites:</b></legend>
					
		<textarea class="linkme" id="myInput" name="myInput"><a href="$url_linking" hreflang="$language" title="$description_linking">$title_linking</a></textarea>

		<div class="tooltip">
		<button onclick="myFunction();" onmouseout="outFunc()" title="Click here to copy the text to the clipboard!">
		  <span class="tooltiptext" id="myTooltip">Copied to clipboard!</span>
		 Copy Text
		  </button>
		</div>		
	</fieldset>
				
	<br />
	<section>
		<footer class="footer">
				<p>
					&copy; 2016 - 2023 - <strong>ArtikelSchreiber.com: ✅ Marketing: Write an article, free text or marketing content with SEO tool for ✅ eCommerce, Business, Sales and Upsell with ✅ Text generator based on ✅ Artificial Intelligence / AI and ✅ Natural Language Processing/NLP</strong>
				</p>
				<p>
					<cite>"ArtikelSchreiber.com will forever be free of costs!"</i>, CEO & Founder</cite>
				</p>
				<ul id="footer_ul" role="list">
					<li role="listitem" class="footer_ul_li"><a href="https://www.unaique.net/" target="_self" hreflang="de" title="Text Generator deutsch & KI Text Generator">Text Generator deutsch</a></li>
					<li role="listitem" class="footer_ul_li">-</li>
					<li role="listitem" class="footer_ul_li"><a href="https://www.unaique.net/en/" target="_self" hreflang="en" title="CopyWriting: AI Text Generator for Marketing Content by AI | UNAIQUE.NET">AI Text Generator</a></li>
					<li role="listitem" class="footer_ul_li">-</li>
					<li role="listitem" class="footer_ul_li"><a href="https://www.unaique.com/" target="_self" hreflang="en" title="unaique.com">unaique.com</a></li>
					<li role="listitem" class="footer_ul_li"><br /><br /></li>
					<li role="listitem" class="footer_ul_li"><a href="https://rechthaben.net/" target="_self" hreflang="de" title="Grundrechte & BGB | RechtHaben.net : Dem deutschen Volke! Wacht auf! Wehrt euch!">Recht Haben</a></li>
					<li role="listitem" class="footer_ul_li">-</li>
					<li role="listitem" class="footer_ul_li"><a href="https://www.unaique.net/blog/" target="_self" hreflang="de" title="KI Blog">KI Blog</a></li>
					<li role="listitem" class="footer_ul_li">-</li>
					<li role="listitem" class="footer_ul_li"><a href="https://www.artikelschreiber.com/marketing/" target="_self" hreflang="en">Marketing Tools</a></li>
					<li role="listitem" class="footer_ul_li"><br /><br /></li>
					<li role="listitem" class="footer_ul_li"><a href="https://www.unaique.com/impressum.html" target="_self" hreflang="de" rel="noopener noreferrer nofollow">Impressum</a></li>
					<li role="listitem" class="footer_ul_li">-</li>
					<li role="listitem" class="footer_ul_li"><a href="https://www.unaique.com/privacy-policy.html" target="_self" hreflang="de" rel="noopener noreferrer nofollow">Datenschutz</a></li>
				</ul>			
		</footer>
	</section>
		
	<script type="application/ld+json">
		{
		  "@context": "http://schema.org",
		  "@type": "BreadcrumbList",
		  "itemListElement": [{
			"@type": "ListItem",
			"position": 1,
			"item": {
			  "@id": "https://www.artikelschreiber.com/$language/blog/",
			  "name": "Blog $language | ArtikelSchreiber.com"
			}
		  },{
			"@type": "ListItem",
			"position": 2,
			"item": {
			  "@id": "https://www.artikelschreiber.com/$language/",
			  "name": "$title_meta"
			}
		  },{
			"@type": "ListItem",
			"position": 3,
			"item": {
			  "@id": "https://www.artikelschreiber.com/",
			  "name": "Schreibe einen Artikel mit KI"
			}
		  }]
		}
	</script>

	<script type="text/javascript" async>
		function addLink(){
			var selection 	= window.getSelection();
			navigator.clipboard.writeText(selection+"<br /><br />"+"<a href='https://www.unaique.net/' title='Text Generator deutsch - KI Text Generator | UNAIQUE.NET' target='_self' hreflang='de'>KI Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.unaique.net/en/' title='CopyWriting: Generator for Marketing Content by AI | UNAIQUE.NET' target='_self' hreflang='en'>AI Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.artikelschreiber.com/' title='Artikel schreiben für Content Marketing | ArtikelSchreiber.com' hreflang='de' target='_self'>Artikel Schreiber</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.artikelschreiber.com/en/' title='AI Content Generator: Write text for Marketing | ArtikelSchreiber.com' hreflang='en' target='_self'>Text Generator</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://rechthaben.net/' title='rechthaben.net' hreflang='de' target='_self'>rechthaben.net</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='https://www.unaique.com/' title='www.unaique.com' hreflang='en' target='_self'>www.unaique.com</a> &nbsp;&nbsp;-&nbsp;&nbsp; <a href='$blogurl' title='$blogurl - Blog $language' hreflang='$language' target='_self'>$blogurl</a>");
		}
		document.oncopy = addLink;
	</script>
	
	<script async>
function myFunction() {
  var copyText = document.getElementById("myInput");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  
  var tooltip = document.getElementById("myTooltip");
  tooltip.innerHTML = "Copied successfully!";// + copyText.value;
}

function outFunc() {
  var tooltip = document.getElementById("myTooltip");
  tooltip.innerHTML = "Copied to clipboard!";
}
</script>
			
<script type="text/javascript" async>
document.getElementById("shareFacebook").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=$url_linking">Facebook</a>';
document.getElementById("shareTwitter").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://twitter.com/share?url=$url_linking">Twitter</a>';
document.getElementById("shareWhatsApp").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="whatsapp://send?text=$url_linking">WhatsApp</a>';
document.getElementById("shareLinkedIn").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="http://www.linkedin.com/shareArticle?mini=true&url=$url_linking">LinkedIn</a>';
document.getElementById("shareEmail").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="mailto:?subject=Check out the free ArtikelSchreiber.com&body=$url_linking">eMail</a>';
document.getElementById("sharevKontakte").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="http://vkontakte.ru/share.php?url=$url_linking">vKontakte</a>';
document.getElementById("shareTumblr").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="http://www.tumblr.com/share/link?url=$url_linking">Tumblr</a>';
document.getElementById("shareLineit").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://lineit.line.me/share/ui?url=$url_linking">LineIT</a>';
document.getElementById("shareSkype").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://web.skype.com/share?url=$url_linking">Skype</a>';
document.getElementById("shareTelegram").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://telegram.me/share/url?url=$url_linking">Telegram</a>';
document.getElementById("shareSnapChat").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://snapchat.com/scan?attachmentUrl=$url_linking">SnapChat</a>';
document.getElementById("shareReddit").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="http://reddit.com/submit?url=$url_linking">Reddit</a>';
document.getElementById("shareFlipboard").innerHTML = '<a  rel="noopener noreferrer nofollow" target="_blank" href="https://share.flipboard.com/bookmarklet/popout?url=$url_linking">Flipboard</a>';
document.getElementById("shareXing").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://www.xing.com/spi/shares/new?url=$url_linking">XING</a>';
</script>

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8441004200831936" crossorigin="anonymous"></script>

</body>
</html>
END;
exit(0);
?>