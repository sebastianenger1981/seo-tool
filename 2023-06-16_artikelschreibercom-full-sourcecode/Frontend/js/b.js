﻿function isMobile(){return/Mobi/.test(navigator.userAgent)}function getBrowserName(){return window.opr&&window.opr.addons||window.opera||0<=navigator.userAgent.indexOf(" OPR/")?"Opera":"undefined"!=typeof InstallTrigger?"Firefox":/constructor/i.test(window.HTMLElement)||"[object SafariRemoteNotification]"===(!window.safari).toString()?"Safari":document.documentMode?"Internet Explorer":!document.documentMode&&window.StyleMedia?"Microsoft Edge":window.chrome?"Chrome":void 0}function getOSName(){var e;if(isMobile())if(/Windows/.test(navigator.userAgent))e="Windows",/Phone 8.0/.test(navigator.userAgent)?e+=" Phone 8.0":/Phone 10.0/.test(navigator.userAgent)&&(e+=" Phone 10.0");else if(/Android/.test(navigator.userAgent)){e=(n=function(){if(/Android/.test(navigator.appVersion))return navigator.appVersion.match(/Android (\d+).(\d+)/)}())[0]}else if(/iPhone;/.test(navigator.userAgent)){function t(){if(/iP(hone|od|ad)/.test(navigator.appVersion)){var e=navigator.appVersion.match(/OS (\d+)_(\d+)_?(\d+)?/);return[parseInt(e[1],10),parseInt(e[2],10),parseInt(e[3]||0,10)]}}e="iOS "+(n=t())[0]+"."+n[1]+"."+n[2]}else if(/iPad;/.test(navigator.userAgent)){function t(){if(/iP(hone|od|ad)/.test(navigator.appVersion)){var e=navigator.appVersion.match(/OS (\d+)_(\d+)_?(\d+)?/);return[parseInt(e[1],10),parseInt(e[2],10),parseInt(e[3]||0,10)]}}var n;e="iOS "+(n=t())[0]+"."+n[1]+"."+n[2]}else/BBd*/.test(navigator.userAgent)&&(e="BlackBerry");else/Windows/.test(navigator.userAgent)?(e="Windows",/5.1;/.test(navigator.userAgent)?e+=" XP":/6.0;/.test(navigator.userAgent)?e+=" Vista":/6.1;/.test(navigator.userAgent)?e+=" 7":/6.2/.test(navigator.userAgent)?e+=" 8":/10.0;/.test(navigator.userAgent)&&(e+=" 10"),/64/.test(navigator.userAgent)?e+=" 64-bit":e+=" 32-bit"):/Macintosh/.test(navigator.userAgent)&&(e="Macintosh",/OS X/.test(navigator.userAgent)&&(e+=" OS X"));return e}function getBrowser(){return{os:getOSName(),browser:getBrowserName(),language:navigator.language,languages:navigator.languages,user_agent:navigator.userAgent,device:isMobile()?"Mobile":"Desktop",referrer:document.referrer||"N/A",online:navigator.onLine,timezone:Intl.DateTimeFormat().resolvedOptions().timeZone,screen_resolution:screen.width+" x "+screen.height,cookie_enabled:navigator.cookieEnabled}}