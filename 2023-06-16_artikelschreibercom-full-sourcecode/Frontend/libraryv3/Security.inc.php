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
#require_once '/home/www/wwwartikelschreiber/libraryv3/GeoIP2/vendor/autoload.php';
#use GeoIp2\Database\Reader;

class Security {
	public function isBadEntry($text){
		// https://stackoverflow.com/questions/310572/regex-in-php-to-match-that-arent-html-entities
		if (preg_match("/&[a-z]{1,};/i", $text) != 0){ // example match: ".),&39;((&34;.(,"
			return True; //isBad
		}
		if (preg_match("/&[0-9]{1,};/i", $text) != 0){ // example match: ".),&39;((&34;.(,"
			return True; //isBad
		}	
		return False;
	} // public function ignoreInfrigmentCity(){
								
	public function sanitizeForJsonOption($req){
		// Entferne boesartigen MYSQL Code
		$sql_code = array ( 
			"\"",
			'"',
			',',
			'"',
			'\'',
			';'
		  );
		$replace = array('','','','');  
		$content = str_ireplace($sql_code,$replace,$req);
		return $content;
	} // public function sanitizeRequest($req){
	
	public function sanitizeRequestSimple($req){
		$mk_badflag	= $this->isBadEntry($req);
		if ($mk_badflag === True){
			$req 	= "";
		}
		
		// Entferne boesartigen MYSQL Code
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
		$replace = array('','','','','','','','','','','','');  
		$content = str_ireplace($sql_code,$replace,$req);
		//$content = preg_replace('/[[:^print:]]/', "", $content);
		//$content = preg_replace('/[^\p{L}\s]/u','',$content);
		$content = preg_replace('/[^A-Za-z0-9 öäüÜÄÖß_\-\+\&]/','',$content);
		return $content;
	} // public function sanitizeRequest($req){
		
	public function sanitizeRequest($req){
		
		$mk_badflag	= $this->isBadEntry($req);
		if ($mk_badflag === True){
			$req 	= "";
		}
		
		// Entferne boesartigen MYSQL Code
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
		  
		$content = str_ireplace($sql_code,'',$req);
		return filter_var($content, FILTER_SANITIZE_STRING);
	} // public function sanitizeRequest($req){
			
	public function movePage($num,$url){
	   static $http = array (
		   100 => "HTTP/1.1 100 Continue",
		   101 => "HTTP/1.1 101 Switching Protocols",
		   200 => "HTTP/1.1 200 OK",
		   201 => "HTTP/1.1 201 Created",
		   202 => "HTTP/1.1 202 Accepted",
		   203 => "HTTP/1.1 203 Non-Authoritative Information",
		   204 => "HTTP/1.1 204 No Content",
		   205 => "HTTP/1.1 205 Reset Content",
		   206 => "HTTP/1.1 206 Partial Content",
		   300 => "HTTP/1.1 300 Multiple Choices",
		   301 => "HTTP/1.1 301 Moved Permanently",
		   302 => "HTTP/1.1 302 Found",
		   303 => "HTTP/1.1 303 See Other",
		   304 => "HTTP/1.1 304 Not Modified",
		   305 => "HTTP/1.1 305 Use Proxy",
		   307 => "HTTP/1.1 307 Temporary Redirect",
		   400 => "HTTP/1.1 400 Bad Request",
		   401 => "HTTP/1.1 401 Unauthorized",
		   402 => "HTTP/1.1 402 Payment Required",
		   403 => "HTTP/1.1 403 Forbidden",
		   404 => "HTTP/1.1 404 Not Found",
		   405 => "HTTP/1.1 405 Method Not Allowed",
		   406 => "HTTP/1.1 406 Not Acceptable",
		   407 => "HTTP/1.1 407 Proxy Authentication Required",
		   408 => "HTTP/1.1 408 Request Time-out",
		   409 => "HTTP/1.1 409 Conflict",
		   410 => "HTTP/1.1 410 Gone",
		   411 => "HTTP/1.1 411 Length Required",
		   412 => "HTTP/1.1 412 Precondition Failed",
		   413 => "HTTP/1.1 413 Request Entity Too Large",
		   414 => "HTTP/1.1 414 Request-URI Too Large",
		   415 => "HTTP/1.1 415 Unsupported Media Type",
		   416 => "HTTP/1.1 416 Requested range not satisfiable",
		   417 => "HTTP/1.1 417 Expectation Failed",
		   500 => "HTTP/1.1 500 Internal Server Error",
		   501 => "HTTP/1.1 501 Not Implemented",
		   502 => "HTTP/1.1 502 Bad Gateway",
		   503 => "HTTP/1.1 503 Service Unavailable",
		   504 => "HTTP/1.1 504 Gateway Time-out"
	   );
	   header($http[$num]);
	   header ("Location: $url");
	}
}
?>