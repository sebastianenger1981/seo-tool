<?php
/*
HTML Minifier
=============
This is a static PHP class that minifies HTML. To use it, call HTMLMinifier::process() and pass your
HTML into it. You can also initialise it so that you can use the function non-statically. Either way
is fine.

@author		Terence Pek <terence@terresquall.com>
@website	www.terresquall.com
@version	3.1.0
@dated		27/06/2018
@notes		- Fixed a bug with the 'ignore_async_and_defer_tags' option. They behaved opposite of what they should have.
			- Fixed a bug causing <style scoped> tags to not have their comments cleaned.
			- Fixed a bug with <style> types nested in IE conditional tags causing a fatal error.
			- <script> tags that have an 'id' attribute are no longer merged with other scripts.
			- Non-Javascript <script> tags are no longer moved, and Javascript comments in them are no longer removed.
			- Added support for 'compression_ignored_tags' and deprecated 'compression_ignore_script_tags'.
			- Double slashes (//) in Javascript regex blocks no longer get identified as comments.
			- Added support for minifying JS / CSS files.
			- Modified ::compress() so that it can now exclude tags from compression. Excluded <textarea> tags from being compressed.
			- Make get_tags() handle nested tags.
			Fixed a bug where any Javascript blocks with CDATA will not have their comments cleaned.
			Resolved a few bugs with whitespace being left behind if you choose to not compress script tags.
			Fixed a bug that caused chunks of non-conditional commented content to be removed.
			- Made $CacheFolder more lenient with directory separators.
*/
class HTMLMinifier {
	
	public static $CacheFolder = ''; // Set this at the end of the file. If empty, there will be no caching.
	public static $CacheExpiry = 86400; // Time in seconds. 86400 is 1 day.
	
	const VERSION = '3.1.0';
	const SIGNATURE = 'Original size: %d bytes, minified: %d bytes. HTMLMinifier: www.terresquall.com/web/html-minifier.';
	const CACHE_SIG = 'Server cached on %s.';
	
	static $Signature; // Signature processed by sprintf() is placed here.
	
	// For documentation.
	static $CompressionMode = array(
		'none' => 'None',
		//'pretty_indent' => 'Pretty indent',
		'all_whitespace_not_newlines' => 'All whitespace except newlines',
		'all_whitespace' => 'All whitespaces'
	);
	
	static $Defaults = array(
		// General options.
		'clean_html_comments' => true,
		'merge_multiple_head_tags' => true,
		'merge_multiple_body_tags' => true,
		'show_signature' => true, // Show signature at the end.
		
		// Stylesheet optimisations.
		'clean_css_comments' => array('remove_comments_with_cdata_tags_css' => false),
		'shift_link_tags_to_head' => array('ignore_link_schema_tags' => true),
		'shift_meta_tags_to_head' => array('ignore_meta_schema_tags' => true),
		'shift_style_tags_to_head' => array('combine_style_tags' => false),
		
		// Javascript optimisations.
		'clean_js_comments' => array('remove_comments_with_cdata_tags_js' => false),
		//'compression_ignore_script_tags' => true, //LEGACY ATTRIBUTE
		'shift_script_tags_to_bottom' => false, // 'combine_javascript_in_script_tags', 'ignore_async_and_defer_tags'
		'add_async_defer_tag' => false,
		
		// How do you want to compress the script?
		'compression_mode' => 'all_whitespace_not_newlines',
		'compression_ignored_tags' => array('textarea','pre','script') // NEW THING, NOT IMPLEMENTED.
	);
	
	private static $Presets = array(
		'super_safe' => array(
			'merge_multiple_head_tags' => false,
			'merge_multiple_body_tags' => false,
			'shift_link_tags_to_head' => false,
			'shift_meta_tags_to_head' => false,
			'shift_style_tags_to_head' => false,
		),
		'safe' => array(),
		'moderate' => array(
			'shift_style_tags_to_head' => array('combine_style_tags' => false),
			'shift_script_tags_to_bottom' => array('combine_javascript_in_script_tags' => false, 'ignore_async_and_defer_tags' => true),
		),
		'fully_optimised' => array(
			'shift_style_tags_to_head' => array('combine_style_tags' => true),
			'shift_script_tags_to_bottom' => array('combine_javascript_in_script_tags' => true, 'ignore_async_and_defer_tags' => true),
			//'compression_ignore_script_tags' => false, //LEGACY ATTRIBUTE
			'compression_mode' => 'all_whitespace'
		)
	);
	
	private static $SelfClosingTags = array('area','base','br','col','embed','hr','img','input','keygen','link','menuitem','meta','param','source','track','wbr','!--');
	
	public function __construct() { throw new Exception("Please don't try to initialise the HTMLMinifier class! Use it as a static class."); }
	
	// Get preset settings for process().
	public static function get_presets($type) {
		if(!array_key_exists($type,self::$Presets)) return null;
		return array_merge(self::$Defaults,self::$Presets[$type]);
	}
		
	// This is THE function that you call when you use this.
	// Refer to self::$Defaults for what to fill $options with.
	public static function process($html,$options = null,$cache_key = '') {
		
		// If cache key is provided, try to retrieve from cache first.
		if($cache_key) {
			$out = HTMLMinifier::cache($cache_key);
			if($out !== false) return $out;
		}
		
		// Let's start processing our stuff here.
		$startLen = strlen($html); // Save original size.
		$out = $html;
		
		// Figure out what our compression options are.
		if($options !== null && is_array($options)) $options = array_merge(self::$Defaults,$options);
		else $options = self::$Defaults;
		
		// Force 'clean_js_comments' and 'clean_css_comments' if the compression mode is all whitespace.
		if($options['compression_mode'] === 'all_whitespace') {
			$options['clean_js_comments'] = true;
			$options['clean_css_comments'] = true;
		}
		
		// Remove all HTML comments if they are not conditional comments.
		$comments = array();
		$conditionals = array();
		$out = self::remove_html_comments($out,$comments,$conditionals,$options['clean_html_comments']);
		
		// Get all content that is wrapped between two conditionals that matter.
		preg_match_all('@(<!-- \\[htmlminifier\\[[0-9]*?cs\\]\\] -->)([\\s\\S]*?)(<!-- \\[htmlminifier\\[[0-9]*?ce\\]\\] -->)@',$out,$wrapped_conditionals);
		foreach($wrapped_conditionals[2] as $k => $c) {
			if(!preg_match('@<link|style|meta|script@i',$c))
				unset($wrapped_conditionals[0][$k],$wrapped_conditionals[1][$k],$wrapped_conditionals[2][$k],$wrapped_conditionals[3][$k]);
		}
		
		// Make sure that there is a head tag in the document.
		$head_tags = self::get_tags('head',$out);
		$head_count = count($head_tags[0]);
		
		// Empty the contents of the head tag(s).
		$head = null;
		if($head_count > 1) {
			if($options['merge_multiple_head_tags']) {
				$head = '';
				foreach($head_tags[2] as $h) {
					$out = self::replace($h,'',$out);
					$head .= $h;
				}
			} else {
				$head = array();
				foreach($head_tags[2] as $h) {
					$out = self::replace($h,'',$out);
					array_push($head,$h);
				}
			}
		} elseif($head_count === 1) {
			$head = $head_tags[2][0];
			$out = self::replace($head,'',$out);
		}
		
		// Process stylesheet stuff here as contents outside stylesheet will be moved to bottom of head.
		$out = self::process_css_options($out,$options,$head,$comments,$conditionals,$wrapped_conditionals);
		
		// Put <head> back and begin to process <script> tags.
		if($head) {
			$empty_heads = self::get_tags('head',$out);
			if(count($empty_heads[0]) > 0) {
				if(is_array($head)) {
					foreach($empty_heads[0] as $i => $m) {
						if(empty($head[$i])) $out = self::replace($m,'',$out); // Remove this tag if there are no contents for it.
						else $out = self::replace($m,$empty_heads[1][$i] . PHP_EOL . $head[$i] . PHP_EOL . $empty_heads[3][$i],$out);
					}
				} else {
					$out = self::replace($empty_heads[0][0],$empty_heads[1][0] . PHP_EOL . $head . PHP_EOL . $empty_heads[3][0],$out);
					unset($empty_heads[0][0],$empty_heads[1][0],$empty_heads[2][0],$empty_heads[3][0]); // Remove these matches as they have been used.
					foreach($empty_heads[0] as $m) $out = self::replace($m,'',$out);
				}
			} else trigger_error('Trying to put back &lt;head&gt; tag contents, but we cannot find any empty &lt;head&gt; tag anymore!',E_USER_ERROR);
		}
		
		$out = self::process_script_options($out,$options,$comments,$conditionals,$wrapped_conditionals);
		
		// We are still checking for 'compression_ignore_script_tags' for backward compatibility.
		if( !empty($options['compression_ignore_script_tags']) && !in_array('script',$options['compression_ignored_tags']) )
			$options['compression_ignored_tags'][] = 'script';
		$out = self::compress($out,$options['compression_mode'],$options['compression_ignored_tags']);
				
		// Replace all the comments that are saved.
		if(preg_match_all('@<!-- \\[htmlminifier\\[([0-9a-z]*)\\]\\] -->@i',$out,$tagged_comments)) {
			foreach($tagged_comments[0] as $k => $tc) {
				if(array_key_exists($tagged_comments[1][$k],$comments)) {
					$new_comment = $comments[$tagged_comments[1][$k]];
					if(substr($tagged_comments[1][$k],-1) === 'c') $new_comment = self::compress($new_comment,$options['compression_mode'],$options['compression_ignored_tags']);
					$out = self::replace($tc,'<!--'.$new_comment.'-->',$out);
				} else
					$out = self::replace($tc,'',$out);
			}
		}
		
		// Append signature at the end of the document
		if($options['show_signature']) {
			self::$Signature = sprintf(self::SIGNATURE, $startLen, strlen($out));
			$pos = strrpos($out,'</html>');
			
			// Terminate if the </html> tag is missing.
			if($pos === false) {
				//trigger_error('HTMLMinifier::process(): Missing &lt;/html&gt; tag.',E_USER_ERROR);
				return $out;
			}
			
			$out = substr_replace($out,'<!-- ' . self::$Signature . ' --></html>',$pos,7);
		}
		
		// Cache if there is a key.
		if($cache_key) HTMLMinifier::cache($cache_key,$out);
		
		return $out;
	}
	
	// Used to compress JS or CSS files.
	// $source - file data in string format.
	// $filetype - "js" or "css".
	// $options - the same stuff that you use for HTMLMinifier::process.
	public static function minify_rsc($source,$filetype,$options = null,$cache_key = '') {
		
		// If cache key is provided, try to retrieve from cache first.
		if($cache_key) {
			$out = HTMLMinifier::cache($cache_key);
			if($out !== false) return $out;
		}
		
		// Figure out what our compression options are.
		if($options !== null && is_array($options)) $options = array_merge(self::$Defaults,$options);
		else $options = self::$Defaults;
		
		$orig_size = strlen($source); // Saves the original size of the source.
		
		// Remove comments if required.
		switch($filetype) {
		case 'js': case 'javascript':
			if($options['clean_js_comments'] || $options['compression_mode'] === 'all_whitespace')
				$source = self::remove_comments($source,'javascript');
			break;
		case 'css':
			if($options['clean_css_comments'] || $options['compression_mode'] === 'all_whitespace')
				$source = self::remove_comments($source,'css');
			break;
		}
		
		$out = trim(self::compress($source,$options['compression_mode'])); // Compress the source.
		$new_size = strlen($out); // Saves the new size.
		
		// Format the signature.
		if($options['show_signature']) {
			$sig = sprintf(self::SIGNATURE,$orig_size,$new_size);
			if($cache_key) $sig .= PHP_EOL . sprintf(self::CACHE_SIG,date('d M Y'));
			$out = '/* ' . PHP_EOL . $sig . PHP_EOL . '*/' . PHP_EOL . $out; // Add the signature.
		}
		
		if($cache_key) HTMLMinifier::cache($cache_key,$out); // Cache if there is a key.
		
		return $out;
		
	}
	
	// This is the function used for both caching and retrieving cached views. If only the first argument is passed, it
	// RETRIEVES a cached file. If the second argument is passed, it CACHES a file (unless the argument is false).
	// $path - Key in the absolute path of the URL.
	// $arg - Content that you want to cache the file with.
	public static function cache($path,$arg = null) {
		
		if(!$path) {
			trigger_error('Empty / invalid string provided for cache key.',E_USER_ERROR);
			return false;
		}
		
		$ext = pathinfo($path,PATHINFO_EXTENSION);
		$hash = md5($path);
		$folderpath = realpath(self::$CacheFolder);
		$fullpath = $folderpath . DIRECTORY_SEPARATOR . $hash;
		if($ext) $fullpath .= ".$ext";
		else $fullpath .= '.html';
		
		// Check if we can write into the folder.
		if(!is_writable($folderpath)) {
			trigger_error("HTMLMinifier::cache(): Assigned folder for storing the cached file '" . self::$CacheFolder . "' is not writeable or does not exist.");
			return false;
		}
		
		if($arg && gettype($arg) === 'string') {
			$arg = str_replace(self::$Signature,self::$Signature . ' ' . sprintf(self::CACHE_SIG,date('d M Y')),$arg);
			return file_put_contents($fullpath,$arg);
		} else {
			if(!file_exists($fullpath)) return false;
			elseif(!is_readable($fullpath)) { // This is just to notify the user that the cache is not working.
				trigger_error("HTMLMinifier::cache(): The cached file '$fullpath' is not readable so the cache is not working.");
				return false;
			}
			
			// Check for expiry.
			if(self::$CacheExpiry > 0 && (is_null($arg) || $arg === true)) {
				if(time() - filectime($fullpath) > self::$CacheExpiry) {
					if(!unlink($fullpath))
						trigger_error("HTMLMinifier::cache(): Unable to delete expired cached file of '$path'.");
					return false;
				}
			}
			
			return file_get_contents($fullpath);
		}		
	}
	
	// Processes options related to CSS, and moves relevant tag to the provided source for head.
	// $comments - Array from the main processing thread.
	// $conditionals - Array from the main processing thread.
	// $wrapped_conditionals - Array from the main processing thread.
	private static function process_css_options($source, $options, &$head, &$comments, &$conditionals, &$wrapped_conditionals) {	
		
		// If no CSS options are enabled, skip this part.
		if(!($options['clean_css_comments'] || $options['shift_link_tags_to_head'] || $options['shift_meta_tags_to_head'] || $options['shift_style_tags_to_head']))
			return $source;
		
		$ignore_cdata_comments = empty($options['clean_css_comments']['remove_comments_with_cdata_tags_css']);
		$ignore_link_schema_tags = !empty($options['shift_link_tags_to_head']['ignore_link_schema_tags']);
		$ignore_meta_schema_tags = !empty($options['shift_meta_tags_to_head']['ignore_meta_schema_tags']);
		
		// If we are cleaning CSS comments, clean the comments in our <head> tags first.
		if($options['clean_css_comments'] && $head) {
			
			// Check if $head is an array.
			if(is_array($head)) $head_arr = $head;
			else $head_arr = array($head);

			// Clean out comments in head.
			foreach($head_arr as $id => $head_item) {
				$head_css = self::get_tags('style',$head_item);
				foreach($head_css[0] as $k => $m) {
					if(preg_match('@^<style@i',$head_css[1][$k])) {
						$head_css_body = self::remove_comments($head_css[2][$k],'css',$ignore_cdata_comments);
						$head_arr[$id] = self::replace($m,$head_css[1][$k].$head_css_body.$head_css[3][$k],$head_item);
					}
				}
			}
			
			if(count($head_arr) > 1) $head = $head_arr;
			else $head = $head_arr[0];
		}
		
		// Target all the tags relevant to CSS.
		$targets = array('style','noscript','!--');
		if($head) $targets = array_merge(array('link','meta'),$targets);
		
		// Handle all found tags relevant to CSS.
		$css = self::get_tags($targets,$source);
		$wrapped_styles = array(); // Store all wrapped styles here in case we are combining script tags.
		foreach($css[0] as $k => $m) {
			
			if(preg_match('@^<noscript@i',$css[1][$k])) continue; // Ignore everything inside a <noscript> tag.
			
			// Evaluates what to do depending on what is the tag.
			if($head && preg_match('@^<link@i',$css[1][$k])) {
				// Shifts all found <link> tags to head.
				if($options['shift_link_tags_to_head']) {
					
					// Schema.org <link> tags can belong outside of head.
					if($ignore_link_schema_tags) {
						$attrb = self::get_tag_attributes($m);
						if(isset($attrb['itemscope'])) continue;
					}
					
					// Remove the tag from its original position.
					$source = self::replace($m,'',$source);
					
					// Does $m belong inside IE conditional tags? If so, wrap it around the conditional tag it belongs to.
					self::_is_in_wrapped_conditionals($m,$wrapped_conditionals,$source);
					
					if(is_array($head)) $head[count($head)-1] .= $m;
					else $head .= $m;

				}
			} elseif($head && preg_match('@^<meta@i',$css[1][$k])) {
								
				// Shifts all found <meta> tags to head.
				if($options['shift_meta_tags_to_head']) {
					
					// Schema.org <meta> tags can belong outside of head.
					if($ignore_meta_schema_tags) {
						$attrb = self::get_tag_attributes($m);
						if(isset($attrb['itemscope'])) continue;
					}
					
					// Remove the tag from its original position.
					$source = self::replace($m,'',$source);
					
					// Does $m belong inside IE conditional tags? If so, wrap it around the conditional tag it belongs to.
					self::_is_in_wrapped_conditionals($m,$wrapped_conditionals,$source);
					
					if(is_array($head)) $head[count($head)-1] .= $m;
					else $head .= $m;
				}
				
			} elseif(preg_match('@^<style@i',$css[1][$k])) {
				
				// Remove comments in the tag, regardless of whether we are shifting the tags.
				if($options['clean_css_comments']) {
					$css[2][$k] = self::remove_comments($css[2][$k],'css',$ignore_cdata_comments);
					$css[0][$k] = $css[1][$k].$css[2][$k].$css[3][$k];
				}
				
				// Shifts all found <style> tags to head.
				if($options['shift_style_tags_to_head']) {
					
					// Ignore <style> tags that have the scoped attribute (process them for comments first).
					$style = self::get_tag_attributes($css[1][$k]);
					if(isset($style['scoped'])) {
						if($options['clean_css_comments']) $source = self::replace($m,$css[0][$k],$source);
						continue;
					}
					
					// For use below.
					$style_tag = $css[0][$k];
					
					// Removing the tag from source and appending it to head.
					$source = self::replace($m,'',$source);
					
					// A little different from _is_in_wrapped_conditionals().
					foreach($wrapped_conditionals[2] as $k => $w) {
						
						// If we find that our tag is inside a conditional statement, wrap it up in the condition before moving it up.
						if(strpos($w,$m) !== false) {
							
							array_push($wrapped_styles,$style_tag); // Record for use later.
							
							$wrapped_conditionals[2][$k] = self::replace($m,'',$wrapped_conditionals[2][$k]);
							$style_tag = $wrapped_conditionals[1][$k] . $style_tag . $wrapped_conditionals[3][$k];
							
							// Remove this conditional from the source if there is nothing else inside it.
							// Otherwise reform the match array.
							if(trim($wrapped_conditionals[2][$k]))
								$wrapped_conditionals[0][$k] = $wrapped_conditionals[1][$k] . $wrapped_conditionals[2][$k] . $wrapped_conditionals[3][$k];
							else {
								$source = self::replace($wrapped_conditionals[3][$k],'',self::replace($wrapped_conditionals[1][$k],'',$source));
								unset($wrapped_conditionals[0][$k],$wrapped_conditionals[1][$k],$wrapped_conditionals[2][$k],$wrapped_conditionals[3][$k]);
							}
							
							// In case there is an error, here is an error for a backtrace.
							if($source === false) trigger_error('There seems to be a problem with HTMLMinifier.');
							
							break;
						}
					}
					
					if(is_array($head)) $head[count($head)-1] .= $style_tag;
					else $head .= $style_tag;

				} else {
					
					// Just reinject the comments if we are not moving them about.
					$source = self::replace($m,$css[0][$k],$source);
					
				}

			} else {
				
				$comment_tag = self::_extract_comment_tag($css[1][$k]);
				
				// If this is a valid comment tag.
				if($comment_tag && isset($comments[$comment_tag])) {
					
					// Find style tags in the comment and remove CSS comments within.
					if($options['clean_css_comments']) {
						$styles = self::get_tags('style',$comments[$comment_tag]);
						foreach($styles[0] as $key => $str) {
							if(!preg_match('@^<style@i',$str)) continue;
							$styles[2][$key] = self::remove_comments($styles[2][$key],'css',$ignore_cdata_comments);
							$styles[0][$key] = $styles[1][$key] . $styles[2][$key] . $styles[3][$key];
							$comments[$comment_tag] = self::replace($str,$styles[0][$key],$comments[$comment_tag]);
						}
					}
					
					// Ignore this section if there is no head.
					if($head) {
						// No point scanning the comments if we are not moving any tags to the head.
						if($options['shift_link_tags_to_head'] && $head) array_push($targets,'link');
						if($options['shift_style_tags_to_head']) array_push($targets,'style');
						if($options['shift_meta_tags_to_head'] && $head) array_push($targets,'meta');
						
						// Capture <noscript> tags last to deprioritise them (I think, I forget).
						array_push($targets,'noscript');

						$in_css = self::get_tags($targets,$comments[$comment_tag]);
						
						if(count($in_css[0]) > 0) {
														
							$new_cond = ''; // This is the string that will be injected into <head>.
							foreach($in_css[0] as $str) {
								if(preg_match('@^<noscript@i',$str)) continue; // Ignore contents inside <noscript> tags.
								$comments[$comment_tag] = self::replace($str,'',$comments[$comment_tag]);
								$new_cond .= $str.PHP_EOL;
							}
							
							if(preg_match('@(\\[if\\s[\\s\\S]*?\\]>)([\\s\\S]*?)(<!\\[endif\\])@i',$comments[$comment_tag],$if_cond)) {
								$numbering = $k.'hc';
								$new_cond = $if_cond[1] . $new_cond . $if_cond[3]; // Wrap up the condition in an if statement.
								$comments[$numbering] = $new_cond;
								
								if(is_array($head)) $head[count($head)-1] .= "<!-- [htmlminifier[$numbering]] -->" . PHP_EOL;
								else $head .= "<!-- [htmlminifier[$numbering]] -->" . PHP_EOL;
								
								// If this comment is all whitespace, remove it.
								if(!trim($if_cond[2])) unset($comments[$comment_tag]);
								
							} else trigger_error('It seems like there is some error in your HTML conditional.',E_USER_ERROR);
							
						}
					}
				}

			}
		}
		
		// Combine all separate style tags without attributes.
		if($head && $options['shift_style_tags_to_head'] && !empty($options['shift_style_tags_to_head']['combine_style_tags'])) {
			
			$css = self::get_tags('style|noscript',$head);
			
			// If there is only 1 tag, don't need to do this.
			if(count($css[0]) > 1) {
				$new_style = '<style>';
				foreach($css[1] as $k => $c) {
					
					if(in_array($css[0][$k],$wrapped_styles)) continue; // Ignore all <style> tags wrapped in conditionals.
					if(preg_match('@<noscript@i',$c)) continue; // Ignore all <style> tags inside <noscript> at the moment.
					
					$attrb = self::get_tag_attributes($c);
					
					// Basically, we are only combining style tags without the media attribute, or with [type="text/css"].
					if(!$attrb || (!isset($attrb['media']) && (!isset($attrb['type']) || $attrb['type'] === 'text/css'))) {
						$head = self::replace($css[0][$k],'',$head);
						$new_style .= $css[2][$k];
					}
				}
				$new_style .= '</style>';
				
				if(is_array($head)) $head[count($head)-1] .= $new_style;
				else $head .= $new_style;
			}
		}
		
		return $source;
	}
	
	// This is just a common chunk of code used in process_css_options() and process_script_options().
	// Returns true if the checked condition is in wrapped conditionals.
	private static function _is_in_wrapped_conditionals(&$tag,&$wrapped_conditionals,&$source) {
		
		// Does $m belong inside IE conditional tags? If so, wrap it around the conditional tag it belongs to.
		foreach($wrapped_conditionals[2] as $k => $w) {
			
			// If we find that our tag is inside a conditional statement, wrap it up in the condition before moving it up.
			if(strpos($w,$tag) !== false) {
				$wrapped_conditionals[2][$k] = self::replace($tag,'',$wrapped_conditionals[2][$k]);
				$tag = $wrapped_conditionals[1][$k] . $tag . $wrapped_conditionals[3][$k];
				
				// Remove this conditional from the source if there is nothing else inside it.
				// Otherwise reform the match array.
				if(trim($wrapped_conditionals[2][$k]))
					$wrapped_conditionals[0][$k] = $wrapped_conditionals[1][$k] . $wrapped_conditionals[2][$k] . $wrapped_conditionals[3][$k];
				else {
					$source = self::replace($wrapped_conditionals[3][$k],'',self::replace($wrapped_conditionals[1][$k],'',$source));
					unset($wrapped_conditionals[0][$k],$wrapped_conditionals[1][$k],$wrapped_conditionals[2][$k],$wrapped_conditionals[3][$k]);
				}
				
				// In case there is an error, here is an error for a backtrace.
				if($source === false) trigger_error('There seems to be a problem with HTMLMinifier.');
				
				return true;
			}
		}
		
		return false;
	}
	
	// Extracts the numbering inside a comment from remove_html_comments().
	private static function _extract_comment_tag($comment_statement) {
		if(preg_match('@^<!-- \\[htmlminifier\\[([0-9]*?c?)\\]\\]@',$comment_statement,$match)) return $match[1];
		return false;
	}
		
	// $scripts is the content of all script tags without src.
	private static function process_script_options($source,$options,&$comments,&$conditionals,&$wrapped_conditionals) {
				
		// If none of the options are turned on, then let's move on.
		if(!($options['clean_js_comments'] || $options['shift_script_tags_to_bottom']) || $options['add_async_defer_tag'])
			return $source;
		
		// Parse some nested options preemptively.
		$ignore_async_defer = !empty($options['shift_script_tags_to_bottom']['ignore_async_and_defer_tags']);
		$ignore_cdata_comments = empty($options['clean_js_comments']['remove_comments_with_cdata_tags_js']);
		$combine_javascript = !empty($options['shift_script_tags_to_bottom']['combine_javascript_in_script_tags']);
		
		if($options['shift_script_tags_to_bottom']) {
			$appendix = ''; // Contains all the scripts we will be appending to the end of <body>.
			if($combine_javascript)
				$script_combine = '';
		}
		
		$scripts = self::get_tags(array('script','noscript','!--'),$source);
		foreach($scripts[0] as $k => $s) {
			
			if(preg_match('@^<noscript@i',$scripts[1][$k])) continue; // Causes all tags embedded in <noscript> to be ignored.
			
			if(preg_match('@!--@',$s)) {
				
				$comment_tag = self::_extract_comment_tag($scripts[1][$k]);
				
				// If this is a valid comment tag.
				if($comment_tag && isset($comments[$comment_tag])) {
					
					$in_script = self::get_tags('script|noscript',$comments[$comment_tag]);
					if(count($in_script[0])) {
						
						$new_cond = ''; // This is the new element that is going to fit inside the conditional.
						foreach($in_script[0] as $id => $str) {
							
							if(preg_match('@^<noscript@i',$str)) continue; // Ignore contents inside <noscript> tags.
							
							$attrb = self::get_tag_attributes($str);
							
							// If this tag is not Javascript, let's ignore it and move on.
							if(isset($attrb['type']) && !preg_match('@(text|application)/(x-)?javascript@i',$attrb['type']))
								continue;
							
							// Compress script if we set script compression to true.
							if(trim($in_script[2][$id]) && $options['clean_js_comments'])
								$in_script[2][$id] = self::remove_comments($in_script[2][$id],'js',$ignore_cdata_comments);
							
							$in_script[3][$id] .= PHP_EOL; // Adds a line break for aesthetic purposes at the end of closing tag.
							
							// Clean comments in Javascript if we need to.
							$new_str = self::compress($in_script[1][$id] . $in_script[2][$id] . $in_script[3][$id],$options['compression_mode'],$options['compression_ignored_tags']);
							
							// If we are moving this tag, remove it from its original position.
							if( $options['shift_script_tags_to_bottom'] && !($ignore_async_defer && (isset($attrb['async']) || isset($attrb['defer']))) ) {
								$comments[$comment_tag] = self::replace($str,'',$comments[$comment_tag]);
								$new_cond .= $new_str;
							} else $comments[$comment_tag] = self::replace($str,$new_str,$comments[$comment_tag]);
							
						}
						
						// Pull out the current conditional tags of the comment we are iterating over.
						if(preg_match('@(\\[if\\s[\\s\\S]*?\\]>)([\\s\\S]*?)(<!\\[endif\\])@i',$comments[$comment_tag],$if_cond)) {
							
							// If this comment is all whitespace, remove it.
							if(!trim($if_cond[2])) unset($comments[$comment_tag]);
							
							// If we are shifting the tags to the bottom...
							if($options['shift_script_tags_to_bottom']) {
								// Create a new comment, seed it with a tag, and add the actual comment to the comments array.
								$numbering = $k.'fc';
								$new_cond = $if_cond[1] . $new_cond . $if_cond[3];
								$comments[$numbering] = $new_cond;
								$appendix .= "<!-- [htmlminifier[$numbering]] -->" . PHP_EOL; // Adds this to the end of the document.
							}
							
						} else trigger_error('It seems like there is some error in your HTML conditional: ' . $if_cond[0],E_USER_ERROR);
						
					}
				}
			} else {

				$attrb = self::get_tag_attributes($scripts[1][$k]);
				
				// If this tag is not Javascript, let's ignore it and move on.
				if(isset($attrb['type']) && !preg_match('@(text|application)/(x-)?javascript@i',$attrb['type']))
					continue;
				
				// Wrap scripts in conditionals with respective conditionals.
				$is_wrapped = self::_is_in_wrapped_conditionals($scripts[0][$k],$wrapped_conditionals,$source);
				if($is_wrapped){
					$scripts[1][$k] = substr($scripts[0][$k],0,strpos($scripts[0][$k],$scripts[1][$k])+strlen($scripts[1][$k]));
					$scripts[3][$k] = substr($scripts[0][$k],strpos($scripts[0][$k],$scripts[3][$k]));
				}
				
				// If this is an inline script, try and clean its comments.
				if($options['clean_js_comments'] && trim($scripts[2][$k])) {
					$scripts[2][$k] = self::remove_comments($scripts[2][$k],'js',$ignore_cdata_comments);
					$scripts[0][$k] = $scripts[1][$k] . $scripts[2][$k] . $scripts[3][$k];
				}
				
				if($options['shift_script_tags_to_bottom']) {
					
					// Don't move this tag if it has the async or defer attribute.
					if( $ignore_async_defer && (isset($attrb['async']) || isset($attrb['defer'])) ) continue;
					
					// Figure out if this is a piece of script we should combine or just append at the end.
					if(!isset($attrb['id']) && !$is_wrapped && trim($scripts[2][$k]) && $combine_javascript) {
						
						// We are moving the script to the end of the page.
						$source = self::replace($s,'',$source);
						$script_combine .= $scripts[2][$k] . PHP_EOL;
						continue;
						
					}
					
					// We are just going to append this piece of script at the end.
					$source = self::replace($s,'',$source);
					$appendix .= $scripts[0][$k] . PHP_EOL;
				} else {
					$source = self::replace($s,$scripts[0][$k],$source);
				}
			}
		}
		
		// Grab the body tag(s) in the document.
		$body_tags = self::get_tags('body',$source);
		$body_count = count($body_tags);
		
		$body = null;
		if($body_count > 1) {
			if($options['merge_multiple_body_tags']) {
				$body = '';
				foreach($body_tags[2] as $b) {
					$source = self::replace($b,'',$source);
					$body .= $b;
				}
			} else {
				$body = array();
				foreach($body_tags[2] as $b) {
					$source = self::replace($b,'',$source);
					array_push($body,$b);
				}
			}
		} elseif($body_count === 1) {
			$body = $body_tags[2][0];
			$source = self::replace($body,'',$source);
		}
		
		if($options['shift_script_tags_to_bottom']) {
			// Stuff $appendix and $script_combine into the end of the body tag.
			if(isset($script_combine)) $appendix .= '<script>'.$script_combine.'</script>';
			
			if($body) {
				if(is_array($body)) $body[$body_count-1] .= $appendix;
				else $body .= $appendix;
			} else {
				// We should try and append the appendix to a HTML tag first, before adding it directly to source.
				$source .= $appendix;
			}
		}
		
		// Put <body> back.
		if($body) {
			$empty_bodies = self::get_tags('body',$source);
			if(count($empty_bodies[0]) > 0) {
				if(is_array($body)) {
					foreach($empty_bodies[0] as $i => $m) {
						if(empty($body[$i])) $source = self::replace($m,'',$source); // Remove this tag if there are no contents for it.
						else $source = self::replace($m,$empty_bodies[1][$i] . $body[$i] . $empty_bodies[3][$i],$source);
					}
				} else {
					$source = self::replace($empty_bodies[0][0],$empty_bodies[1][0] . $body . $empty_bodies[3][0],$source);
					unset($empty_bodies[0][0],$empty_bodies[1][0],$empty_bodies[2][0],$empty_bodies[3][0]); // Remove these matches as they have been used.
					foreach($empty_bodies[0] as $m) $source = self::replace($m,'',$source);
				}
			} else trigger_error('Trying to put back &lt;body&gt; tag contents, but we cannot any empty &lt;body&gt; tag anymore!',E_USER_ERROR);
		}
		
		return $source;

	}
	
	// Shortcut for using substring replace.
	private static function replace($search,$replacement,$subject) {
		$idx = strpos($subject,$search);
		if($idx !== false) return substr_replace($subject,$replacement,$idx,strlen($search));
		return $idx;
	}
	
	// Finds tags of a certain name and returns an array of matches.
	private static function get_tags($tagName,$source,$disallowNesting = true) {
		
		switch(gettype($tagName)) {
		case 'string':
			$preg_tag = $tagName;
			break;
		case 'array':
			foreach($tagName as $k => $t) $tagName[$k] = preg_quote($t);
			$preg_tag = implode('|',$tagName);
		}
		
		$src_end = strlen($source)-1; // Calculate last index of $source.
		$result = array(array(),array(),array(),array()); // Simulate a preg_match() array; 0: full result, 1: opening tag, 2: contents, 3: closing tag.
		$source_pointer = 0; // For tracking how far down the source we have been searching.
		
		$regex = sprintf('@<(%s)(?:\\s[\\s\\S]*?)?/?>@i',$preg_tag);
		$k = 0; // Counter for number of matches in loop below.
		
		// Keep finding tags until we reach the end, or have no more matches.
		// We are not using preg_match_all because we don't want to match the same content multiple times.
		// e.g. If there is a <style> in a <noscript>, we only want to capture the <noscript>.
		while($source_pointer <= $src_end){
			
			// If there are no matches, end the loop.
			if(!preg_match($regex,$source,$match,PREG_OFFSET_CAPTURE,$source_pointer)) break;
			
			$result[0][$k] = $result[1][$k] = $match[0][0];
			$source_pointer = $match[0][1];
			
			// Match for self-closing tag. If it is not, then find the closing tag.
			if(!in_array($match[1][0],self::$SelfClosingTags)) {
				
				$result[2][$k] = $result[3][$k] = '';
				
				// Move pointer beyond start tag.
				$c_start = $match[0][1]+strlen($match[0][0]);
				
				// Find ending / nested tags.
				$match_preg = preg_quote($match[1][0]);
				if(!preg_match('@<(?:(/)'.$match_preg.'\\s*|'.$match_preg.'[\\s\\S]*?)>@i',$source,$c_end_match,PREG_OFFSET_CAPTURE,$c_start)) {
					// If there are no matches, it means that there are no further tags of this sort. Treat as floating tag.
					unset($result[0][$k],$result[1][$k],$result[2][$k],$result[3][$k]);
					$source_pointer = $c_start;
					continue;
				}
				
				// If there is a nested opening tag, then let's handle it.
				if(empty($c_end_match[1])) {
					
					if($disallowNesting) {
						trigger_error('You cannot nest &lt;'.$match[1][0].'&gt; tags inside each other in your source.');
						return false;
					}
					
					$nests = 2;
					while($nests > 0) {
						$source_pointer = $c_end_match[0][1] + strlen($c_end_match[0][0]);
						if(preg_match('@<(?:(/)'.$match_preg.'\\s*|'.$match_preg.'[\\s\\S]*?)>@i',$source,$c_end_match,PREG_OFFSET_CAPTURE,$source_pointer)) {
							if(empty($c_end_match[1])) $nests++;
							else $nests--;
						} else {
							unset($result[0][$k],$result[1][$k],$result[2][$k],$result[3][$k]);
							$source_pointer = $c_start;
							continue 2;
						}
					}
				}
				$c_end = $c_end_match[0][1];
				$result[2][$k] = substr($source,$c_start,$c_end-$c_start);
				
				// Compute for closing tag.
				$c_term = $c_end+2+strlen($match[1][0]);
				$char = substr($source,$c_term++,1);
				while($char !== '>') {
					// For malformed HTML documents.
					if($c_term > $src_end) {
						trigger_error('Incomplete closing tag found; your source has not been minified. Search "'.htmlspecialchars(substr($source,$c_end,$c_term-$c_end)).'" in the source below.');
						return false;
					}
					if(!ctype_space($char)) {
						trigger_error('You have a closing tag with attributes; your source has not been minified. Search "'.htmlspecialchars(substr($source,$c_end,$c_term-$c_end)).'" in the source displayed below to find the issue.');
						return false;
					}
					
					// If everything is ok, move on.
					$char = substr($source,$c_term++,1);
				}
				$result[3][$k] = substr($source,$c_end,$c_term-$c_end);
				
				// Compute for full tag.
				$result[0][$k] .= $result[2][$k].$result[3][$k];
			}
			
			$source_pointer += strlen($result[0][$k++]); // Moves the pointer downwards and increments $k.
			$match = array();
		}
		
		return $result;
	}
	
	private static function create_tag($tagName,$content = '',$attributes = false) {
		$out = "<$tagName";
		if(is_array($attributes) && count($attributes) > 0) {
			$out .= ' ';
			foreach($attributes as $k => $v) $out .= "$k=\"$v\" ";
			$out = rtrim($out) . '>';
		}
		return $out . $content . "</$tagName>";
	}
	
	// Takes an opening HTML tag and segregates it into key value pairs in an array.
	private static function get_tag_attributes($tag) {
		preg_match('@^<[a-z0-9_\\-\\.:]+(\\s[\\s\\S]*?)?>$@i',$tag,$match);
		if(isset($match[1])) {
			
			if(preg_match_all('@([a-z0-9_\\-\\.:]+)(?:=("[\\s\\S]*?"|\'[\\s\\S]*?\'))?@i',$match[1],$attrb)) {
				$r = array();
				foreach($attrb[0] as $k => $a) {
					if(empty($attrb[2][$k])) $r[$attrb[1][$k]] = true;
					else $r[$attrb[1][$k]] = substr($attrb[2][$k],1,strlen($attrb[2][$k])-2);
				}
				return $r;
			}
			return null;
		}
		return null;
	}
	
	// Given a compression string, returns compressed HTML output.
	// $excludedTags: Give an array of tags whose contents you don't want to compress.
	public static function compress($out,$type,$excludedTags = null) {
		
		// Remove all tags that are excluded and replace them after compression.
		if(is_array($excludedTags)) {
			$substitutes = array();
			$tags = self::get_tags($excludedTags,$out);
			foreach($tags[0] as $k => $t) {
				$out = self::replace($t,"<!-- [[ htmlminifier_compressed_$k ]] -->",$out);
				$substitutes[$k] = $t;
			}
		}
		
		// Actual compression.
		switch($type) {
		case 'all_whitespace_not_newlines':
		case 'pretty_indent':
			$out = preg_replace("/^\\s+|\\s+$/m",'',$out);
			break;
		case 'all_whitespace':
			$out = preg_replace('/\\s+/m',' ',$out); // Temporary fix for Wordpress source.
			break;
		}
		
		// Return the substituted tags.
		if(!empty($substitutes)) {
			foreach($substitutes as $k => $t)
				$out = self::replace("<!-- [[ htmlminifier_compressed_$k ]] -->",$t,$out);
		}
		
		// Return the compressed contents.
		return $out;
	}
	
	// Removes CSS or JS comments
	private static function remove_comments($source,$type = 'javascript', $ignoreCdataComments = true) {
		
		// Uses the regular expressions in self::$RegexArray.
		$regex = array(
			// Capture these things, because otherwise comment characters in these boundaries will be captured.
			'string_single' => "\\'.*?\\'",
			'string_double' => '\\".*?\\"',
			
			// Things that are captured and removed.
			'comment_single' => '//[\\s\\S]*?\\R',
			'comment_multi' => '/\\*[\\s\\S]*?\\*/'
		);
		if($type === 'css') $regex = array_merge(array('css_url_function' => 'url\\([\\s\\S]*?\\)'),$regex);
		elseif($type === 'javascript' || $type === 'js') $regex = array_merge( array( 'js_regex_string' => '/(?!/|\\*).+?(?<!\\\\)/'),$regex );
		$full_regex = '@(?:'.implode('|',$regex).')@i';
		
		// Nab us everything in the regex.
		if(preg_match_all($full_regex,$source,$match) <= 0)
			return $source;
		
		foreach($match[0] as $m) {
			// Ignoring comment notated inside strings, regexes or the CSS URL function.
			if(preg_match('/^'.$regex['string_single'].'$/',$m)) continue;
			if(preg_match('/^'.$regex['string_double'].'$/',$m)) continue;
			if($type === 'css' && preg_match('/^'.$regex['css_url_function'].'$/',$m)) continue;
			if(!empty($regex['js_regex_string']) && preg_match('@^' . $regex['js_regex_string'] . '$@',$m)) continue;
			
			// Ignoring components with CDATA.
			if($ignoreCdataComments && preg_match('/(?:<!\\[CDATA\\[|\\]\\]>)/',$m)) continue;
			$source = self::replace($m,'',$source);
		}
		
		return $source;			
	}
	
	// Remove HTML comments in the source.
	// $removedComments: Pass an array here to store all the removed comments.
	// $conditionalsRecord: Pass an array here to get the indexes of all comments that are conditionals.
	private static function remove_html_comments($source,&$removedComments = null,&$conditionalsRecord = null,$clean_normal_comments = true) {
		// By capturing script and style tags too, we ignore HTML comments made INSIDE these tags.
		$regex = array(
			'comment' => '<!--([\\s\\S]*?)-->', // Remove all comments except [if ] blocks.
			'script' => '(\\<(?:script|style)(?:\\s+[\\s\\S]*?)?\\>([\\s\\S]*?)\\</(?:script|style)\\s*?\\>)'
		);
		$full_regex = '@(?:'.implode('|',$regex).')@';
		
		// Nab us all the comments!
		preg_match_all($full_regex,$source,$match);
		
		// If the variable is not an array, null it.
		if(!is_array($removedComments)) $removedComments = null;
		if(!is_array($conditionalsRecord)) $conditionalsRecord = null;
		
		$i = 0; // This is for numbering the comments.
		foreach($match[1] as $k => $m) {
			if($m) { // This will make it ignore all script / style tags.
				
				$numbering = strval($i++);
				
				// Do stuff if its an IE conditional comment.
				// NOTE: Detection system will break in nested if statements.
				$is_conditional = false;
				if(preg_match('@^\\s*\\[if@i',$m)) {
					if(preg_match('@<!\\[endif\\]$@i',$m)) $numbering .= 'c';
					else $numbering .= 'cs';
					array_push($conditionalsRecord,$numbering);
					$is_conditional = true;
				} elseif(preg_match('@\\s*(<!)?\\[endif@i',$m)) {
					$numbering .= 'ce';
					array_push($conditionalsRecord,$numbering);
					$is_conditional = true;
				}
				
				// Note: Leaves an empty comment in place of the removed comments.
				if($removedComments !== null) {
					if($is_conditional || !$clean_normal_comments) $removedComments[$numbering] = $m;
					$source = self::replace($match[0][$k],"<!-- [htmlminifier[$numbering]] -->",$source);
				} else $source = self::replace($match[0][$k],"<!-- [htmlminifier[$numbering]] -->",$source);
			}
		}
		return $source;
	}
}