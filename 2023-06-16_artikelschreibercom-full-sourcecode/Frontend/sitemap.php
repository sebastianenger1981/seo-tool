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
ini_set('memory_limit','512M');
ini_set('max_execution_time', 3000);
ini_set('display_errors', 0);

require_once("/home/www/wwwartikelschreiber/libraryv3/Logging.inc.php"); 

$seconds_to_cache = 72000;
$ts = gmdate("D, d M Y H:i:s", time() + $seconds_to_cache) . " GMT";

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

$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/marketing/review/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'weekly');  //weekly etc.
$url->addChild('priority', "0.55");

$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/marketing/paraphrase/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'weekly');  //weekly etc.
$url->addChild('priority', "0.55");

$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/marketing/generator/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'weekly');  //weekly etc.
$url->addChild('priority', "0.55");

$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/marketing/tagline/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'weekly');  //weekly etc.
$url->addChild('priority', "0.85");

$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/marketing/slogan/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'weekly');  //weekly etc.
$url->addChild('priority', "0.85");

$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/marketing/article/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'weekly');  //weekly etc.
$url->addChild('priority', "0.95");

$url = $urlset->addChild('url');
$url->addChild('loc',"https://www.artikelschreiber.com/marketing/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'weekly');  //weekly etc.
$url->addChild('priority', "0.90");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/status/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.72");

//add the page URL to the XML urlset
$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.90");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/tr/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/fr/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/en/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/es/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/it/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/ru/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/jp/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/pt/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/in/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/sa/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/cn/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.99");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/texts/" );
$url->addChild('lastmod', date("Y-m-d") );
$url->addChild('changefreq', 'daily');  //weekly etc.
$url->addChild('priority', "0.75");


/*
$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/api/" );
$url->addChild('lastmod', "2018-10-21" );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.82");

$url = $urlset->addChild('url');
$url->addChild('loc', "https://www.artikelschreiber.com/leichte-sprache/" );
$url->addChild('lastmod', "2018-10-21" );
$url->addChild('changefreq', 'monthly');  //weekly etc.
$url->addChild('priority', "0.89");

$image = $url->addChild('image:image', null, 'http://www.google.com/schemas/sitemap-image/1.1');
$image->addChild('image:loc',"https://www.artikelschreiber.com/images/logo.png", 'http://www.google.com/schemas/sitemap-image/1.1');
$image->addChild('image:caption',"Schreiben Sie automatisch Artikel mit dem Text Generator", 'http://www.google.com/schemas/sitemap-image/1.1');
$image->addChild('image:title',"Schreibe automatisch Text & Content | ArtikelSchreiber.com", 'http://www.google.com/schemas/sitemap-image/1.1');
*/
//add whitespaces to xml output (optional, of course)
$dom = new DomDocument();
$dom->loadXML($urlset->asXML());
$dom->formatOutput = true;
//output xml
echo $dom->saveXML();
$Logs = new Logging();
$Logs->logQuerys("Sitemap");
exit(0);
?>