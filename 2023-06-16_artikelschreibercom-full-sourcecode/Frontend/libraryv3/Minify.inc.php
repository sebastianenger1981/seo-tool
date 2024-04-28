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
require_once("/home/www/wwwartikelschreiber/libraryv3/HTMLMinifier.php");
// Source: https://www.terresquall.com/web/html-minifier/

class Minify {
	public function doMinify($html){
		HTMLMinifier::$CacheFolder = "/dev/shm/"; // Cached files are stored in 'mycodefolder'.
		return HTMLMinifier::process(
			$html,
			array(
				// 'shift_script_tags_to_bottom' => array( 'combine_javascript_in_script_tags' => true ),
				 'compression_ignore_script_tags' => false,
				 'combine_style_tags' => true,
				// 'shift_script_tags_to_bottom' => true,
				 'show_signature' => false,
				 'combine_javascript_in_script_tags' => true,
				 'compression_mode' => 'all_whitespace',
			)
		); // return HTMLMinifier::process(;
	}
} // class Minify {
?>