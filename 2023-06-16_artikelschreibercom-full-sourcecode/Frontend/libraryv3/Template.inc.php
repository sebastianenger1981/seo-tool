<?php

	/* Template System created by Andi */
	class Template {
		public static $dir;

		public static function setPath($dir) {
			self::$dir = $dir;
		}

		//return parsed file
		private function parse($file) {
		#	 if (ob_get_length() > 0) {
		#		ob_end_clean();
		#	  }
		#	
		#	ob_start();
		#	@include($file);
		#	$buffer = ob_get_contents();
		#	ob_end_clean();
			$buffer = file_get_contents($file);
			return trim($buffer);
		}
		
		private function readCache($cacheFile,$expireTime) {
			if(file_exists(self::$dir.'/cache/'.$cacheFile)&&filemtime(self::$dir.'/cache/'.$cacheFile) > (time()-$expireTime)){
				return file_get_contents(self::$dir.'/cache/'.$cacheFile.'.php');
			}
			return false;
		}
		
		private function writeCache($cacheFile,$content){
			$fp=fopen(self::$dir.'/cache/'.$cacheFile.'.php','w');
			fwrite($fp,$content);
			fclose($fp);
		} 
		
		//flushCache: Removes all files in the cache
		public function flushCache() {
			$files = glob(self::$dir.'/cache/*');
			foreach($files as $file) {
				@unlink($file); 
			}
		}
		
		public function data($tplname, $content) {
			return $this->display($tplname, $content, false);
		}
		
		public function display($tplname, $content, $print=true) {
			return $this->display_internal($tplname, $content, $print, false, 0);
		}
		
		public function display_cache($tplname, $content, $print, $expire_time="default") {
			if($expire_time == "default") $expire_time = 3*3600; //default caching for 3 hours
			
			return $this->display_internal($tplname, $content, $print, $print, $expire_time);
		}
		
		private function display_internal($tplname, $content, $print=true, $caching=false, $expire_time) {  
			if(is_array($content)) {
				if(!empty(self::$dir)) {
				
					//check if there is a cache available
					if($caching) {
						if($this->readCache($tplname, $expire_time)) {
							$data = file_get_contents(self::$dir.'/cache/'.$tplname);
							
							if($print)
								echo $data; 
							else
								return $data;	
								
							return ""; //no data if $print was set
						}
					}
				
					$fname = self::$dir.'/'.$tplname.'.tpl';
					$data = $this->parse($fname);				
					if(!empty($data)) {
						//if no css style is set choose a default one
						if(!isset($content['cssstyle'])) {
							$content['cssstyle'] = self::$dir."/css/style.css";
						}
						if(!isset($content['javascriptcontent'])) {
							$content['javascriptcontent'] = "";
						}
						
						//$data = fread($fd, filesize($fname));		
						foreach($content as $k => $v) {
//							echo 'Replace {'.$k.'} by '.$v.'<br />';	
							$data = str_replace('{'.$k.'}', $v, $data);
						}
						
						//check if there needs a cache file to be written
						if($caching) {
							$this->writeCache($tplname, $data);
						}
				
						if($print)
							echo $data; 
						else
							return $data;
							
					} else {
						return false;
					}
					
				} else {
					echo('Specifiy a target template directory using setPath method.');
				}
			} else {
				echo('$content has to be an array with keys.');
			}
			return true;
		}
	}
	$design = new Template();
?>
