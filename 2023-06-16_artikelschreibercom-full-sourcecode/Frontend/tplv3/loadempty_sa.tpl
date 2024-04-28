<!--
Copyright (c) 2023, Sebastian Enger, M.Sc.
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree(BSD-4-Clause).  

Frontend and Backend Source Code for Project:
- https://www.artikelschreiber.com/
- https://www.artikelschreiben.com/
- https://www.unaique.net/
-->
<!DOCTYPE html>
<html lang="ar">
	<head>
		<link rel="preload" href="https://www.artikelschreiber.com/js/jquery.min.js" as="script" />
		<title>{title} {suchanfrage}</title>
		<meta charset="UTF-8" />
		<meta name='robots' content='index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1' />
		<meta name="viewport" content="width=device-width, height=device-height, user-scalable=1, initial-scale=1" />
		<meta name="keywords" content="كتابة ، مولد نص ، مقال ، نصوص ، كتابة إبداعية ، إنشاء مقال ، كاتب مقال ، منشئ محتوى ، إنشاء محتوى ، سرد القصص ، مقالات مجانية ، نص فريد ، محتوى فريد ، كاتب مقال ، مؤلف ، مؤلف ، مؤلف ، صحفي ، صحفي ، محرر ، محرر ، وسائط ، صحيفة ، مقال صحفي ، منشور ، كتابة مقال ، كتابة نصوص ، كتابة نصوص" />
		<meta name="description" content="{description} {suchanfrage}" />
		<meta name="mobile-web-app-capable" content="yes" />
		<meta name="google-site-verification" content="fPXCs0AV0WPev8eVSxGwzMNZGIQ7c6BS-OAa2mUg37A" />
		<meta property="og:title" content="{title} {suchanfrage}" />
		<meta property="og:description" content="{description} {suchanfrage}" />
		<meta property="og:url" content="https://www.artikelschreiber.com/" />
		<meta property="og:image" content="https://www.artikelschreiber.com/images/apple-icon-200x200.png" />
		<meta property="og:site_name" content="ArtikelSchreiber" />
		<meta property="og:locale" content="sa_SA" />
		<meta property="og:type" content="Website" />
		<meta name="twitter:card" content="summary_large_image" />
		<meta name="twitter:site" content="artikelschreiber.com"  />
		<meta name="twitter:title" content="{title} {suchanfrage}" />
		<meta name="twitter:description" content="{description} {suchanfrage}" />
		<meta name="twitter:creator" content="artikelschreiber.com" />
		<meta name="twitter:image:src" content="https://www.artikelschreiber.com/images/apple-icon-200x200.png" />
		<meta name="twitter:domain" content="www.artikelschreiber.com" />
		<meta name="twitter:url" content="https://www.artikelschreiber.com/" />
		<meta name="twitter:image" content="https://www.artikelschreiber.com/images/apple-icon-200x200.png" />
		
		<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png" />
		
		<link rel="alternate" hreflang="de" href="https://www.artikelschreiber.com/" />
		<link rel="alternate" hreflang="en" href="https://www.artikelschreiber.com/en/" />
		<link rel="alternate" hreflang="fr" href="https://www.artikelschreiber.com/fr/" />
		<link rel="alternate" hreflang="es" href="https://www.artikelschreiber.com/es/" />
		<link rel="alternate" hreflang="it" href="https://www.artikelschreiber.com/it/" />
		<link rel="alternate" hreflang="ru" href="https://www.artikelschreiber.com/ru/" />
		<link rel="alternate" hreflang="zn" href="https://www.artikelschreiber.com/cn/" />
		<link rel="alternate" hreflang="ja" href="https://www.artikelschreiber.com/jp/" />
		<link rel="alternate" hreflang="pt" href="https://www.artikelschreiber.com/pt/" />
		<link rel="alternate" hreflang="in" href="https://www.artikelschreiber.com/hi/" />
		<link rel="alternate" hreflang="ar" href="https://www.artikelschreiber.com/ar/" />
		<link rel="canonical" href="{canonical}" />
		<link rel="alternate" href="{canonical}" hreflang="x-default" />
		<link rel="alternate" href="{startpage_url}texts/feed.php" title="RSS feed | ArtikelSchreiber.com" type="application/rss+xml" />
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
			
			.center{display:block;margin-left:auto;margin-right:auto;width:50%,max-width: 100%; height: auto;}
			
			.loader{border:16px solid #f3f3f3;border-top:16px solid #3498db;border-radius:50%;width:120px;height:120px;animation:2s linear infinite spin}@keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
		</style>
	</head>
	
	<body style="text-align:center; overflow-wrap: break-word; word-wrap: normal; word-break: break-word;" translate="yes" lang="ar">
		<div class="container">
			<h4 id="showBanner">
				<fieldset lang="ar">
					<textarea class="linkme" id="myInput" name="myInput"><a href="{url_linking}" target="_self" hreflang="{language}" title="{description_linking}">{title_linking}</a></textarea>

					<div class="tooltip">
					<button onclick="myFunction();" onmouseout="outFunc()" title="انقر هنا لنسخ النص إلى الحافظة!">
					  <span class="tooltiptext" id="myTooltip">نسخ إلى الحافظة</span>
					 نسخ النص
					  </button>
					</div>
					
					<p>
						<b><u id="SocialShareButtons">شارك النص مع الأصدقاء:</u></b> &nbsp;&nbsp;&nbsp;
						
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
				<fieldset lang="ar">
					<legend><b>معلومات الحالة:</b></legend>
					<p>
						<ul>
							<li>الرجاء ترك هذا الموقع أو علامة التبويب هذه مفتوحة - سأتحقق بانتظام لمعرفة ما إذا كانت مقالتك قد اكتملت. </li>
							<li>إذا كان الأمر كذلك ، فسوف أريكم ذلك ، وإذا لم يكن الأمر كذلك ، فسأحاول مرة أخرى بعد بضع ثوان. </li>
							<li>يرجى الانتظار - يستغرق الأمر بعض الوقت حتى يتم الانتهاء من العنصر الفردي الخاص بك (إنه يستحق ذلك !!!).</li>
							<li>الخدمة حاليا مشغولة جدا. مقالتك قد يستغرق وقتا أطول من المعتاد ليكتمل.</li>
							<li>بعد كتابة مقالتك الفريدة ، يمكنك تنزيلها كملف نصي مجانًا أو مجانًا.</li>
						</ul>
					</p>
				</fieldset>
			</h4>
			<br />
			<fieldset lang="ar">
				<legend><b>التقدم في إنشاء مقالتك:</b></legend>
				<div class="center loader"></div>
				<span id="body" style="text-align: left;"></span>
				<span id="statusMessage"></span>
			</fieldset>
		</div>
	
	<script src="https://www.artikelschreiber.com/js/jquery.min.js"></script>
	
	<script>
		var timer;
		
		function eraseCookie(k){document.cookie = k + '=; Max-Age=0'}
		function readCookie(k){return(document.cookie.match('(^|; )'+k+'=([^;]*)')||0)[2]}
		var sidVal2 = readCookie("DemoArtikelSessionID");
		
		function checkForArticle(){
			$.ajax({
				type: "POST",
				url: "https://www.artikelschreiber.com/textgenerator.php",
				dataType: "text",
				data: { 
					"do": "check",
					"lang": "ar",
					"uniqueidentifier": sidVal2, 
				},
				
				cache: false,
				success: function(htmlv1){
					$('#body').empty();
					
					var i 	= htmlv1;
					var n 	= htmlv1.length;

					console.log("h length:"+n);
					console.log("h:"+i);
					if (i !== undefined && n>250){
						$('#body').html(htmlv1).show();
						clearInterval(timer);
											
						$('#showBanner').remove();
						$('#showBanner').empty();
						
						$('.loader').remove();
						$('.loader').empty();
						
						$('.loading').remove();
						$('.loading').empty();
						
						$('#statusMessage').remove();
						$('#statusMessage').empty();
					}
					return;
				}
			})
		}  
		
		function copyDivToClipboard() {
			var range = window.getSelection().getRangeAt(0);
			range.selectNode(document.getElementById("a"));
			window.getSelection().addRange(range);
			document.execCommand("copy")
		}
		
		function loading(){
		  var num = 1;
		  $('.loading span').html(num+'%');
			for(i=0; i<=35000; i++) {
				setTimeout(function() { 
					if (num>99){
						num = 99;
					}
					$('.loading span').html(num+'%');
				   	num++;
					if(num>=99){
						$('#statusMessage').html("<br /><br /><br /><b>قم بتنفيذ الخطوة 5: التقط العنصر الخاص بك!</b>").show();
					} else if(num>=55){
						$('#statusMessage').html("<br /><br /><br /><b>قم بتنفيذ الخطوة 4: قم بإنشاء النص الفردي الخاص بك!</b>").show();
					} else if(num>=20){
						$('#statusMessage').html("<br /><br /><br /><b>نفذ خطوة العمل 3: استخدم أدوات معالجة اللغة الطبيعية للمعالجة المسبقة لجميع الموارد التي تم العثور عليها!</b>").show();
					} else if(num>=10){
						$('#statusMessage').html("<br /><br /><br /><b>نفذ الخطوة 2: استخدم مصادر المحتوى!</b>").show();
					}else if(num>=1){
						$('#statusMessage').html("<br /><br /><br /><b>نفذ خطوة العمل 1: قم بتقييم كلماتك الرئيسية!</b>").show();
					}
				},30000);
			};
		}
		
	$(document).ready(function() {
		timer = setInterval(checkForArticle, 15000);
		loading();
				 
		var data2 		= "";
		var data1 		= "";
		$("#submit").click(function() {
			var email 	= $("#email").val();
			$("#returnmessage").empty();
			$.post("https://www.artikelschreiber.com/ajax/email.php", {
				data_id1: data1,
				data_id2: data2,
				email: email
				}, function(data) {
					$("#returnmessage").html(data); 
					if (data == "Your Query has been received, We will contact you soon.") {
						$("#form")[0].reset();
					}
				}); 
			 return false; 
		}); 
	});
</script>
	
	<script type="text/javascript" async>
		function addLink(){
			var selection 	= window.getSelection();
			navigator.clipboard.writeText(selection+"<br /><br />"+"{contentLinkNewDiv}");
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
  tooltip.innerHTML = "تم النسخ بنجاح!";// + copyText.value;
}

function outFunc() {
  var tooltip = document.getElementById("myTooltip");
  tooltip.innerHTML = "نسخ إلى الحافظة";
}
</script>

<script async>
document.getElementById("shareFacebook").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u='+'https://www.artikelschreiber.com/sa/'+'">Facebook</a>';
document.getElementById("shareTwitter").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://twitter.com/share?url='+'https://www.artikelschreiber.com/sa/'+'">Twitter</a>';
document.getElementById("shareWhatsApp").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="whatsapp://send?text='+'https://www.artikelschreiber.com/sa/'+'">WhatsApp</a>';
document.getElementById("shareLinkedIn").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="http://www.linkedin.com/shareArticle?mini=true&url='+'https://www.artikelschreiber.com/sa/'+'">LinkedIn</a>';
document.getElementById("shareEmail").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="mailto:?subject=Check out the free ArtikelSchreiber.com&body='+'https://www.artikelschreiber.com/sa/'+'">eMail</a>';
document.getElementById("sharevKontakte").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="http://vkontakte.ru/share.php?url='+'https://www.artikelschreiber.com/sa/'+'">vKontakte</a>';
document.getElementById("shareTumblr").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="http://www.tumblr.com/share/link?url='+'https://www.artikelschreiber.com/sa/'+'">Tumblr</a>';
document.getElementById("shareLineit").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://lineit.line.me/share/ui?url='+'https://www.artikelschreiber.com/sa/'+'">LineIT</a>';
document.getElementById("shareSkype").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://web.skype.com/share?url='+'https://www.artikelschreiber.com/sa/'+'">Skype</a>';
document.getElementById("shareTelegram").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://telegram.me/share/url?url='+'https://www.artikelschreiber.com/sa/'+'">Telegram</a>';
document.getElementById("shareSnapChat").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://snapchat.com/scan?attachmentUrl='+'https://www.artikelschreiber.com/sa/'+'">SnapChat</a>';
document.getElementById("shareReddit").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="http://reddit.com/submit?url='+'https://www.artikelschreiber.com/sa/'+'">Reddit</a>';
document.getElementById("shareFlipboard").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://share.flipboard.com/bookmarklet/popout?url='+'https://www.artikelschreiber.com/sa/'+'">Flipboard</a>';
document.getElementById("shareXing").innerHTML = '<a rel="noopener noreferrer nofollow" target="_blank" href="https://www.xing.com/spi/shares/new?url='+'https://www.artikelschreiber.com/sa/'+'">XING</a>';
</script>

</body>
</html>