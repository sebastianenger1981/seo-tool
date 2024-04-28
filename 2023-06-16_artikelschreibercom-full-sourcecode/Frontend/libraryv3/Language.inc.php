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
class Language {
	public function writeAuthorText($language){ // in Language.inc.php auslagern
		if (strcasecmp($language,"de") == 0){
			$html =<<<END
			<ul role="list">
				<li lang="de" role="listitem">Dieser Artikel wurde mit dem kostenlosen ArtikelSchreiber.com zum <a href="https://www.artikelschreiber.com/" target="_self" hreflang="de" title="https://www.artikelschreiber.com/">Text schreiben</a> erstellt. </li>			
				<li lang="de" role="listitem">Unsere weiteren kostenlose Dienste mit KI sind https://www.unaique.net/, der <a href="https://www.unaique.net/" target="_self" title="https://www.unaique.net/" hreflang="de">KI Text Generator</a>		
				<li lang="de" role="listitem">Wir bieten einen kostenlosen KI Content Generator auf www.unaique.com als <a href='https://www.unaique.com/' title='AI WRITER - Content Generator | UNAIQUE.COM' target='_self' hreflang='en'>AI WRITER</a>.</li>
				<li lang="de" role="listitem">Auf <a href="https://rechthaben.net/" target="_self" title="https://rechthaben.net/" hreflang="de">Recht Haben</a> bieten wir kostenlose Anleitungen und Muster, wie man sich mit Recht wehrt.</li>
			</ul>
END;
		} else {
		$html =<<<END
			<ul role="list">
				<li lang="en" role="listitem">This Article Text has been written automatically with the free of cost service <a href="https://www.artikelschreiber.com/" target="_self" hreflang="de" title="https://www.artikelschreiber.com/">Text schreiben</a>. </li>			
				<li lang="en" role="listitem">Our other free services are https://www.unaique.net/ called <a href="https://www.unaique.net/" target="_self" title="https://www.unaique.net/" hreflang="de">KI Text Generator</a>		
				<li lang="en" role="listitem">We offer a free of costs AI Content Generator based on GPT-3 and GPT-4 on the Website <a href='https://www.unaique.com/' title='AI WRITER - Content Generator | UNAIQUE.COM' target='_self' hreflang='en'>AI WRITER</a></li>
				<li lang="de" role="listitem">Auf <a href="https://rechthaben.net/" target="_self" title="https://rechthaben.net/" hreflang="de">Recht Haben</a> bieten wir Anleitungen und Muster, wie man sich mit Recht wehrt.</li>
			</ul>
END;
		}
		return $html;
	} // function writeAuthorText(){
	
	public function checkExistingLanguage($lang){
		$valid_langs = array('de','en','es','fr','it','jp','in','sa','cn','ru','tr','pt','ja','ar','zh');
		if (strlen($lang) == 2){
			if (in_array($lang, $valid_langs)){
				return True;
			} // if (in_array($lang, $valid_langs)){
		} // if (strlen($lang) == 2){
		return False;
	} // public function checkExistingLanguage($lang){
	
	public function getLanguageArtikelSprache(){
		$language_array = array(
			'de' 	=> "Dein Artikel ist in <strong>deutscher Sprache</strong> geschrieben", // de
			'en' 	=> "Your article has been created in <strong>English</strong> language", // en
			'es'	=> "Su artículo está escrito en <strong>español</strong>", // es
			'fr'	=> "Votre article est écrit en <strong>français</strong>", // fr
			'in'	=> "आपका लेख <strong> भारतीय </strong> . में लिखा गया है", //hi
			'it'	=> "Il tuo articolo è scritto in <strong>italiano</strong>", //it
			'jp'	=> "あなたの記事は<strong>日本語</strong>で書かれています", //jp
			'pt'	=> "O seu artigo está escrito em <strong>Português</strong>", // pt,
			'ru'	=> "Ваша статья написана на <strong>русском языке</strong>", 
			'cn'	=> "你的文章是用<strong>简单的中文写的</strong>。",
			'sa'	=> "مقالتك مكتوبة باللغة <strong> العربية </ strong>",
			'tr' 	=> "Makaleniz <strong>Türkçe</strong> yazılmıştır"
		);
		return $language_array;
	} // public function getLanguageArtikelSprache(){
		
	public function getLanguageArray(){ 
		//https://www.w3schools.com/charsets/ref_utf_symbols.asp
		$language_array = array(
		'de' => array(
			'startpage_header_h1'	=> "SEO Optimizer: Ghost Writer - Hausarbeiten schreiben mit SEO Tool und KI",	
			'startpage_header_h2'	=> "SEO Tool: Ghost Writer - Hausarbeiten schreiben mit Ghostwriter Service für Schule, Studium und Beruf (zum Beispiel für Schulaufgaben, Hausarbeiten, Facharbeiten, Diplomarbeiten, Doktorarbeiten, Bachelor- und Masterarbeiten)",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "Erstelle deinen einzigartigen Artikel kostenlos auf auf 'www.artikelschreiber.com': <a href='https://www.artikelschreiber.com/' title='Artikel schreiben für Content Marketing | ArtikelSchreiber.com' target='_self' hreflang='de'>www.artikelschreiber.com</a>",
			'description_create' 	=> "Erstelle deinen einzigartigen Artikel kostenlos auf auf www.artikelschreiber.com",
			'summary' 				=> "Erstelle kostenlose Artikel (www.artikelschreiber.com)",
			'url' 					=> "https://www.artikelschreiber.com/",
			'email_subject'			=> "Schau dir den kostenlosen ArtikelSchreiber.com an",
			'email_body'			=> "Nutze den kostenlosen SEO Text Generator mit Künstlicher Intelligenz, um neue Artikel für SEO, Wordpress/Blog, Produktbeschreibungen, Amazon, Ebay, Textaufträge und Journalismus unter",
			'server' 				=> "Der Server ist überlastet. Probiere es bitte später noch einmal.",
			'werbung'				=> "Werbung",
			'lang'					=> "de",
			'show_questions'		=> "Ihr einzigartiger SEO-Text beantwortet Ihnen folgende Fragen",
			'mainkeyword'			=> "Thema deines Artikels", # Hauptstichwort
			'subkeyword'			=> "Schwerpunkt des Texts", # Nebenstichwort
			'action_createtext'		=> "Text erstellen!", # Text erstellen!
			'request_action_create'	=> "Neuen Artikel erstellen", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "Möchtest du ArtikelSchreiber.com wirklich verlassen?",
			'redirect_info_goto'	=> "Dieser Link führt zu einer externen Website außerhalb von ArtikelSchreiber.com",
			'redirect_goto_external'=> "WEBSITE AUFRUFEN",
			'redirect_goto_service' => "Zurück zu ArtikelSchreiber.com",
			'index_title'			=> "SEO Optimizer: Ghost Writer - Hausarbeiten schreiben mit KI",
			'index_title_short'		=> "Ghost Writer: Hausarbeiten schreiben",
			//'index_title'			=> "Artikel schreiben für Content Marketing | ArtikelSchreiber.com",
			'index_description'		=> "SEO Optimizer: Ghost Writer zum Hausarbeiten schreiben mit Ghostwriter Service und dem kostenlosen SEO Tool ➡️ Jetzt gratis nutzen",
			'title_create'			=> "Dein kostenloser SEO Text Generator | ArtikelSchreiber.com"
		),
		'en' => array(
			'startpage_header_h1'	=> "SEO Tool: Content Writing with Pointed Copywriting through Rewriter Tool powered by AGI",	
			'startpage_header_h2'	=> "SEO Content Writing: SEO Copywriting with AI Text Generator powered by Artificial General Intelligence (AGI)",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "Create your unique article for free on 'www.artikelschreiber.com/en/': <a href='https://www.artikelschreiber.com/en/' title='Article Generator: Write text for Marketing | ArtikelSchreiber.com' target='_self' hreflang='en'>www.artikelschreiber.com/en</a>",
			'description_create' 	=> "Create your unique article for free on www.artikelschreiber.com/en/",
			'summary' 				=> "Create free articles (www.artikelschreiber.com/en/)",
			'url' 					=> "https://www.artikelschreiber.com/en/",
			'email_subject'			=> "Check out the free ArtikelSchreiber.com",
			'email_body'			=> "Use the free SEO Text Generator with artificial intelligence to create new articles for SEO, Wordpress/Blog, product descriptions, Amazon, Ebay, text assignments and journalism under",
			'server' 				=> "The server is overloaded. Please try again later.",
			'werbung'				=> "Advertising",
			'lang'					=> "en",
			'show_questions'		=> "Your unique SEO Text answers the following questions for you",
			'mainkeyword'			=> "Topic of your Article", # Hauptstichwort
			'subkeyword'			=> "Focus of your Text", # Nebenstichwort
			'action_createtext'		=> "Create text!", # Text erstellen!
			'request_action_create'	=> "Create a new article", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "Do you really want to leave ArtikelSchreiber.com?",
			'redirect_info_goto'	=> "This link leads to an external website outside of ArtikelSchreiber.com",
			'redirect_goto_external'=> "ENTER WEBSITE",
			'redirect_goto_service' => "Return to ArtikelSchreiber.com",
			'index_title'			=> "SEO Tool: SEO Optimizer for Content Writing with Strong AI",
			'index_title_short'		=> "SEO Tool: SEO Optimizer",
			//'index_title'			=> "Article Generator: Write text for Marketing | ArtikelSchreiber.com", //changed 2022/11/16
			'index_description'		=> "SEO Tool: SEO Optimizer and Text Generator for Content Writing powered by Artificial General Intelligence (AGI) ✓ for eCommerce, Business, Sales ➡️ Always free",
			'title_create'			=> "Your free SEO text generator | ArtikelSchreiber.com"
		),
		'es' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "Crea tu artículo único gratis en 'www.artikelschreiber.com/es/': <a href='https://www.artikelschreiber.com/es/' title='Escribir un artículo para marketing digital | ArtikelSchreiber.com' target='_self' hreflang='es'>www.artikelschreiber.com/es/</a>",
			'description_create' 	=> "Crea tu artículo único gratis en www.artikelschreiber.com/es/",
			'summary' 				=> "Crear artículos gratuitos (www.artikelschreiber.com/es/)",
			'url' 					=> "https://www.artikelschreiber.com/es/",
			'email_subject'			=> "Consulte el artículo gratuito ArtikelSchreiber.com",
			'email_body'			=> "Use el generador de texto SEO gratuito con inteligencia artificial para crear nuevos artículos para SEO, Wordpress/Blog, descripciones de productos, Amazon, Ebay, asignaciones de texto y periodismo bajo",
			'server' 				=> "El servidor está sobrecargado. Por favor, inténtelo más tarde.",
			'werbung'				=> "Publicidad",
			'lang'					=> "es",
			'show_questions'		=> "Tu Texto SEO único responde las siguientes preguntas por ti",
			'mainkeyword'			=> "Palabras clave principales", # Hauptstichworte
			'subkeyword'			=> "Palabras clave subsidiarias", # Nebenstichworte
			'action_createtext'		=> "¡Crea texto!", # Text erstellen!
			'request_action_create'	=> "Crea un nuevo articulo", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "¿Realmente quieres dejar ArtikelSchreiber.com?",
			'redirect_info_goto'	=> "Este enlace conduce a un sitio web externo fuera de ArtikelSchreiber.com",
			'redirect_goto_external'=> "ENTRAR SITIO WEB",
			'redirect_goto_service' => "Volver a ArtikelSchreiber.com",
			'index_title'			=> "Escribir un artículo para marketing digital |ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "Marketing: escriba contenido de marketing con la herramienta AI ✓ para comercio electrónico, negocios, ventas o ventas adicionales ✓ 180,000 usuarios satisfechos ➡️ Siempre gratis",
			'title_create'			=> "Su generador de textos SEO gratuito | ArtikelSchreiber.com"
		),
		'fr' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "Créez votre article unique gratuitement sur 'www.artikelschreiber.com/fr/': <a href='https://www.artikelschreiber.com/fr/' title='Rédiger un article pour le marketing numérique | ArtikelSchreiber.com' target='_self' hreflang='fr'>www.artikelschreiber.com/fr/</a>",
			'description_create' 	=> "Créez votre article unique gratuitement sur www.artikelschreiber.com/fr/",
			'summary' 				=> "Créez des articles gratuits (www.artikelschreiber.com/fr/)",
			'url' 					=> "https://www.artikelschreiber.com/fr/",
			'email_subject'			=> "Consultez l'article gratuit ArtikelSchreiber.com",
			'email_body'			=> "Utilisez le générateur de texte SEO gratuit avec intelligence artificielle pour créer de nouveaux articles pour SEO, Wordpress/Blog, descriptions de produits, Amazon, Ebay, affectations de texte et journalisme sous",
			'server' 				=> "Le serveur est surchargé. Veuillez réessayer plus tard.",
			'werbung'				=> "Publicité",
			'lang'					=> "fr",
			'show_questions'		=> "Votre texte SEO unique répond pour vous aux questions suivantes",
			'mainkeyword'			=> "Mots-clés principaux", # Hauptstichworte
			'subkeyword'			=> "Mots-clés subsidiaires", # Nebenstichworte
			'action_createtext'		=> "Créez du texte !", # Text erstellen!
			'request_action_create'	=> "Créer un nouvel article", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "Voulez-vous vraiment quitter ArtikelSchreiber.com?",
			'redirect_info_goto'	=> "Ce lien mène à un site Web externe en dehors de ArtikelSchreiber.com",
			'redirect_goto_external'=> "ENTRER SUR LE SITE WEB",
			'redirect_goto_service' => "Retour à ArtikelSchreiber.com",
			'index_title'			=> "Rédiger un article pour le marketing numérique | ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "Marketing : Rédigez un article, un texte gratuit ou un contenu marketing avec l'outil AI SEO ✓ pour le commerce électronique, les affaires, les ventes ou la vente incitative ✓ 180 000 utilisateurs satisfaits ➡️ Toujours gratuit",
			'title_create'			=> "Ton générateur de texte SEO gratuit | ArtikelSchreiber.com"
		),
		'it' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "Crea il tuo articolo unico gratuitamente su 'www.artikelschreiber.com/it/': <a href='https://www.artikelschreiber.com/it/' title='Scrivi un articolo per il marketing digitale | ArtikelSchreiber.com' target='_self' hreflang='it'>www.artikelschreiber.com/it/</a>",
			'description_create' 	=> "Crea il tuo articolo unico gratuitamente su www.artikelschreiber.com/it/",
			'summary' 				=> "Creare articoli gratuiti (www.artikelschreiber.com/it/)",
			'url' 					=> "https://www.artikelschreiber.com/it/",
			'email_subject'			=> "Dai un'occhiata all'articolo gratuito ArtikelSchreiber.com",
			'email_body'			=> "Usa il generatore di testo SEO gratuito con intelligenza artificiale per creare nuovi articoli per SEO, Wordpress/Blog, descrizioni di prodotti, Amazon, Ebay, compiti di testo e giornalismo sotto",
			'server' 				=> "Il server è sovraccarico. Si prega di riprovare più tardi.",
			'werbung'				=> "Pubblicità",
			'lang'					=> "it",
			'show_questions'		=> "Il tuo testo SEO unico risponde alle seguenti domande per te",
			'mainkeyword'			=> "Parole chiave principali", # Hauptstichworte
			'subkeyword'			=> "Parole chiave sussidiarie", # Nebenstichworte
			'action_createtext'		=> "Crea testo!", # Text erstellen!
			'request_action_create'	=> "Crea un nuovo articolo", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "Vuoi davvero lasciare ArtikelSchreiber.com?",
			'redirect_info_goto'	=> "Questo collegamento rimanda a un sito Web esterno al di fuori di ArtikelSchreiber.com",
			'redirect_goto_external'=> "ACCEDI AL SITO",
			'redirect_goto_service' => "Torna a ArtikelSchreiber.com",
			'index_title'			=> "Scrivi un articolo per il marketing digitale | ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "Marketing: Scrivi un articolo, un testo libero o un contenuto di marketing con lo strumento AI SEO ✓ per eCommerce, Business, Sales o Upsell ✓ 180.000 utenti soddisfatti ➡️ Sempre gratis",
			'title_create'			=> "Il tuo generatore di testo SEO gratuito | ArtikelSchreiber.com"
		),
		'ru' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "Создайте свою уникальную статью бесплатно на сайте 'www.artikelschreiber.com/ru/': <a href='https://www.artikelschreiber.com/ru/' title='Написать статью для цифрового маркетинга | ArtikelSchreiber.com' target='_self' hreflang='ru'>www.artikelschreiber.com/ru/</a>",
			'description_create' 	=> "Создайте свою уникальную статью бесплатно на сайте www.artikelschreiber.com/ru/",
			'summary' 				=> "Создание бесплатных статей (www.artikelschreiber.com/ru/)",
			'url' 					=> "https://www.artikelschreiber.com/ru/",
			'email_subject'			=> "Ознакомьтесь с бесплатной статьей ArtikelSchreiber.com",
			'email_body'			=> "Используйте бесплатный SEO Text Generator с искусственным интеллектом для создания новых статей для SEO, Wordpress/Blog, описаний продуктов, Amazon, Ebay, текстовых заданий и журналистики под",
			'server' 				=> "Сервер перегружен. Пожалуйста, повторите попытку позже.",
			'werbung'				=> "Реклама",
			'lang'					=> "ru",
			'show_questions'		=> "Ваш уникальный SEO-текст отвечает на следующие вопросы:",
			'mainkeyword'			=> "Основные ключевые слова", # Hauptstichworte
			'subkeyword'			=> "Вспомогательные ключевые слова", # Nebenstichworte
			'action_createtext'		=> "Создать новую статью", # Text erstellen!
			'request_action_create'	=> "Создать новую статью", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "Вы действительно хотите покинуть ArtikelSchreiber.com?",
			'redirect_info_goto'	=> "Эта ссылка ведет на внешний веб-сайт за пределами ArtikelSchreiber.com.",
			'redirect_goto_external'=> "ВОЙТИ НА САЙТ",
			'redirect_goto_service' => "Вернуться на ArtikelSchreiber.com",
			'index_title'			=> "Написать статью для цифрового маркетинга | ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "Маркетинг: напишите статью, бесплатный текст или маркетинговый контент с помощью инструмента AI SEO ✓ для электронной коммерции, бизнеса, продаж или дополнительных продаж ✓ 180 000 довольных пользователей ➡️ Всегда бесплатно",
			'title_create'			=> "Ваш бесплатный генератор SEO-текстов | ArtikelSchreiber.com"
		),
		'cn' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "在'www.artikelschreiber.com/cn/'上免费创建你的独特文章: <a href='https://www.artikelschreiber.com/cn/' title='SEO工具：为数字营销写一篇文章 | ArtikelSchreiber.com' target='_self' hreflang='cn'>www.artikelschreiber.com/cn/</a>",
			'description_create' 	=> "在www.artikelschreiber.com/cn/上免费创建你的独特文章",
			'summary' 				=> "创建免费文章（www.artikelschreiber.com/cn/）",
			'url' 					=> "https://www.artikelschreiber.com/cn/",
			'email_subject'			=> "查看免费文章 ArtikelSchreiber.com",
			'email_body'			=> "使用具有人工智能的免费 SEO 文本生成器为 SEO、Wordpress/博客、产品描述、亚马逊、Ebay、文本分配和新闻创建新文章",
			'werbung'				=> "广告",
			'server' 				=> "服务器过载。请稍后再试。",
			'lang'					=> "cn",
			'show_questions'		=> "您独特的 SEO 文本为您回答以下问题",
			'mainkeyword'			=> "主要关键词", # Hauptstichworte
			'subkeyword'			=> "子关键词", # Nebenstichworte
			'action_createtext'		=> "创建文本！", # Text erstellen!
			'request_action_create'	=> "创建新文章", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "您真的要离开 ArtikelSchreiber.com 吗？",
			'redirect_info_goto'	=> "此链接指向 ArtikelSchreiber.com 之外的外部网站",
			'redirect_goto_external'=> "进入网站",
			'redirect_goto_service' => "返回 ArtikelSchreiber.com",
			'index_title'			=> "SEO工具：为数字营销写一篇文章 | ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "营销：使用 AI SEO 工具撰写文章、免费文本或营销内容 ✓ 用于电子商务、商业、销售或追加销售 ✓ 180.000 个满意的用户 ➡️ 永远免费",
			'title_create'			=> "您的免费SEO文本生成器 | ArtikelSchreiber.com"
		),
		'pt' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "Crie o seu artigo único gratuitamente em 'www.artikelschreiber.com/pt/': <a href='https://www.artikelschreiber.com/pt/' title='Ferramenta SEO: Escreva um artigo para marketing digital | ArtikelSchreiber.com' target='_self' hreflang='pt'>www.artikelschreiber.com/pt/</a>",
			'description_create' 	=> "Crie o seu artigo único gratuitamente em www.artikelschreiber.com/pt/",
			'summary' 				=> "Criar artigos gratuitos (www.artikelschreiber.com/pt/)",
			'url' 					=> "https://www.artikelschreiber.com/pt/",
			'email_subject'			=> "Confira o artigo gratuito ArtikelSchreiber.com",
			'email_body'			=> "Use o SEO Text Generator gratuito com inteligência artificial para criar novos artigos para SEO, Wordpress/Blog, descrições de produtos, Amazon, Ebay, atribuições de texto e jornalismo em",
			'server' 				=> "O servidor está sobrecarregado. Por favor, tente novamente mais tarde.",
			'werbung'				=> "Publicidade",
			'lang'					=> "pt",
			'show_questions'		=> "Seu texto de SEO exclusivo responde às seguintes perguntas para você",
			'mainkeyword'			=> "Palavras-chave principais", # Hauptstichworte
			'subkeyword'			=> "Palavras-chave subsidiárias", # Nebenstichworte
			'action_createtext'		=> "Crie o texto!", # Text erstellen!
			'request_action_create'	=> "Crie um novo artigo", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "Você realmente quer deixar ArtikelSchreiber.com?",
			'redirect_info_goto'	=> "Este link leva a um site externo fora do ArtikelSchreiber.com",
			'redirect_goto_external'=> "ENTRAR NO SITE",
			'redirect_goto_service' => "Voltar para ArtikelSchreiber.com",
			'index_title'			=> "Ferramenta SEO: Escreva um artigo para marketing digital |ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "Marketing: Escreva um artigo, texto livre ou conteúdo de marketing com a ferramenta AI SEO ✓ para comércio eletrônico, negócios, vendas ou upsell ✓ 180.000 usuários satisfeitos ➡️ Sempre grátis",
			'title_create'			=> "O seu gerador de texto SEO gratuito | ArtikelSchreiber.com"
		),
		'sa' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",				
			'description' 			=> "قم بإنشاء مقالتك الفريدة مجانًا على 'www.artikelschreiber.com/sa/': <a href='https://www.artikelschreiber.com/sa/' title='أداة تحسين محركات البحث SEO: اكتب مقالًا للتسويق الرقمي | ArtikelSchreiber.com' target='_self' hreflang='sa'> www.artikelschreiber.com/sa/</a>",
			'description_create' 	=> "قم بإنشاء مقالتك الفريدة مجانًا على www.artikelschreiber.com/sa/",
			'summary' 				=> "إنشاء مقالات مجانية (www.artikelschreiber.com/sa/)",
			'url' 					=> "https://www.artikelschreiber.com/sa/",
			'email_subject'			=> "تحقق من المقال المجاني ArtikelSchreiber.com",
			'email_body'			=> "استخدم مُنشئ نصوص SEO المجاني مع الذكاء الاصطناعي لإنشاء مقالات جديدة لـ SEO و Wordpress / Blog وأوصاف المنتج و Amazon و Ebay والتعيينات النصية والصحافة تحت",
			'server' 				=> "الخادم مثقل. الرجاء معاودة المحاولة في وقت لاحق.",
			'werbung'				=> "إعلان",
			'lang'					=> "sa",
			'show_questions'		=> "يجيب نص SEO الفريد الخاص بك على الأسئلة التالية من أجلك",
			'mainkeyword'			=> "الكلمات الرئيسية الرئيسية", # Hauptstichworte
			'subkeyword'			=> "الكلمات الرئيسية الفرعية", # Nebenstichworte
			'action_createtext'		=> "إنشاء نص!", # Text erstellen!
			'request_action_create'	=> "قم بإنشاء مقال جديد", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "هل تريد حقًا مغادرة ArtikelSchreiber.com؟",
			'redirect_info_goto'	=> "يؤدي هذا الرابط إلى موقع ويب خارجي خارج ArtikelSchreiber.com",
			'redirect_goto_external'=> "أدخل الموقع",
			'redirect_goto_service' => "العودة إلى ArtikelSchreiber.com",
			'index_title'			=> "أداة تحسين محركات البحث SEO: اكتب مقالًا للتسويق الرقمي |ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "التسويق: اكتب مقالًا أو نصًا مجانيًا أو محتوى تسويقيًا باستخدام أداة AI SEO للتجارة الإلكترونية أو الأعمال أو المبيعات أو Upsell ✓ 180.000 مستخدم راضٍ ➡️ مجاني دائمًا",
			'title_create'			=> "مولد النص SEO المجاني الخاص بك | ArticleSchreiber.com"
		),
		'jp' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "www.artikelschreiber.com/jp/': <a href='https://www.artikelschreiber.com/jp/' title='SEOツール：デジタルマーケティングの記事を書く | ArtikelSchreiber.com'  target='_self' hreflang='jp'>www.artikelschreiber.com/jp/</a> に無料で独自の記事を作成することができます。",
			'description_create' 	=> "www.artikelschreiber.com/jp/ 無料であなただけの記事を作成",
			'summary' 				=> "無料記事作成（www.artikelschreiber.com/jp/）",
			'url' 					=> "https://www.artikelschreiber.com/jp/",
			'email_subject'			=> "無料の記事ArtikelSchreiber.comをチェックしてください",
			'email_body'			=> "人工知能を備えた無料のSEOテキストジェネレーターを使用して、SEO、Wordpress / Blog、製品の説明、Amazon、Ebay、テキストの割り当て、ジャーナリズムに関する新しい記事を作成します。",
			'server' 				=> "サーバーに負荷がかかっている。後でもう一度お試しください。",
			'werbung'				=> "広告宣伝",
			'lang'					=> "jp",
			'show_questions'		=> "あなたのユニークなSEOテキストはあなたのために次の質問に答えます",
			'mainkeyword'			=> "主なキーワード", # Hauptstichworte
			'subkeyword'			=> "補助キーワード", # Nebenstichworte
			'action_createtext'		=> "テキストを作成してください！", # Text erstellen!
			'request_action_create'	=> "新しい記事を作成する", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "本当にArtikelSchreiber.comを離れたいですか？",
			'redirect_info_goto'	=> "このリンクは、ArtikelSchreiber.comの外部の外部Webサイトにつながります",
			'redirect_goto_external'=> "ウェブサイトに入る",
			'redirect_goto_service' => "ArtikelSchreiber.comに戻る",
			'index_title'			=> "SEOツール：デジタルマーケティングの記事を書く | ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "マーケティング：AI SEOツールを使用して記事、フリーテキスト、またはマーケティングコンテンツを作成する✓eコマース、ビジネス、セールス、またはアップセル向け✓180.000満足しているユーザー➡️常に無料",
			'title_create'			=> "無料SEOテキストジェネレーター｜ArtikelSchreiber.com"
		),
		'tr' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "üzerinde ücretsiz olarak benzersiz öğenizi oluşturun 'www.artikelschreiber.com/tr/': <a href='https://www.artikelschreiber.com/tr/' title='SEO Aracı: Dijital pazarlama için bir makale yazın | ArtikelSchreiber.com' target='_self' hreflang='tr'>www.artikelschreiber.com/tr/</a>",
			'description_create' 	=> "Benzersiz öğenizi ücretsiz oluşturun auf www.artikelschreiber.com/tr/",
			'summary' 				=> "Ücretsiz makaleler oluşturun (www.artikelschreiber.com/tr/)",
			'url' 					=> "https://www.artikelschreiber.com/tr/",
			'email_subject'			=> "Ücretsiz ArtikelSchreiber.com makalesine göz atın",
			'email_body'			=> "SEO, Wordpress/Blog, ürün açıklamaları, Amazon, Ebay, metin atamaları ve gazetecilik için yeni makaleler oluşturmak için Yapay Zeka ile ücretsiz SEO Metin Üreticisini kullanın.",
			'server' 				=> "Sunucu aşırı yüklenmiş. Lütfen daha sonra tekrar deneyiniz.",
			'werbung'				=> "reklam",
			'lang'					=> "tr",
			'show_questions'		=> "Eşsiz SEO Metniniz aşağıdaki soruları sizin için yanıtlar",
			'mainkeyword'			=> "ana anahtar kelimeler", # Hauptstichwort
			'subkeyword'			=> "ikincil anahtar kelimeler", # Nebenstichwort
			'action_createtext'		=> "metin oluştur!", # Text erstellen!
			'request_action_create'	=> "Yeni makale oluştur", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "Gerçekten ArtikelSchreiber.com'dan ayrılmak istiyor musunuz?",
			'redirect_info_goto'	=> "Bu bağlantı, ArtikelSchreiber.com dışındaki harici bir web sitesine yönlendirir.",
			'redirect_goto_external'=> "WEB SİTESİNE GİRİN",
			'redirect_goto_service' => "ArtikelSchreiber.com'a dön",
			'index_title'			=> "SEO Aracı: Dijital pazarlama için bir makale yazın |ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "Pazarlama: AI SEO aracıyla bir makale, ücretsiz metin veya pazarlama içeriği yazın ✓ e-Ticaret, İşletme, Satış veya Upsell ✓ 180.000 memnun kullanıcı ➡️ Her zaman ücretsiz",
			'title_create'			=> "Ücretsiz SEO Metin Üreticiniz | ArtikelSchreiber.com"
		),
		'in' => array(
			'startpage_header_h1'	=> "",	
			'startpage_header_h2'	=> "",
			'startpage_header_h3'	=> "",	
			'startpage_header_h4'	=> "",	
			'startpage_header_h5'	=> "",				
			'startpage_header_h6'	=> "",	
			'description' 			=> "'www.artikelschreiber.com/in/' पर अपना अनूठा लेख निःशुल्क बनाएं: <a href='https://www.artikelschreiber.com/in/' title='SEO टूल: डिजिटल मार्केटिंग के लिए एक आर्टिकल लिखें | ArtikelSchreiber.com' target='_self' hreflang='in'>www.artikelschreiber.com/in/</a>",
			'description_create' 	=> "www.artikelschreiber.com/in/ पर अपना अनूठा लेख निःशुल्क बनाएं",
			'summary' 				=> "मुफ़्त लेख बनाएँ (www.artikelschreiber.com/in/)",
			'url' 					=> "https://www.artikelschreiber.com/in/",
			'email_subject'			=> "मुफ़्त लेख देखें ArtikelSchreiber.com",
			'email_body'			=> "के अंतर्गत SEO, Wordpress/Blog, उत्पाद विवरण, Amazon, Ebay, टेक्स्ट असाइनमेंट और पत्रकारिता के लिए नए लेख बनाने के लिए आर्टिफिशियल इंटेलिजेंस के साथ निःशुल्क SEO टेक्स्ट जेनरेटर का उपयोग करें।",
			'server' 				=> "सर्वर ओवरलोड है। बाद में पुन: प्रयास करें।",
			'werbung'				=> "विज्ञापन",
			'lang'					=> "in",
			'show_questions'		=> "आपका अनूठा SEO टेक्स्ट आपके लिए निम्नलिखित प्रश्नों का उत्तर देता है",
			'mainkeyword'			=> "मुख्य खोजशब्द", # Hauptstichworte
			'subkeyword'			=> "सहायक कीवर्ड", # Nebenstichworte
			'action_createtext'		=> "टेक्स्ट बनाएं!", # Text erstellen!
			'request_action_create'	=> "एक नया लेख बनाएं", # Neuen Artikel erstellen
			'redirect_leave_ascom'	=> "क्या आप वाकई ArtikelSchreiber.com छोड़ना चाहते हैं? ",
			'redirect_info_goto'	=> "यह लिंक ArtikelSchreiber.com के बाहर एक बाहरी वेबसाइट की ओर ले जाता है",
			'redirect_goto_external'=> "वेबसाइट दर्ज करें",
			'redirect_goto_service' => "ArtikelSchreiber.com पर लौटें",
			'index_title'			=> "SEO टूल: डिजिटल मार्केटिंग के लिए एक आर्टिकल लिखें | ArtikelSchreiber.com",
			'index_title_short'		=> "",
			'index_description'		=> "मार्केटिंग: ईकामर्स, बिजनेस, सेल्स या अपसेल के लिए AI SEO टूल के साथ एक आर्टिकल, फ्री टेक्स्ट या मार्केटिंग कंटेंट लिखें 180,000 संतुष्ट यूजर्स ️ हमेशा फ्री",
			'title_create'			=> "आपका मुफ़्त SEO टेक्स्ट जेनरेटर ｜ArtikelSchreiber.com"
		)
	);
		return $language_array;
	} // public function getLanguageArray(){
} // class
?>