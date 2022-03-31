//----------------------------------------------------/
//
//      POLO - HTML5 Template
//      Author: INSPIRO - Ardian Berisha
//      Version: v5.9.9
//      Update: April 10, 2020
//
//----------------------------------------------------/
//INSPIRO Global var
var INSPIRO = {},
  $ = jQuery.noConflict();
(function ($) {
  "use strict"
  // Predefined Global Variables
  var $window = $(window),
    $theme_color = "#2250fc",
    //Main
    $body = $("body"),
    $bodyInner = $(".body-inner"),
    $section = $("section"),
    //Header
    $topbar = $("#topbar"),
    $header = $("#header"),
    $headerCurrentClasses = $header.attr("class"),
    //Logo
    headerLogo = $("#logo"),
    //Menu
    $mainMenu = $("#mainMenu"),    
    $mainMenuTriggerBtn = $("#mainMenu-trigger a, #mainMenu-trigger button"),
    //Slider
    $slider = $("#slider"),
    $inspiroSlider = $(".inspiro-slider"),
    $carousel = $(".carousel"),
    /*Grid Layout*/
    $gridLayout = $(".grid-layout"),
    $gridFilter = $(".grid-filter, .page-grid-filter"),
    windowWidth = $window.width();

  //Check if header exist
  if ($header.length > 0) {
    var $headerOffsetTop = $header.offset().top
  }
  var Events = {
    browser: {
      isMobile: function () {
        if (navigator.userAgent.match(/(iPhone|iPod|iPad|Android|BlackBerry)/)) {
          return true
        } else {
          return false
        }
      }
    }
  }
  //Settings
  var Settings = {
    isMobile: Events.browser.isMobile,
    submenuLight: $header.hasClass("submenu-light") == true ? true : false,
    headerHasDarkClass: $header.hasClass("dark") == true ? true : false,
    headerDarkClassRemoved: false,
    sliderDarkClass: false,
    menuIsOpen: false,
    menuOverlayOpened: false,
  }
  //Window breakpoints
  $(window).breakpoints({
    triggerOnInit: true,
    breakpoints: [{
        name: "xs",
        width: 0
      },
      {
        name: "sm",
        width: 576
      },
      {
        name: "md",
        width: 768
      },
      {
        name: "lg",
        width: 1025
      },
      {
        name: "xl",
        width: 1200
      }
    ]
  })
  var currentBreakpoint = $(window).breakpoints("getBreakpoint")
  $body.addClass("breakpoint-" + currentBreakpoint)
  $(window).bind("breakpoint-change", function (breakpoint) {
    $body.removeClass("breakpoint-" + breakpoint.from)
    $body.addClass("breakpoint-" + breakpoint.to)
  });


  $(window).bind("breakpoint-change", function(event) {
    $(window).breakpoints("greaterEqualTo", "lg", function () {
      $body.addClass("b--desktop");
      $body.removeClass("b--responsive");
    });
    $(window).breakpoints("lessThan", "lg", function () {
      $body.removeClass("b--desktop");
      $body.addClass("b--responsive");
    });
  });


  
  INSPIRO.core = {
    functions: function () {
      INSPIRO.core.scrollTop()
      INSPIRO.core.rtlStatus()
      INSPIRO.core.equalize()
      INSPIRO.core.customHeight()
      INSPIRO.core.darkTheme()
    },
    scrollTop: function () {
      var $scrollTop = $("#scrollTop")
      if ($scrollTop.length > 0) {
        var scrollOffset = $body.attr("data-offset") || 400
        if ($window.scrollTop() > scrollOffset) {
          if ($body.hasClass("frame")) {
            $scrollTop.css({
              "bottom": "46px",
              "opacity": 1,
              "z-index": 199
            })
          } else {
            $scrollTop.css({
              "bottom": "26px",
              "opacity": 1,
              "z-index": 199
            })
          }
        } else {
          $scrollTop.css({
            bottom: "16px",
            opacity: 0
          })
        }
        $scrollTop.off("click").on("click", function () {
          $("body,html")
            .stop(true)
            .animate({
                scrollTop: 0
              },
              1000,
              "easeInOutExpo"
            )
          return false
        })
      }
    },
    rtlStatus: function () {
      var $rtlStatusCheck = $("html").attr("dir")
      if ($rtlStatusCheck == "rtl") {
        return true
      }
      return false
    },
    equalize: function () {
      var $equalize = $(".equalize")
      if ($equalize.length > 0) {
        $equalize.each(function () {
          var elem = $(this),
            selectorItem = elem.find(elem.attr("data-equalize-item")) || "> div",
            maxHeight = 0
          selectorItem.each(function () {
            if ($(this).outerHeight(true) > maxHeight) {
              maxHeight = $(this).outerHeight(true)
            }
          })
          selectorItem.height(maxHeight)
        })
      }
    },
    customHeight: function (setHeight) {
      var $customHeight = $(".custom-height")
      if ($customHeight.length > 0) {
        $customHeight.each(function () {
          var elem = $(this),
            elemHeight = elem.attr("data-height") || 400,
            elemHeightLg = elem.attr("data-height-lg") || elemHeight,
            elemHeightMd = elem.attr("data-height-md") || elemHeightLg,
            elemHeightSm = elem.attr("data-height-sm") || elemHeightMd,
            elemHeightXs = elem.attr("data-height-xs") || elemHeightSm

          function customHeightBreakpoint(setHeight) {
            if (setHeight) {
              elem = setHeight
            }
            switch ($(window).breakpoints("getBreakpoint")) {
              case "xs":
                elem.height(elemHeightXs)
                break
              case "sm":
                elem.height(elemHeightSm)
                break
              case "md":
                elem.height(elemHeightMd)
                break
              case "lg":
                elem.height(elemHeightLg)
                break
              case "xl":
                elem.height(elemHeight)
                break
            }
          }
          customHeightBreakpoint(setHeight)
          $(window).resize(function () {
            setTimeout(function () {
              customHeightBreakpoint(setHeight)
            }, 100)
          })
        })
      }
    },
    darkTheme: function () {
      var $darkElement = $("[data-dark-src]"),
        $lightBtnTrigger = $("#light-mode"),
        $darkBtnTrigger = $("#dark-mode"),
        darkColorScheme = "darkColorScheme",
        defaultDark = $body.hasClass("dark");

      if (typeof Cookies.get(darkColorScheme) !== "undefined") {
       // $body.addClass("dark");
      }


      $darkBtnTrigger.on("click", function (e) {
        darkElemSrc();
        $body.addClass("dark");
        INSPIRO.elements.shapeDivider();
        Cookies.set(darkColorScheme, true, {
          expires: Number(365)
        })
      })

      $lightBtnTrigger.on("click", function (e) {
        lightElemSrc();
        $body.removeClass("dark");
        INSPIRO.elements.shapeDivider();
        Cookies.remove(darkColorScheme);
      })

      if ($body.hasClass("dark")) {
        darkElemSrc();
      }

      function darkElemSrc() {
        $darkElement.each(function () {
          var elem = $(this),
            elemOriginalSrc = elem.attr("src"),
            elemDarkSrc = elem.attr("data-dark-src");

          if (elemDarkSrc) {
            elem.attr("data-original-src", elemOriginalSrc);
            elem.attr("src", elemDarkSrc);
          }
        })
      }

      function lightElemSrc() {
        $darkElement.each(function () {
          var elem = $(this),
            elemLightSrc = elem.attr("data-original-src");

          if (elemLightSrc) {
            elem.attr("src", elemLightSrc);
          }
        })
      }
    }
  }
  INSPIRO.header = {
    functions: function () {
      INSPIRO.header.logoStatus();
      INSPIRO.header.stickyHeader();
      INSPIRO.header.topBar();
      INSPIRO.header.search();
      INSPIRO.header.mainMenu();
      INSPIRO.header.mainMenuOverlay();
      INSPIRO.header.pageMenu();
      INSPIRO.header.sidebarOverlay();
      INSPIRO.header.dotsMenu();
      INSPIRO.header.onepageMenu();
    },
    logoStatus: function (status) {
      var headerLogoDefault = headerLogo.find($(".logo-default")),
        headerLogoDark = headerLogo.find($(".logo-dark")),
        headerLogoFixed = headerLogo.find(".logo-fixed"),
        headerLogoResponsive = headerLogo.find(".logo-responsive");

      if ($header.hasClass("header-sticky") && headerLogoFixed.length > 0) {
        headerLogoDefault.css("display", "none");
        headerLogoDark.css("display", "none");
        headerLogoResponsive.css("display", "none");
        headerLogoFixed.css("display", "block");
      } else {
        headerLogoDefault.removeAttr("style");
        headerLogoDark.removeAttr("style");
        headerLogoResponsive.removeAttr("style");
        headerLogoFixed.removeAttr("style");
      }
      $(window).breakpoints("lessThan", "lg", function () {
        if (headerLogoResponsive.length > 0) {
          headerLogoDefault.css("display", "none");
          headerLogoDark.css("display", "none");
          headerLogoFixed.css("display", "none");
          headerLogoResponsive.css("display", "block");
        }
      })
    },
    stickyHeader: function () {
      var shrinkHeader = $header.attr("data-shrink") || 0,
        shrinkHeaderActive = $header.attr("data-sticky-active") || 200,
        scrollOnTop = $window.scrollTop();
      if ($header.hasClass("header-modern")) {
        shrinkHeader = 300;
      }

      $(window).breakpoints("greaterEqualTo", "lg", function () {
        if (!$header.is(".header-disable-fixed")) {
          if (scrollOnTop > $headerOffsetTop + shrinkHeader) {
            $header.addClass("header-sticky");
            if (scrollOnTop > $headerOffsetTop + shrinkHeaderActive) {
              $header.addClass("sticky-active");
              if (Settings.submenuLight && Settings.headerHasDarkClass) {
                $header.removeClass("dark");
                Settings.headerDarkClassRemoved = true;
              }
              INSPIRO.header.logoStatus();
            }
          } else {
            $header.removeClass().addClass($headerCurrentClasses);
            if (Settings.sliderDarkClass && Settings.headerHasDarkClass) {
              $header.removeClass("dark");
              Settings.headerDarkClassRemoved = true;
            }
            INSPIRO.header.logoStatus();
          }
        }
      });
      $(window).breakpoints("lessThan", "lg", function () {
        if ($header.attr("data-responsive-fixed") == "true") {
          if (scrollOnTop > $headerOffsetTop + shrinkHeader) {
            $header.addClass("header-sticky");
            if (scrollOnTop > $headerOffsetTop + shrinkHeaderActive) {
              $header.addClass("sticky-active");
              if (Settings.submenuLight) {
                $header.removeClass("dark");
                Settings.headerDarkClassRemoved = true;
              }
              INSPIRO.header.logoStatus();
            }
          } else {
            $header.removeClass().addClass($headerCurrentClasses);
            if (Settings.headerDarkClassRemoved == true && $body.hasClass("mainMenu-open")) {
              $header.removeClass("dark");
            }
            INSPIRO.header.logoStatus();
          }
        }
      })
    },
    //chkd
    topBar: function () {
      if ($topbar.length > 0) {
        $("#topbar .topbar-dropdown .topbar-form").each(function (index, element) {
          if ($window.width() - ($(element).width() + $(element).offset().left) < 0) {
            $(element).addClass("dropdown-invert");
          }
        })
      }
    },
    search: function () {
      var $search = $("#search");
      if ($search.length > 0) {
        var searchBtn = $("#btn-search"),
          searchBtnClose = $("#btn-search-close"),
          searchInput = $search.find(".form-control");

        function openSearch() {
          $body.addClass("search-open");
          searchInput.focus();
        }

        function closeSearch() {
          $body.removeClass("search-open");
          searchInput.value = "";
        }
        searchBtn.on("click", function () {
          openSearch();
          return false;
        })
        searchBtnClose.on("click", function () {
          closeSearch();
          return false;
        })
        document.addEventListener("keyup", function (ev) {
          if (ev.keyCode == 27) {
            closeSearch();
          }
        })
      }
    },
    mainMenu: function () {
      if ($mainMenu.length > 0) {
        $mainMenu.find(".dropdown, .dropdown-submenu").prepend('<span class="dropdown-arrow"></span>');

        var $menuItemLinks = $('#mainMenu nav > ul > li.dropdown > a[href="#"], #mainMenu nav > ul > li.dropdown > .dropdown-arrow, .dropdown-submenu > a[href="#"], .dropdown-submenu > .dropdown-arrow, .dropdown-submenu > span, .page-menu nav > ul > li.dropdown > a'),
          $triggerButton = $("#mainMenu-trigger a, #mainMenu-trigger button"),
          processing = false,
          triggerEvent;

        $triggerButton.on("click", function (e) {
          var elem = $(this);
          e.preventDefault();
          $(window).breakpoints("lessThan", "lg", function () {
            var openMenu = function () {
              if (!processing) {
                processing = true;
                Settings.menuIsOpen = true;
                if (Settings.submenuLight && Settings.headerHasDarkClass) {
                  $header.removeClass("dark");
                  Settings.headerDarkClassRemoved = true;
                }else {
                  if (Settings.headerHasDarkClass && Settings.headerDarkClassRemoved) {
                    $header.addClass("dark");
                  }
                }
                elem.addClass("toggle-active");
                $body.addClass("mainMenu-open");
                INSPIRO.header.logoStatus();
                $mainMenu.animate({
                  "min-height": $window.height()
                }, {
                  duration: 500,
                  easing: "easeInOutQuart",
                  start: function () {
                    setTimeout(function () {
                      $mainMenu.addClass("menu-animate");
                    }, 300);
                  },
                  complete: function () {
                    processing = false;
                  }
                })
              }
            }
            var closeMenu = function () {
              if (!processing) {
                processing = true;
                Settings.menuIsOpen = false;
                INSPIRO.header.logoStatus();
                $mainMenu.animate({
                  "min-height": 0
                }, {
                  start: function () {
                    $mainMenu.removeClass("menu-animate");
                  },
                  done: function () {
                    $body.removeClass("mainMenu-open");
                    elem.removeClass("toggle-active");
                    if (Settings.submenuLight && Settings.headerHasDarkClass && Settings.headerDarkClassRemoved && !$header.hasClass("header-sticky")) {
                      $header.addClass("dark");
                    }
                    if (Settings.sliderDarkClass && Settings.headerHasDarkClass && Settings.headerDarkClassRemoved) {
                      $header.removeClass("dark");
                      Settings.headerDarkClassRemoved = true;
                    }
                  },
                  duration: 500,
                  easing: "easeInOutQuart",
                  complete: function () {
                    processing = false;
                  }
                })
              }
            }
            if (!Settings.menuIsOpen) {
              triggerEvent = openMenu();
            } else {
              triggerEvent = closeMenu();
            }
          })
        });

        $menuItemLinks.on("click", function(e) {
          $(this).parent("li").siblings().removeClass("hover-active");
          if($body.hasClass("b--responsive") || $mainMenu.hasClass("menu-onclick") ) {
              $(this).parent("li").toggleClass("hover-active");
          }
          e.stopPropagation();
          e.preventDefault();
        });

        $body.on("click", function(e) {
          $mainMenu.find(".hover-active").removeClass("hover-active");
        });

        $(window).on('resize', function(){
          if($body.hasClass("mainMenu-open")){
            if (Settings.menuIsOpen) {
              $mainMenuTriggerBtn.trigger("click");
              $mainMenu.find(".hover-active").removeClass("hover-active");
            }
          }
      }); 


        /*invert menu fix*/
        $(window).breakpoints("greaterEqualTo", "lg", function () {
          var $menuLastItem = $("nav > ul > li:last-child"),
            $menuLastItemUl = $("nav > ul > li:last-child > ul"),
            $menuLastInvert = $menuLastItemUl.width() - $menuLastItem.width(),
            $menuItems = $("nav > ul > li").find(".dropdown-menu");

          $menuItems.css("display", "block");

          $(".dropdown:not(.mega-menu-item) ul ul").each(function (index, element) {
            if ($window.width() - ($(element).width() + $(element).offset().left) < 0) {
              $(element).addClass("menu-invert");
            }
          })

          if($menuLastItemUl.length > 0) {
          if ($window.width() - ($menuLastItemUl.width() + $menuLastItem.offset().left) < 0 ) {
            $menuLastItemUl.addClass("menu-last");
          }
        }
          $menuItems.css("display", "");
        })
      }

    },
    mainMenuOverlay: function () {},
    pageMenu: function () {

      var $pageMenu = $(".page-menu");

      if ($pageMenu.length > 0) {
        $(window).breakpoints("greaterEqualTo", "lg", function () {
          var shrinkPageMenu = $pageMenu.attr("data-shrink") || $pageMenu.offset().top + 200;

          if ($pageMenu.attr('data-sticky') == "true") {
            $window.scroll(function () {
              if ($window.scrollTop() > shrinkPageMenu) {
                $pageMenu.addClass("sticky-active");
                $header.addClass("pageMenu-sticky");
              } else {
                $pageMenu.removeClass("sticky-active");
                $header.removeClass("pageMenu-sticky");
              }
            });

          }
        });

        $pageMenu.each(function () {
          $(this).find("#pageMenu-trigger").on("click", function () {
            $pageMenu.toggleClass("page-menu-active");
            $pageMenu.toggleClass("items-visible");
          })
        });


      }
    },
    sidebarOverlay: function () {
      var sidebarOverlay = $("#side-panel");
      if (sidebarOverlay.length > 0) {
        sidebarOverlay.css("opacity", 1);
        $("#close-panel").on("click", function () {
          $body.removeClass("side-panel-active");
          $("#side-panel-trigger").removeClass("toggle-active");
        })
      }

      var $sidepanel = $("#sidepanel"),
        $sidepanelTrigger = $(".panel-trigger"),
        sidepanelProcessing = false,
        sidepanelEvent;

      $sidepanelTrigger.on("click", function (e) {
        e.preventDefault();
        var panelOpen = function () {
          if (!sidepanelProcessing) {
            sidepanelProcessing = true;
            Settings.panelIsOpen = true;
            $sidepanel.addClass("panel-open");
            sidepanelProcessing = false;
          }
        }
        var panelClose = function () {
          if (!sidepanelProcessing) {
            sidepanelProcessing = true;
            Settings.panelIsOpen = false;
            $sidepanel.removeClass("panel-open");
            sidepanelProcessing = false;
          }
        }
        if (!Settings.panelIsOpen) {
          sidepanelEvent = panelOpen();
        } else {
          sidepanelEvent = panelClose();
        }
      })
    },
    dotsMenu: function () {
      var $dotsMenu = $("#dotsMenu"),
        $dotsMenuItems = $dotsMenu.find("ul > li > a");
      if ($dotsMenu.length > 0) {
        $dotsMenuItems.on("click", function () {
          $dotsMenuItems.parent("li").removeClass("current");
          $(this).parent("li").addClass("current");
          return false;
        })
        $dotsMenuItems.parents("li").removeClass("current");
        $dotsMenu.find('a[href="#' + INSPIRO.header.currentSection() + '"]').parent("li").addClass("current");
      }
    },
    onepageMenu: function () {
      if ($mainMenu.hasClass("menu-one-page")) {
        var $currentMenuItem = "current";

        $(window).on("scroll", function () {
          var $currentSection = INSPIRO.header.currentSection();
          $mainMenu.find("nav > ul > li > a").parents("li").removeClass($currentMenuItem);
          $mainMenu.find('nav > ul > li > a[href="#' + $currentSection + '"]').parent("li").addClass($currentMenuItem);
        })
      }
    },
    currentSection: function () {
      var elemCurrent = "body"
      $section.each(function () {
        var elem = $(this),
          elemeId = elem.attr("id");
        if (elem.offset().top - $window.height() / 3 < $window.scrollTop() && elem.offset().top + elem.height() - $window.height() / 3 > $window.scrollTop()) {
          elemCurrent = elemeId;
        }
      })
      return elemCurrent;
    }
  }
  INSPIRO.slider = {
    functions: function () {
      INSPIRO.slider.inspiroSlider();
      INSPIRO.slider.carousel();
      INSPIRO.slider.carouselAjax();
    },
    inspiroSlider: function () {
      if ($inspiroSlider.length > 0) {
        //Check if flickity plugin is loaded
        if (typeof $.fn.flickity === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery flickity slider plugin is missing in plugins.js file.", "danger");
          return true;
        }
        var defaultAnimation = "fadeInUp";

        function animate_captions($elem) {
          var $captions = $elem;
          $captions.each(function () {
            var $captionElem = $(this),
              animationDuration = "600ms";
            if ($(this).attr("data-animate-duration")) {
              animationDuration = $(this).attr("data-animate-duration") + "ms";
            }
            $captionElem.css({
              opacity: 0
            })
            $(this).css("animation-duration", animationDuration);
          })
          $captions.each(function (index) {
            var $captionElem = $(this),
              captionDelay = $captionElem.attr("data-caption-delay") || index * 350 + 1000,
              captionAnimation = $captionElem.attr("data-caption-animate") || defaultAnimation;
            var t = setTimeout(function () {
              $captionElem.css({
                opacity: 1
              })
              $captionElem.addClass(captionAnimation)
            }, captionDelay);
          })
        }

        function hide_captions($elem) {
          var $captions = $elem;
          $captions.each(function (caption) {
            var caption = $(this),
              captionAnimation = caption.attr("data-caption-animate") || defaultAnimation;
            caption.removeClass(captionAnimation);
            caption.removeAttr("style");
          })
        }

        function start_kenburn(elem) {
          var currentSlide = elem.find(".slide.is-selected"),
            currentSlideKenburns = currentSlide.hasClass("kenburns");
          if (currentSlideKenburns) {
            setTimeout(function () {
              currentSlide.find(".kenburns-bg").addClass("kenburns-bg-animate");
            }, 500);
          }
        }

        function stop_kenburn(elem) {
          var notCurrentSlide = elem.find(".slide:not(.is-selected)");
          notCurrentSlide.find(".kenburns-bg").removeClass("kenburns-bg-animate");
        }

        function slide_dark(elem) {
          var $sliderClassSlide = elem.find(".slide.is-selected");
          if ($sliderClassSlide.hasClass("slide-dark") && Settings.headerHasDarkClass) {
            $header.removeClass("dark");
            Settings.sliderDarkClass = true;
            Settings.headerDarkClassRemoved = true;
          } else {
            Settings.sliderDarkClass = false;
            if (Settings.headerDarkClassRemoved && Settings.headerHasDarkClass && !$body.hasClass("mainMenu-open") && !$header.hasClass("sticky-active")) {
              $header.addClass("dark");
            }
          }
        }

        function sliderHeight(elem, state) {
          var elem,
            headerHeight = $header.outerHeight(),
            topbarHeight = $topbar.outerHeight() || 0,
            windowHeight = $window.height(),
            sliderCurrentHeight = elem.height(),
            screenHeightExtra = headerHeight + topbarHeight,
            $sliderClassSlide = elem.find(".slide"),
            sliderFullscreen = elem.hasClass("slider-fullscreen"),
            screenRatio = elem.hasClass("slider-halfscreen") ? 1 : 1.2,
            transparentHeader = $header.attr("data-transparent"),
            customHeight = elem.attr("data-height"),
            responsiveHeightXs = elem.attr("data-height-xs"),
            containerFullscreen = elem.find(".container").first().outerHeight(),
            contentCrop;
            
          if (containerFullscreen >= windowHeight) {
            contentCrop = true;
            var sliderMinHeight = containerFullscreen;
            elem.css("min-height", sliderMinHeight + 100);
            $sliderClassSlide.css("min-height", sliderMinHeight + 100);
            elem.find(".flickity-viewport").css("min-height", sliderMinHeight + 100);
          }

          sliderElementsHeight("null");

          function sliderElementsHeight(height) {
            if (height == "null") {
              elem.css("height", "");
              $sliderClassSlide.css("height", "");
              elem.find(".flickity-viewport").css("height", "");
            } else {
              elem.css("height", height);
              $sliderClassSlide.css("height", height);
              elem.find(".flickity-viewport").css("height", height);
            }
          }
          if (customHeight) {
            $(window).breakpoints("greaterEqualTo", "lg", function () {
              sliderElementsHeight(customHeight + "px");
            });
          }
          if (responsiveHeightXs) {
            $(window).breakpoints("lessThan", "md", function () {
              sliderElementsHeight(responsiveHeightXs + "px");
            });
          }
        }
        $inspiroSlider.each(function () {
          var elem = $(this);
          //Plugin Options
          elem.options = {
            cellSelector: elem.attr("data-item") || ".slide",
            prevNextButtons: elem.data("arrows") == false ? false : true,
            pageDots: elem.data("dots") == false ? false : true,
            fade: elem.data("fade") == true ? true : false,
            draggable: elem.data("drag") == true ? true : false,
            freeScroll: elem.data("free-scroll") == true ? true : false,
            wrapAround: elem.data("loop") == false ? false : true,
            groupCells: elem.data("group-cells") == true ? true : false,
            autoPlay: elem.attr("data-autoplay") || 7000,
            pauseAutoPlayOnHover: elem.data("hoverpause") == true ? true : false,
            adaptiveHeight: elem.data("adaptive-height") == false ? false : false,
            asNavFor: elem.attr("data-navigation") || false,
            selectedAttraction: elem.attr("data-attraction") || 0.07,
            friction: elem.attr("data-friction") || 0.9,
            initialIndex: elem.attr("data-initial-index") || 0,
            accessibility: elem.data("accessibility") == true ? true : false,
            setGallerySize: elem.data("gallery-size") == false ? false : false,
            resize: elem.data("resize") == false ? false : false,
            cellAlign: elem.attr("data-align") || "left",
            playWholeVideo: elem.attr("data-play-whole-video") == false ? false : true
          }
          //Kenburns effect
          elem.find(".slide").each(function () {
            if ($(this).hasClass("kenburns")) {
              var elemChild = $(this),
                elemChildImage = elemChild.css("background-image").replace(/.*\s?url\([\'\"]?/, "").replace(/[\'\"]?\).*/, "")

              if (elemChild.attr("data-bg-image")) {
                elemChildImage = elemChild.attr("data-bg-image");
              }
              elemChild.prepend('<div class="kenburns-bg" style="background-image:url(' + elemChildImage + ')"></div>');
            }
          })
          elem.find(".slide video").each(function () {
            this.pause();
          })
          $(window).breakpoints("lessThan", "lg", function () {
            elem.options.draggable = true;
          });

          if (elem.find(".slide").length <= 1) {
            elem.options.prevNextButtons = false;
            elem.options.pageDots = false;
            elem.options.autoPlay = false;
            elem.options.draggable = false;
          }

          if (!$.isNumeric(elem.options.autoPlay) && elem.options.autoPlay != false) {
            elem.options.autoPlay = Number(7000);
          }

          if (INSPIRO.core.rtlStatus() == true) {
            elem.options.resize = true;

          }

          sliderHeight(elem);
          
          var inspiroSliderData = elem.flickity({
            cellSelector: elem.options.cellSelector,
            prevNextButtons: elem.options.prevNextButtons,
            pageDots: elem.options.pageDots,
            fade: elem.options.fade,
            draggable: elem.options.draggable,
            freeScroll: elem.options.freeScroll,
            wrapAround: elem.options.wrapAround,
            groupCells: elem.options.groupCells,
            autoPlay: Number(elem.options.autoPlay),
            pauseAutoPlayOnHover: elem.options.pauseAutoPlayOnHover,
            adaptiveHeight: elem.options.adaptiveHeight,
            asNavFor: elem.options.asNavFor,
            selectedAttraction: Number(elem.options.selectedAttraction),
            friction: elem.options.friction,
            initialIndex: elem.options.initialIndex,
            accessibility: elem.options.accessibility,
            setGallerySize: elem.options.setGallerySize,
            resize: elem.options.resize,
            cellAlign: elem.options.cellAlign,
            rightToLeft: INSPIRO.core.rtlStatus(),
            on: {
              ready: function (index) {
                var $captions = elem.find(".slide.is-selected .slide-captions > *");
                slide_dark(elem);
                sliderHeight(elem);
                start_kenburn(elem);
                animate_captions($captions);
                setTimeout(function () {
                  elem.find(".slide:not(.is-selected) video").each(function (i, video) {
                    video.pause();
                    video.currentTime = 0;
                  })
                }, 700);
              }
            }
          });

          var flkty = inspiroSliderData.data("flickity");

          inspiroSliderData.on("change.flickity", function () {
            var $captions = elem.find(".slide.is-selected .slide-captions > *");
            hide_captions($captions);
            setTimeout(function () {
              stop_kenburn(elem);
            }, 1000);
            start_kenburn(elem);
            animate_captions($captions);
            elem.find(".slide video").each(function (i, video) {
              video.currentTime = 0;
            });
          });

          inspiroSliderData.on("select.flickity", function () {
            //  INSPIRO.elements.backgroundImage();
            var $captions = elem.find(".slide.is-selected .slide-captions > *");
            slide_dark(elem);
            sliderHeight(elem);
            start_kenburn(elem);
            animate_captions($captions);
            var video = flkty.selectedElement.querySelector("video");
            if (video) {
              video.play();
              flkty.options.autoPlay = Number(video.duration * 1000);
            } else {
              flkty.options.autoPlay = Number(elem.options.autoPlay);
            }
          });
          inspiroSliderData.on("dragStart.flickity", function () {
            var $captions = elem.find(".slide:not(.is-selected) .slide-captions > *");
            hide_captions($captions);
          });
          $(window).resize(function () {
            sliderHeight(elem);
            elem.flickity("reposition");
          });
        })
      }
    },
    carouselAjax: function () {
      INSPIRO.slider.carousel($(".carousel"));
     },
    carousel: function (elem) {
      if (elem) {
        $carousel = elem;
      }

      if ($carousel.length > 0) {
        //Check if flickity plugin is loaded
        if (typeof $.fn.flickity === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery flickity plugin is missing in plugins.js file.", "danger");
          return true;
        }
        $carousel.each(function () {
          var elem = $(this)
          //Plugin Options
          elem.options = {
            containerWidth: elem.width(),
            items: elem.attr("data-items") || 4,
            itemsLg: elem.attr("data-items-lg"),
            itemsMd: elem.attr("data-items-md"),
            itemsSm: elem.attr("data-items-sm"),
            itemsXs: elem.attr("data-items-xs"),
            margin: elem.attr("data-margin") || 10,
            cellSelector: elem.attr("data-item") || false,
            prevNextButtons: elem.data("arrows") == false ? false : true,
            pageDots: elem.data("dots") == false ? false : true,
            fade: elem.data("fade") == true ? true : false,
            draggable: elem.data("drag") == false ? false : true,
            freeScroll: elem.data("free-scroll") == true ? true : false,
            wrapAround: elem.data("loop") == false ? false : true,
            groupCells: elem.data("group-cells") == true ? true : false,
            autoPlay: elem.attr("data-autoplay") || 7000,
            pauseAutoPlayOnHover: elem.data("hover-pause") == false ? false : true,
            asNavFor: elem.attr("data-navigation") || false,
            lazyLoad: elem.data("lazy-load") == true ? true : false,
            initialIndex: elem.attr("data-initial-index") || 0,
            accessibility: elem.data("accessibility") == true ? true : false,
            adaptiveHeight: elem.data("adaptive-height") == true ? true : false,
            autoWidth: elem.data("auto-width") == true ? true : false,
            setGallerySize: elem.data("gallery-size") == false ? false : true,
            resize: elem.data("resize") == false ? false : true,
            cellAlign: elem.attr("data-align") || "left",
            rightToLeft: INSPIRO.core.rtlStatus()
          }

          //Calculate min/max on responsive breakpoints
          elem.options.itemsLg = elem.options.itemsLg || Math.min(Number(elem.options.items), Number(4));
          elem.options.itemsMd = elem.options.itemsMd || Math.min(Number(elem.options.itemsLg), Number(3));
          elem.options.itemsSm = elem.options.itemsSm || Math.min(Number(elem.options.itemsMd), Number(2));
          elem.options.itemsXs = elem.options.itemsXs || Math.min(Number(elem.options.itemsSm), Number(1));
          var setResponsiveColumns;

          function getCarouselColumns() {
            switch ($(window).breakpoints("getBreakpoint")) {
              case "xs":
                setResponsiveColumns = Number(elem.options.itemsXs);
                break;
              case "sm":
                setResponsiveColumns = Number(elem.options.itemsSm);
                break;
              case "md":
                setResponsiveColumns = Number(elem.options.itemsMd);
                break;
              case "lg":
                setResponsiveColumns = Number(elem.options.itemsLg);
                break;
              case "xl":
                setResponsiveColumns = Number(elem.options.items);
                break;
            }
          }
          getCarouselColumns();
          var itemWidth;
          elem.find("> *").wrap('<div class="polo-carousel-item">');
          if (elem.hasClass("custom-height")) {
            elem.options.setGallerySize = false;
            INSPIRO.core.customHeight(elem);
            INSPIRO.core.customHeight(elem.find(".polo-carousel-item"));
            var carouselCustomHeightStatus = true;
          }
          if (Number(elem.options.items) !== 1) {
            if (elem.options.autoWidth || carouselCustomHeightStatus) {
              elem.find(".polo-carousel-item").css({
                "padding-right": elem.options.margin + "px"
              })
            } else {
              itemWidth = (elem.options.containerWidth + Number(elem.options.margin)) / setResponsiveColumns;
              elem.find(".polo-carousel-item").css({
                "width": itemWidth,
                "padding-right": elem.options.margin + "px"
              })
            }
          } else {
            elem.find(".polo-carousel-item").css({
              "width": "100%",
              "padding-right": "0 !important;"
            })
          }
          if (elem.options.autoWidth || carouselCustomHeightStatus) {
            elem.options.cellAlign = "center";
          }

          if (elem.options.autoPlay == "false") {
            elem.options.autoPlay = false;
          }

          if (!$.isNumeric(elem.options.autoPlay) && elem.options.autoPlay != false) {
            elem.options.autoPlay = Number(7000);
          }

          //Initializing plugin and passing the options
          var $carouselElem = $(elem);
          $carouselElem.imagesLoaded(function () {
            // init Isotope after all images have loaded
            $carouselElem.flickity({
              cellSelector: elem.options.cellSelector,
              prevNextButtons: elem.options.prevNextButtons,
              pageDots: elem.options.pageDots,
              fade: elem.options.fade,
              draggable: elem.options.draggable,
              freeScroll: elem.options.freeScroll,
              wrapAround: elem.options.wrapAround,
              groupCells: elem.options.groupCells,
              autoPlay: Number(elem.options.autoPlay),
              pauseAutoPlayOnHover: elem.options.pauseAutoPlayOnHover,
              adaptiveHeight: elem.options.adaptiveHeight,
              asNavFor: elem.options.asNavFor,
              initialIndex: elem.options.initialIndex,
              accessibility: elem.options.accessibility,
              setGallerySize: elem.options.setGallerySize,
              resize: elem.options.resize,
              cellAlign: elem.options.cellAlign,
              rightToLeft: elem.options.rightToLeft,
              contain: true
            });
            elem.addClass("carousel-loaded");
          });
          if (elem.hasClass("custom-height")) {
            INSPIRO.core.customHeight(elem);
          }
          if (Number(elem.options.items) !== 1) {
            $(window).on("resize", function () {
              setTimeout(function () {
                getCarouselColumns();
                itemWidth = (elem.width() + Number(elem.options.margin)) / setResponsiveColumns;
                if (elem.options.autoWidth || carouselCustomHeightStatus) {
                  elem.find(".polo-carousel-item").css({
                    "padding-right": elem.options.margin + "px"
                  })
                } else {
                  if (!elem.hasClass("custom-height")) {
                    elem.find(".polo-carousel-item").css({
                      "width": itemWidth,
                      "padding-right": elem.options.margin + "px"
                    })
                  } else {
                    INSPIRO.core.customHeight(elem.find(".polo-carousel-item"));
                    elem.find(".polo-carousel-item").css({
                      "width": itemWidth,
                      "padding-right": elem.options.margin + "px"
                    })
                  }
                }
                elem.find(".flickity-slider").css({
                  "margin-right": -elem.options.margin / setResponsiveColumns + "px"
                })
                elem.flickity("reposition");
              }, 300);
            });
          }
        })
      }
    }
  }
  INSPIRO.elements = {
    functions: function () {
      INSPIRO.elements.shapeDivider();
      INSPIRO.elements.naTo();
      INSPIRO.elements.morphext();
      INSPIRO.elements.buttons();
      INSPIRO.elements.accordion();
      INSPIRO.elements.animations();
      INSPIRO.elements.parallax();
      INSPIRO.elements.backgroundImage();
      INSPIRO.elements.responsiveVideos();
      INSPIRO.elements.countdownTimer();
      INSPIRO.elements.progressBar();
      INSPIRO.elements.pieChart();
      INSPIRO.elements.maps();
      INSPIRO.elements.gridLayout();
      INSPIRO.elements.tooltip();
      INSPIRO.elements.popover();
      INSPIRO.elements.magnificPopup();
      INSPIRO.elements.yTPlayer();
      INSPIRO.elements.vimeoPlayer();
      INSPIRO.elements.modal();
      INSPIRO.elements.sidebarFixed();
      INSPIRO.elements.clipboard();
      INSPIRO.elements.bootstrapSwitch();
      INSPIRO.elements.countdown();
      INSPIRO.elements.other();
      INSPIRO.elements.videoBackground();
      INSPIRO.elements.forms();
      INSPIRO.elements.formValidation();
      INSPIRO.elements.formAjaxProcessing();
      INSPIRO.elements.floatingDiv();
      INSPIRO.elements.wizard();
      INSPIRO.elements.counters();
    },
    forms: function () {
      //Show hide password
      var $showHidePassword = $(".show-hide-password")
      if ($showHidePassword.length > 0) {
        $showHidePassword.each(function () {
          var elem = $(this),
            $iconEye = "icon-eye",
            $iconClosedEye = "icon-eye-off",
            elemShowHideIcon = elem.find(".input-group-append i"),
            elemInput = elem.children("input")
          elem.find(".input-group-append i").css({
            cursor: "pointer"
          })
          elemShowHideIcon.on("click", function (event) {
            event.preventDefault()
            if (elem.children("input").attr("type") == "text") {
              elemInput.attr("type", "password")
              elemShowHideIcon.removeClass($iconEye)
              elemShowHideIcon.addClass($iconClosedEye)
            } else if (elem.children("input").attr("type") == "password") {
              elemInput.attr("type", "text")
              elemShowHideIcon.addClass($iconEye)
              elemShowHideIcon.removeClass($iconClosedEye)
            }
          })
        })
      }
    },
    formValidation: function () {
      var forms = document.getElementsByClassName("needs-validation")
      var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener(
          "submit",
          function (event) {
            if (form.checkValidity() === false) {
              event.preventDefault()
              event.stopPropagation()
            }
            form.classList.add("was-validated")
          },
          false
        )
      })
    },

    formAjaxProcessing: function () {
      var $ajaxForm = $(".widget-contact-form:not(.custom-js), .ajax-form:not(.custom-js)")
      if ($ajaxForm.length > 0) {
        $ajaxForm.each(function () {
          var elem = $(this),
             elemCustomRedirectPage = elem.attr("data-success-page");
          var button = elem.find("button#form-submit"),
            buttonText = button.html();

          var validation = Array.prototype.filter.call(elem, function (form) {
            form.addEventListener(
              "submit",
              function (event) {
                if (form[0].checkValidity() === false) {
                  event.preventDefault()
                  event.stopPropagation()
                }
                form.classList.add("was-validated")
                return false
              },
              false
            )
          });
          
          elem.submit(function (event) {
            event.preventDefault();
            var post_url = $(this).attr("action");
            var request_method = $(this).attr("method");
            
            if (elem[0].checkValidity() === false) {
              event.stopPropagation()
              elem.addClass("was-validated")
            } else {
              $(elem).removeClass("was-validated")
              button.html('<i class="icon-loader fa-spin"> </i> Sending...')
              $.ajax({
                url: post_url,
                type: request_method,   
                data: new FormData(this),
                cache: false,
                contentType: false,
                processData: false,
                success: function (text) {
                  if (text.response == "success") {
                    if (elem.find(".g-recaptcha").children("div").length > 0) {
                      grecaptcha.reset();
                    }
                    $(elem)[0].reset();
                    button.html(buttonText)
                    if (elemCustomRedirectPage) {
                      window.location.href = elemCustomRedirectPage
                    } else {
                      $.notify({
                        message: text.message
                      }, {
                        type: "success",
                        delay: elem.attr("data-success-message-delay") || 20000
                      })
                    }
                  } else {
                    $.notify({
                      message: elem.attr("data-error-message") || text.message,
                    }, {
                      type: "danger",
                      delay: elem.attr("data-error-message-delay") || 20000
                    })
                    var t = setTimeout(function () {
                      button.html(buttonText)
                    }, 1000)
                  }
                }
              })
            }
          });
        });
      }
    },
    wizard: function () {
      //Show hide password
    },
    floatingDiv: function () {
      var $floatingDiv = $(".floating-div");
      if ($floatingDiv.length > 0) {
        $floatingDiv.each(function () {
          var elem = $(this),
            elemAlign = elem.attr("data-placement") || "bottom",
            elemScrollOffset = elem.attr("data-offset") || 50,
            elemVisible = elem.attr("data-visibile") || "all",
            elemHeight = elem.outerHeight(),
            elemWidth = elem.outerWidth();

          /* if(elemVisible !== "all") {
            
          }else {
            if ($body.hasClass("b--desktop")) {

            }
          } */
          $window.scroll(function () {
            var scrollOffset = $body.attr("data-offset") || 80;
            if ($window.scrollTop() > scrollOffset) {
              elem.css(elemAlign, "20px");
            } else {
              elem.css(elemAlign, -elemHeight + "px");
            }
          });
        });
      }
    },
    other: function (context) {
      //Lazy Load
      var myLazyLoad = new LazyLoad({
        elements_selector: ".lazy",
        class_loaded: "img-loaded"
      });

      if ($(".toggle-item").length > 0) {
        $(".toggle-item").each(function () {
          var elem = $(this),
            toggleItemClass = elem.attr("data-class"),
            toggleItemClassTarget = elem.attr("data-target")
          elem.on("click", function () {
            if (toggleItemClass) {
              if (toggleItemClassTarget) {
                $(toggleItemClassTarget).toggleClass(toggleItemClass)
              } else {
                elem.toggleClass(toggleItemClass)
              }
            }
            elem.toggleClass("toggle-active");
            return false
          })
        })
      }
      /*Dropdown popup invert*/
      var $pDropdown = $(".p-dropdown");
      if ($pDropdown.length > 0) {
        $pDropdown.each(function () {
          var elem = $(this);

          elem.find('> a').on("click", function () {
            elem.toggleClass("dropdown-active");
            return false;
          });


          if ($window.width() / 2 > elem.offset().left) {
            elem.addClass("p-dropdown-invert");
          }
        });
      }

    },
    naTo: function () {
      $("a.scroll-to, #dotsMenu > ul > li > a, .menu-one-page nav > ul > li > a:not([data-lightbox])").on("click", function () {
        var extraPaddingTop = 0,
          extraHeaderHeight = 0
        $(window).breakpoints("lessThan", "lg", function () {
          if (Settings.menuIsOpen) {
            $mainMenuTriggerBtn.trigger("click")
          }
          if ($header.attr("data-responsive-fixed") === true) {
            extraHeaderHeight = $header.height()
          }
        })
        $(window).breakpoints("greaterEqualTo", "lg", function () {
          if ($header.length > 0) {
            extraHeaderHeight = $header.height()
          }
        })
        if ($(".dashboard").length > 0) {
          extraPaddingTop = 30
        }
        var $anchor = $(this)
        $("html, body")
          .stop(true, false)
          .animate({
              scrollTop: $($anchor.attr("href")).offset().top - (extraHeaderHeight + extraPaddingTop)
            },
            1500,
            "easeInOutExpo"
          )
        return false
      })
    },
    morphext: function () {
      var $textRotator = $(".text-rotator")
      if ($textRotator.length > 0) {
        //Check if Morphext plugin is loaded
        if (typeof $.fn.Morphext === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery Morphext plugin is missing in plugins.js file.", "danger")
          return true
        }
        $textRotator.each(function () {
          var elem = $(this)
          //Plugin Options
          elem.options = {
            animation: elem.attr("data-animation") || "fadeIn",
            separator: elem.attr("data-separator") || ",",
            speed: elem.attr("data-speed") || 2000,
            height: elem.height()
          }
          elem.css({
            "min-height": elem.options.height
          })
          //Initializing Morphext plugin and passing the options
          elem.Morphext({
            animation: elem.options.animation,
            separator: elem.options.separator,
            speed: Number(elem.options.speed)
          })
        })
      }
    },
    buttons: function () {
      //Button slide width
      if ($(".btn-slide[data-width]")) {
        $(".btn.btn-slide[data-width]").each(function () {
          var elem = $(this),
            elemWidth = elem.attr("data-width"),
            elemDefaultWidth
          switch (true) {
            case elem.hasClass("btn-lg"):
              elemDefaultWidth = "60"
              break
            case elem.hasClass("btn-sm"):
              elemDefaultWidth = "36"
              break
            case elem.hasClass("btn-xs"):
              elemDefaultWidth = "28"
              break
            default:
              elemDefaultWidth = "48"
              break
          }
          elem.hover(
            function () {
              $(this).css("width", elemWidth + "px")
            },
            function () {
              $(this).css("width", elemDefaultWidth + "px")
            }
          )
        })
      }
    },
    accordion: function () {
      var accordionType = "accordion",
        toogleType = "toggle",
        accordionItem = "ac-item",
        itemActive = "ac-active",
        itemTitle = "ac-title",
        itemContent = "ac-content",
        $accs = $("." + accordionItem)
      $accs.length &&
        ($accs.each(function () {
            var $item = $(this)
            $item.hasClass(itemActive) ? $item.addClass(itemActive) : $item.find("." + itemContent).hide()
          }),
          $("." + itemTitle).on("click", function (e) {
            var $link = $(this),
              $item = $link.parents("." + accordionItem),
              $acc = $item.parents("." + accordionType)
            $item.hasClass(itemActive) ? ($acc.hasClass(toogleType) ? ($item.removeClass(itemActive), $link.next("." + itemContent).slideUp()) : ($acc.find("." + accordionItem).removeClass(itemActive), $acc.find("." + itemContent).slideUp())) : ($acc.hasClass(toogleType) || ($acc.find("." + accordionItem).removeClass(itemActive), $acc.find("." + itemContent).slideUp("fast")), $item.addClass(itemActive), $link.next("." + itemContent).slideToggle("fast")), e.preventDefault()
            return false
          }))
    },
    animations: function () {
      var $animate = $("[data-animate]")
      if ($animate.length > 0) {
        //Check if jQuery Waypoint plugin is loaded
        if (typeof Waypoint === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery Waypoint plugin is missing in plugins.js file.", "danger")
          return true
        }
        $animate.each(function () {
          var elem = $(this)
          elem.addClass("animated")
          //Plugin Options
          elem.options = {
            animation: elem.attr("data-animate") || "fadeIn",
            delay: elem.attr("data-animate-delay") || 200,
            direction: ~elem.attr("data-animate").indexOf("Out") ? "back" : "forward",
            offsetX: elem.attr("data-animate-offsetX") || 0,
            offsetY: elem.attr("data-animate-offsetY") || -100
          }
          //Initializing jQuery Waypoint plugin and passing the options from data animations attributes
          if (elem.options.direction == "forward") {
            new Waypoint({
              element: elem,
              handler: function () {
                var t = setTimeout(function () {
                  elem.addClass(elem.options.animation + " visible")
                }, elem.options.delay)
                this.destroy()
              },
              offset: "100%"
            })
          } else {
            elem.addClass("visible")
            elem.on("click", function () {
              elem.addClass(elem.options.animation)
              return false
            })
          }
          //Demo play
          if (elem.parents(".demo-play-animations").length) {
            elem.on("click", function () {
              elem.removeClass(elem.options.animation)
              var t = setTimeout(function () {
                elem.addClass(elem.options.animation)
              }, 50)
              return false
            })
          }
        })
      }
    },
    parallax: function () {
      var $parallax = $("[data-bg-parallax]")
      if ($parallax.length > 0) {
        //Check if scrolly plugin is loaded
        if (typeof $.fn.scrolly === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery scrolly plugin is missing in plugins.js file.", "danger")
          return true
        }
        $parallax.each(function () {
          var $elem = $(this),
            elemImageSrc = $elem.attr("data-bg-parallax"),
            elemImageVelocity = $elem.attr("data-velocity") || "-.140"
          $elem.prepend('<div class="parallax-container" data-bg="' + elemImageSrc + '"  data-velocity="' + elemImageVelocity + '" style="background: url(' + elemImageSrc + ')"></div>')

          var parallaxLazy = new LazyLoad({
            elements_selector: ".parallax-container",
            class_loaded: "img-loaded"
          });

          $elem.find(".parallax-container").scrolly({
            bgParallax: true
          });
        })
      }
    },
    backgroundImage: function () {
      var $backgroundImage = $("[data-bg-image]");

      if ($backgroundImage.length > 0) {
        $backgroundImage.each(function () {
          var $elem = $(this),
            elemImageSrc = $elem.attr("data-bg-image");
          $elem.addClass("lazy-bg");
          $elem.attr("data-bg", elemImageSrc);
        });

        var laazybg = new LazyLoad({
          elements_selector: ".lazy-bg",
          class_loaded: "bg-loaded"
        });

      }
    },
    shapeDivider: function () {
      var $shape_divider = $(".shape-divider")
      $shape_divider.each(function () {
        var elem = $(this)
        elem.options = {
          style: elem.attr("data-style") || 1,
          color: elem.attr("data-color") || "#ffffff",
          opacity: elem.attr("data-opacity") || "1",
          zIndex: elem.attr("data-zIndex") || "0",
          height: elem.attr("data-height") || 210,
          prefix: "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2MzAg"
        }

        if ($body.hasClass("dark") && elem.options.color === "#ffffff") {
          elem.options.color = "#181818";
        }
        switch (elem.options.style) {
          case "1":
            elem.options.style =
              elem.options.prefix +
              "MTI1LjcyIj48dGl0bGU+QXNzZXQgMTc0PC90aXRsZT48cGF0aCBkPSJNMzk1LDk5LjM3Yy01Ny40MywxMC4xNy0xMjQuMjctOC4wNi0xNzYuOC0xMS43MnEzLjkzLjY0LDgsMS40MWM1MC44MSw2LDExMy4zLDI0LjA4LDE2OC43NiwxNC4yNkM0NjgsOTAuNDIsNTE5LjYsMTEuODgsNjMwLDguOVYwQzUwNS40Miw0LDQ2OCw4Ni40NywzOTUsOTkuMzdaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC4zMDAwMDAwMDAwMDAwMDAwNCIvPjxwYXRoIGQ9Ik0yMjYuMjUsODlDMjczLjg4LDk4LDMzOC4xNCwxMTkuMjksMzk1LDEwOS4yM2M3Mi45My0xMi45MSwxMjYuNjEtNzcuNDYsMjM1LTczLjQ4VjguODZjLTExMC40LDMtMTYyLDgxLjUxLTIzNSw5NC40MkMzMzkuNTUsMTEzLjEsMjc3LjA2LDk1LjA3LDIyNi4yNSw4OVoiIHN0eWxlPSJmaWxsOiNmZmY7b3BhY2l0eTowLjYzIi8+PHBhdGggZD0iTTYwLjgyLDEyMi44OCw2MiwxMjNhMzEuNDksMzEuNDksMCwwLDAsOS4zNC0uNjRBMTAxLjI2LDEwMS4yNiwwLDAsMSw2MC44MiwxMjIuODhaIiBzdHlsZT0iZmlsbDojZmZmIi8+PHBhdGggZD0iTTYwLjgyLDEyMi44OCw2MiwxMjNhMzEuNDksMzEuNDksMCwwLDAsOS4zNC0uNjRBMTAxLjI2LDEwMS4yNiwwLDAsMSw2MC44MiwxMjIuODhaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC4zNTAwMDAwMDAwMDAwMDAwMyIvPjxwYXRoIGQ9Ik0zOTgsMTA3Ljg0Yy01Ni4xNSwxMC4wNy0xMTkuNTktMTEuMjYtMTY2LjYyLTIwLjItMi43MS0uNTItNS4zNS0xLTcuOTQtMS40MUExNTkuNTQsMTU5LjU0LDAsMCwwLDIwMiw4NHEtMy4wOS0uMDktNiwwYy0uNzEsMC0xLjM5LjA4LTIuMDkuMTItNTIuOCwyLjkzLTgwLjM0LDI4Ljc4LTExMi45MSwzNi42MmE3Mi42Myw3Mi42MywwLDAsMS05LjY2LDEuNjJBMzEuNDksMzEuNDksMCwwLDEsNjIsMTIzbC0xLjE4LS4xM0MzMS4zNywxMjIuODUsMCwxMTEuODIsMCwxMTEuODJ2MTMuOUg2MzBWMzQuMzZDNTIzLDMwLjM5LDQ3MCw5NC45NCwzOTgsMTA3Ljg0WiIgc3R5bGU9ImZpbGw6I2ZmZiIvPjxwYXRoIGQ9Ik0wLDEwMi4xNHYxMGM4MywzNCwxMjYuODMtMTQsMTkwLTI0bDEtNGMtNDQuNCw2LjI2LTQ1LDIyLTkzLDMxQzU0Ljc4LDEyMy4yNSwzMCwxMTMuMTQsMCwxMDIuMTRaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC4zMDAwMDAwMDAwMDAwMDAwNCIvPjxwYXRoIGQ9Ik0wLDEwNC4xNHYxMGMyMiw5LDQxLjIzLDEwLjI2LDU4LjgsMTAsNDguNzgtLjc2LDg0Ljc2LTI2LjY1LDEzMS4yLTM0bDEtNGMtNDQuNCw2LjI2LTQ1LDIyLTkzLDMxQzU0Ljc4LDEyNS4yNSwzMCwxMTUuMTQsMCwxMDQuMTRaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC4zMDAwMDAwMDAwMDAwMDAwNCIvPjwvc3ZnPg=="
            break
          case "2":
            elem.options.style = elem.options.prefix + "MTIwIj48dGl0bGU+QXNzZXQgMTY0PC90aXRsZT48cGF0aCBkPSJNNTY3LjY3LDMxLjE0Yy0yNi4yMiwxNy4zNi01MCwzNi41NS04MS44LDUwQzQzNy41MiwxMDEuNDgsMzc1LjUyLDEwNi4yMSwzMTcsMTAzLjIzcy0xMTUuNDItMTMtMTczLjE1LTE5LjU2Qzk2LjQ3LDc4LjI1LDQ3LjE4LDc1LjE4LDAsODAuMDd2MzIuNDFINjMwVjBDNjA2LjQ0LDcuNTIsNTg1Ljg5LDE5LjA5LDU2Ny42NywzMS4xNFoiIHN0eWxlPSJmaWxsOiNmZmY7b3BhY2l0eTowLjY0Ii8+PHBhdGggZD0iTTU2Ny42NywzOC42N2MtMjYuMjIsMTcuMzUtNTAsMzYuNTUtODEuOCw1MEM0MzcuNTIsMTA5LDM3NS41MiwxMTMuNzMsMzE3LDExMC43NXMtMTE1LjQyLTEzLTE3My4xNS0xOS41NkM5Ni40Nyw4NS43Nyw0Ny4xOCw4Mi43LDAsODcuNTlWMTIwSDYzMFY3LjUyQzYwNi40NCwxNSw1ODUuODksMjYuNjEsNTY3LjY3LDM4LjY3WiIgc3R5bGU9ImZpbGw6I2ZmZiIvPjwvc3ZnPg=="
            break
          case "3":
            elem.options.style = elem.options.prefix + "NjAiPjx0aXRsZT5Bc3NldCAxNzI8L3RpdGxlPjxwYXRoIGQ9Ik0wLDAsNDAwLDUzLjIzLDYzMCwwVjYwSDBaIiBzdHlsZT0iZmlsbDojZmZmIi8+PC9zdmc+"
            break
          case "4":
            elem.options.style = elem.options.prefix + "ODAiPjx0aXRsZT40PC90aXRsZT48cGF0aCBkPSJNMjYxLjIsNjQuOUMzNjcuNiw1NC43LDQ5OS42LDM5LjcsNjMwLDE4LjVWMEM0OTcuOCwzMS40LDM2My43LDUyLDI2MS4yLDY0LjlaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC4zMDAwMDAwMDAwMDAwMDAwNCIvPjxwYXRoIGQ9Ik0yNjEuMiw2NC45Yy00MSwzLjktNzguMiw3LjEtMTEwLDkuNiwxMy4yLS40LDI3LS45LDQxLjUtMS42QzMxNSw2Ny43LDQ3OC40LDU5LjQsNjMwLDM0LjhWMTguNUM0OTkuMSwzOS44LDM2Ny4zLDU0LjgsMjYxLjIsNjQuOVoiIHN0eWxlPSJmaWxsOiNmZmY7b3BhY2l0eTowLjYwMDAwMDAwMDAwMDAwMDEiLz48cGF0aCBkPSJNMTkyLjcsNzIuOWMtMTQuNS43LTI4LjMsMS4yLTQxLjUsMS42QzU5LjksNzcuNywwLDc3LjQsMCw3Ny40VjgwSDYzMFYzMy44QzQ3OC40LDU4LjQsMzE1LDY3LjcsMTkyLjcsNzIuOVoiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
          case "5":
            elem.options.style = elem.options.prefix + "MTAwIj48dGl0bGU+QXNzZXQgMTczPC90aXRsZT48cGF0aCBkPSJNMCw1Ni44NGwxMDgsMzlMNDY4LDAsNjMwLDY4LjQyVjEwMEgwWiIgc3R5bGU9ImZpbGw6I2ZmZiIvPjwvc3ZnPg=="
            break
          case "6":
            elem.options.style =
              elem.options.prefix +
              "MTIwIj48dGl0bGU+NjwvdGl0bGU+PHBhdGggZD0iTTYxNS41LDIuNWMtNDEuMyw1LjgtNzcuNCwxMi43LTExNiwxMy43LTIyLjIuNi00NC44LTMuMy02Ny4yLjQtNDguOCw4LjEtMTA3LjgsNDMuNS0xNTcuNyw2Mi42LTQyLjQsMTYuMi02OS45LDE2LTk4LjcsMy44LTIxLjEtOS00Mi4xLTIyLjktNjUuMi0zMy4xLTI5LjQtMTMtNjIuNC0yNC4yLTk4LjktMTIuM2wtMS4xLjNMMCw0MS42VjUzLjhsMTAuNy0zLjYsMS4xLS40YzQyLjEtMTMuNyw2My4xLTUuNiw5OC45LDUuNiwyMi43LDcsNDQuMSwyMCw2NS4yLDI4LjksMzAuOSwxMy4xLDU1LjgsMTMsOTguNy0xLDQ5LjktMTYuNCwxMDguOS01MS44LDE1Ny43LTU5LjksMjIuNC0zLjcsNDUuMi00LjUsNjcuMi0uNCwzNy44LDcuMiw3NC43LDcuMSwxMTYsMS4zLDUtLjcsOS44LTEuNSwxNC41LTIuNVYwQzYyNS4zLDEsNjIwLjUsMS45LDYxNS41LDIuNVoiIHN0eWxlPSJmaWxsOiNmZmY7b3BhY2l0eTowLjM1MDAwMDAwMDAwMDAwMDAzIi8+PHBhdGggZD0iTTQ5OS41LDIzYy0yMi00LjEtNDQuOC0zLjMtNjcuMi40LTQ4LjgsOC4xLTEwNy44LDQzLjUtMTU3LjcsNTkuOS00Mi45LDE0LTY3LjgsMTQuMS05OC43LDEtMjEuMS04LjktNDIuNS0yMS45LTY1LjItMjguOUM3NC45LDQ0LjIsNTMuOSwzNi4xLDExLjgsNDkuOGwtMS4xLjRMMCw1My44VjYybDEwLjctMy42LDEuMS0uNGMzNi41LTExLjksNjguOC04LDk4LjksMS40LDIyLjcsNy4xLDQ0LjEsMTcuMyw2NS4yLDI2LjMsMjguOCwxMi4yLDU1LjcsMTIuOSw5OS4xLDIuOSw1Mi41LTEyLjEsMTA3LjEtNTEuNywxNTUuOS01OS44LDIyLjMtMy44LDQ2LjYtMS44LDY4LjYsMi40LDM3LjgsNy4xLDc0LjcsMjIsMTE2LDE2LjMsNS0uNyw5LjgtMS42LDE0LjUtMi42VjIxLjhjLTQuNywxLTkuNSwxLjgtMTQuNSwyLjVDNTc0LjIsMzAuMSw1MzcuMywzMC4yLDQ5OS41LDIzWiIgc3R5bGU9ImZpbGw6I2ZmZjtvcGFjaXR5OjAuNSIvPjxwYXRoIGQ9Ik00OTkuNSwzMS4yYy0yMi00LjItNDYuMy02LjItNjguNi0yLjRDMzgyLjEsMzYuOSwzMjcuNSw3Ni41LDI3NSw4OC42Yy00My40LDEwLTcwLjMsOS4zLTk5LjEtMi45LTIxLjEtOS00Mi41LTE5LjItNjUuMi0yNi4zQzgwLjYsNTAsNDguMyw0Ni4xLDExLjgsNThsLTEuMS40TDAsNjJ2NThINjMwVjQ0LjljLTQuNywxLTkuNSwxLjktMTQuNSwyLjZDNTc0LjIsNTMuMiw1MzcuMywzOC4zLDQ5OS41LDMxLjJaIiBzdHlsZT0iZmlsbDojZmZmIi8+PC9zdmc+"
            break
          case "7":
            elem.options.style = elem.options.prefix + "MTIwIj48dGl0bGU+QXNzZXQgMTc0PC90aXRsZT48cGF0aCBkPSJNMCwwLDYzMCwxMjBIMFoiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
          case "8":
            elem.options.style =
              elem.options.prefix +
              "MTIwIj48dGl0bGU+ODwvdGl0bGU+PHBhdGggZD0iTTQ1Ni43LDUzLjZDNDM5LjgsNDIuOSwzOTYuOSwxLjgsMzQzLjIsMzAuMWMtMzUuNywxOC43LTg0LDcxLjUtMTI3LjgsNzEuOS0zNi4xLjMtNTcuOC0yMC4yLTgxLjQtMzUuMS0xNy4zLTExLTM1LTIzLjUtNTMuNi0zMi4yQzU1LjYsMjMuMiwzMCwxMS44LjEsMjYuNGMtLjMuMSwwLDkzLjYsMCw5My42SDYzMFYzMS44Yy0zLjksMS4zLTEzLDE3LjMtNjUuMiwzMi44QzUzMy4zLDc2LjQsNDkyLjQsNzYuNCw0NTYuNyw1My42WiIgc3R5bGU9ImZpbGw6I2ZmZiIvPjxnIHN0eWxlPSJvcGFjaXR5OjAuMzgiPjxwYXRoIGQ9Ik02MTEsNjMuNmwtMiw0Mi44LTUyNy45LDUtODEtMS4xVjYxLjhhMTk0LjcsMTk0LjcsMCwwLDAsMjQuNyw5LjQsMTQ2LjgsMTQ2LjgsMCwwLDAsNDMuOSw2LjJDOTQuNiw3Ny4zLDEyMC41LDY1LDE0Niw1MC41YzE4LjctMTAuNiwzNy4xLTIyLjMsNTUuMi0zMS4zQzIxMy43LDEyLjksMjI2LDgsMjM4LjEsNS43YzI0LjMtNC42LDUxLjQtMy4yLDcyLjUsNy45bDM2LjcsMTkuNmMzNy4zLDE5LjksNzMuMSwzOC45LDEwNC4yLDUxLjdDNDY1LjQsOTAuNiw0NzguMyw5NS4yLDQ5MCw5OGMxMy4zLDMuMywyNS4xLDQuNSwzNSwyLjlhNzUuNSw3NS41LDAsMCwwLDkuMy0zLjdsNy40LTMuM2MxNS40LTcuMSwzOC44LTE5LjEsNTkuNi0zMy4yLDUuNS0zLjcuNi40LDUuNy0zLjRDNjE5LDQ4LjIsNjA4LjcsNjQuMiw2MTEsNjMuNloiIHN0eWxlPSJmaWxsOiNmZmYiLz48L2c+PHBhdGggZD0iTTU4MS44LDExLjRDNTUyLC4yLDUzMS41LDMuOSw1MDcuMiw4LjQsNDcyLjEsMTUsNDM0LjcsNDQuMSwzOTYuNiw2My4yYy0xNi4zLDguMS0zMi44LDE0LjQtNDkuMiwxNi4zLTE1LjgtNS40LTMyLTEyLjItNDcuNi0xOS4yLTM3LjktMTcuMS03Mi42LTM1LjctOTEuOS0zOS44bC02LjctMS4zYy0yMi4yLTQuMi00NS45LTUuOC02Ny45LTEuNy0xMC40LDItMjEsNS45LTMxLjgsMTFDNzYuNiw0MC4yLDUwLjksNTcuOSwyNC44LDcxLjJBMjEzLjYsMjEzLjYsMCwwLDEsLjEsODIuMXYzMC44bDgxLTEuNSwzMTIuMy01LjcsMS40LjNMNjMwLDExMS44di04MEM2MTMsMjYuNCw2MTkuMywyNS41LDU4MS44LDExLjRaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC40OSIvPjxnIHN0eWxlPSJvcGFjaXR5OjAuMzgiPjxwYXRoIGQ9Ik01NDUuNCw5N2wtMTEuMS4yTDQ5MCw5OCwuMSwxMDcuMVYwQzIxLjMtLjQsNDEuMyw0LjEsNjAuNCwxMC44YTQwMy43LDQwMy43LDAsMCwxLDQxLjEsMTcuN2MxMCw0LjksMTkuOSw5LjksMjkuNywxNC42LDUsMi4zLDkuOSw0LjksMTQuOCw3LjQsMjYuMSwxMy41LDUyLjcsMjgsOTIuOSwyNy44LDIwLjMtLjEsNDAuNy03LjcsNjAuOS0xOCwxNi04LjIsMzEuOS0xOCw0Ny41LTI3LjEsMjAuOS0xMi4xLDQxLjMtMjIuOSw2MC45LTI2LjZDNDMyLjUsMiw0ODEuMSw4LjYsNTA0LDE4czQ5LjYsMjMuNiw5Ny4zLDQyLjdDNjIwLjIsNjguNCw1NDUuNCw5Nyw1NDUuNCw5N1oiIHN0eWxlPSJmaWxsOiNmZmYiLz48L2c+PC9zdmc+"
            break
          case "9":
            elem.options.style = elem.options.prefix + "MTAwIj48dGl0bGU+QXNzZXQgMTgyPC90aXRsZT48cGF0aCBkPSJNMCw0NS42NVMxNTksMCwzMjIsMCw2MzAsNDUuNjUsNjMwLDQ1LjY1VjEwMEgwWiIgc3R5bGU9ImZpbGw6I2ZmZiIvPjwvc3ZnPg=="
            break
          case "10":
            elem.options.style = elem.options.prefix + "MTIwIj48dGl0bGU+MTA8L3RpdGxlPjxwYXRoIGQ9Ik0wLDEwOC4xSDYzMFYwUzQ3NSwxMDQuNiwzMTQsMTA0LjYsMCwwLDAsMFoiIHN0eWxlPSJmaWxsOiNmZmY7b3BhY2l0eTowLjIyIi8+PHBhdGggZD0iTTAsMTA2LjlINjMwVjE3LjhzLTE1NSw4Ny45LTMxNiw4Ny45UzAsMTksMCwxOVoiIHN0eWxlPSJmaWxsOiNmZmY7b3BhY2l0eTowLjM2Ii8+PHBhdGggZD0iTTAsMTIwSDYzMFY0NS4xcy0xNTUsNjEuOC0zMTYsNjEuOFMwLDQ1LjEsMCw0NS4xWiIgc3R5bGU9ImZpbGw6I2ZmZiIvPjwvc3ZnPg=="
            break
          case "11":
            elem.options.style = elem.options.prefix + "MTIwIj48dGl0bGU+MTE8L3RpdGxlPjxwYXRoIGQ9Ik01MTAuNywyLjljLTk4LjksMjEuOS0yMjIuMyw4NS41LTMyMiw4NS41QzgwLjEsODguNCwyNC4xLDU2LjEsMCwzNi40VjEyMEg2MzBWMTUuMkM2MDIuNCw2LjksNTUwLjEtNS44LDUxMC43LDIuOVoiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
          case "12":
            elem.options.style = elem.options.prefix + "MTIwIj48dGl0bGU+MTI8L3RpdGxlPjxwYXRoIGQ9Ik02MzAsMzQuNWE1NCw1NCwwLDAsMS05LDIuM0M1NzguMyw0Ni4xLDU1Ni4xLDI0LDUxNy4yLDEyLjVjLTIyLjktNi43LTQ3LjktOS44LTcxLTMuOUMzOTUuOCwyMS43LDM0MC4zLDEwMiwyODUuMSwxMDIuNGMtNDUuNC4zLTcyLjYtMjYuNS0xMDIuMy00Ni4xLTIxLjgtMTQuNC00NC0zMC44LTY3LjQtNDIuMUM4NC4yLS45LDUwLjktNy4yLDEzLjIsMTEuOGwtMS4yLjZjLTMuNSwxLjktOC4yLDMuOS0xMiw1LjlWMTIwSDYzMFoiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
          case "13":
            elem.options.style = elem.options.prefix + "OTAiPjx0aXRsZT4xMzwvdGl0bGU+PHBhdGggZD0iTTYzMCw5MEgxTDAsMFMxMzEsNzYuNiwzNjYsMzQuMmMxMjAtMjEuNywyNjQsNC41LDI2NCw0LjVaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC4xNiIvPjxwYXRoIGQ9Ik0xLDkwSDYzMFYwUzQ4OSw3NC4zLDI1NCwzMS45QzEzNCwxMC4zLDAsMzMsMCwzM1oiIHN0eWxlPSJmaWxsOiNmZmY7b3BhY2l0eTowLjIiLz48cGF0aCBkPSJNMCw5MEg2MzBWMTguMlM0NzUsNzcuNSwzMTQsNzcuNSwwLDE4LjIsMCwxOC4yWiIgc3R5bGU9ImZpbGw6I2ZmZiIvPjwvc3ZnPg=="
            break
          case "14":
            elem.options.style = elem.options.prefix + "NjAiPjx0aXRsZT5Bc3NldCAxNzg8L3RpdGxlPjxwYXRoIGQ9Ik0wLDAsMTEzLDE5LDU4MiwyOS40Nyw2MzAsMFY2MEgwWiIgc3R5bGU9ImZpbGw6I2ZmZiIvPjwvc3ZnPg=="
            break
          case "15":
            elem.options.style = elem.options.prefix + "ODAiPjx0aXRsZT5Bc3NldCAxNzc8L3RpdGxlPjxwYXRoIGQ9Ik0zMTUsMCw2MzAsODBIMFoiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
          case "16":
            elem.options.style = elem.options.prefix + "ODAiPjx0aXRsZT4xNjwvdGl0bGU+PHBhdGggZD0iTTAsODBTMjA4LDAsMzE1LDAsNjMwLDgwLDYzMCw4MFoiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
          case "17":
            elem.options.style =
              elem.options.prefix +
              "MTIwIj48dGl0bGU+MTc8L3RpdGxlPjxwYXRoIGQ9Ik0zMjAsMTZjODguNCwyLDMxMCwxMDQsMzEwLDEwNFM1NjkuNiw4Ny4zLDQ5OS41LDU2Yy0xOS43LTguOC00MC4xLTE3LjUtNjAuMi0yNS4zQzM5NS4yLDEzLjYsMzUyLjcuNywzMjQsMCwyMzUtMiwwLDEyMCwwLDEyMGwxNC4xLTUuNUM2Mi41LDkyLjgsMjQzLjMsMTQuMywzMjAsMTZaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC4zMSIvPjxwYXRoIGQ9Ik0xNC4xLDExNC41QzY0LjksOTUsMjM5LjQsMzAuMywzMTUsMzJjODguNCwyLDMxNSw4OCwzMTUsODhTNDA4LjQsMTgsMzIwLDE2QzI0My4zLDE0LjMsNjIuNSw5Mi44LDE0LjEsMTE0LjVaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC40MyIvPjxwYXRoIGQ9Ik0xNC4xLDExNC41QzY0LjksOTUsMjM5LjQsMzAuMywzMTUsMzJjODguNCwyLDMxNSw4OCwzMTUsODhTNDA4LjQsMTgsMzIwLDE2QzI0My4zLDE0LjMsNjIuNSw5Mi44LDE0LjEsMTE0LjVaIiBzdHlsZT0iZmlsbDojZmZmO29wYWNpdHk6MC4zMSIvPjxwYXRoIGQ9Ik0zMTUsMzJDMjM5LjQsMzAuMyw2NC45LDk1LDE0LjEsMTE0LjVMMiwxMjBINjMwUzQwMy40LDM0LDMxNSwzMloiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
          case "18":
            elem.options.style = elem.options.prefix + "NDAiPjx0aXRsZT5Bc3NldCAxNzk8L3RpdGxlPjxwYXRoIGQ9Ik0wLDE4LjEsNTMsMS45LDEwMywyMGw1OS05LjUyLDU2LDE1LjIzLDcyLTcuNjEsNDYsNC43NiwzNC00Ljc2LDM2LDguNTcsNzYtMTksODUsMTUuMjRMNjMwLDBWMzcuMTRIMFoiIHN0eWxlPSJmaWxsOiNmZmY7b3BhY2l0eTowLjQ3MDAwMDAwMDAwMDAwMDAzIi8+PHBhdGggZD0iTTAsMjAsNTMsMy44MSwxMDMsMjEuOWw1OS05LjUyLDU2LDE1LjI0TDI5MCwyMGw0Niw0Ljc2TDM3MCwyMGwzNiw5LjUyLDc2LTE3LjE0LDg1LDE2LjE5LDYzLTE2LjE5VjQwSDBaIiBzdHlsZT0iZmlsbDojZmZmIi8+PC9zdmc+"
            break
          case "19":
            elem.options.style =
              elem.options.prefix +
              "ODAiPjx0aXRsZT4xOTwvdGl0bGU+PHBhdGggZD0iTTYzMCwzNi45YTM0LjYsMzQuNiwwLDAsMC0xNi41LTQuMmMtMTcuMiwwLTMxLjgsMTIuNy0zNi43LDMwLjNhMjEuMiwyMS4yLDAsMCwwLTkuMy0yLjIsMjEuOCwyMS44LDAsMCwwLTEzLjksNS4xLDM4LjcsMzguNywwLDAsMC00MC40LTQuOGMtNS4yLTcuNy0xMy40LTEyLjYtMjIuNy0xMi42YTI1LjcsMjUuNywwLDAsMC04LjcsMS41QzQ3Mi45LDI3LjgsNDUzLDEyLjQsNDMwLDEyLjRzLTQyLjcsMTUuMy01MS43LDM3LjJjLTcuMi0xMC45LTE4LjgtMTguMS0zMS44LTE4LjFhMzcsMzcsMCwwLDAtMjQsOS4yYy02LTEwLjMtMTYuMy0xNy0yOC0xNy0xMy44LDAtMjUuNiw5LjMtMzAuNywyMi43QTI2LjUsMjYuNSwwLDAsMCwyNDQsMzcuMmEyMiwyMiwwLDAsMC01LjguN2MtNC0xMS42LTE0LTE5LjktMjUuNy0xOS45YTI0LjcsMjQuNywwLDAsMC05LjQsMS45QzE4OS4yLDcuNCwxNzEuNiwwLDE1Mi41LDAsMTI0LjYsMCwxMDAsMTUuOCw4NS4zLDM5LjlBMjcuNiwyNy42LDAsMCwwLDYzLDI4LjJhMjMuOSwyMy45LDAsMCwwLTcuMSwxQzQ3LjIsMTMsMzEuNSwyLjMsMTMuNSwyLjNBNDMuMyw0My4zLDAsMCwwLDAsNC40VjgwSDYzMFoiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
          case "20":
            elem.options.style = elem.options.prefix + "MTAwIj48dGl0bGU+QXNzZXQgMTgwPC90aXRsZT48cGF0aCBkPSJNNjMwLDYwLjgyVjEwMEgwVjk1Ljg4bDExLjkxLTYuNDlMODQsNDMuMzRsMzYuNDksMjQuNDVMMTYwLDQ2LDIzMi4wNSwwbDQ5LjA3LDMyLjg5LDM0LjA3LDI5LjU5LDY4LjI5LDI3Ljc1TDQyMyw2NWw0Mi4yLDI4LjI5LDE4LjM5LTE2LDQ5LjA3LTMyLjg5TDU5NCw4My42MSw2MjgsNjEuOVoiIHN0eWxlPSJmaWxsOiNmZmYiLz48L3N2Zz4="
            break
        }
        var decodeSvg = atob(elem.options.style)
        var wrapper = document.createElement("div")
        wrapper.innerHTML = decodeSvg
        var svg = wrapper.firstChild
        var paths = svg.getElementsByTagName("path");
        [].forEach.call(paths, function (path) {
          path.style.fill = elem.options.color
        })

        svg.setAttribute("preserveAspectRatio", "none");
        if ($body.hasClass("b--desktop")) {
          if (elem.options.height) {
            svg.setAttribute("style", "height:" + Number(elem.options.height).toFixed() + "px")
          } else {
            svg.setAttribute("style", "height:" + Number(svg.height.baseVal.value).toFixed() + "px")
          }
        } else {
          if (elem.options.height) {
            svg.setAttribute("style", "height:" + Number(elem.options.height).toFixed() / 2 + "px")
          } else {
            svg.setAttribute("style", "height:" + Number(svg.height.baseVal.value).toFixed() / 2 + "px")
          }
        }
        $(".shape-divider svg title").remove()
        elem.css({
          "z-index": elem.options.zIndex,
          "opacity": elem.options.opacity
        })
        elem.append(svg)
      })
    },
    responsiveVideos: function () {
      //selecting elements
      var selectors = ['iframe[src*="player.vimeo.com"]', 'iframe[src*="youtube.com"]', 'iframe[src*="youtube-nocookie.com"]', 'iframe[src*="kickstarter.com"][src*="video.html"]', "object", "embed"]
      var videoContainers = $("section, .content, .post-content, .video-js, .post-video, .video-wrap, .ajax-quick-view,#slider:not(.revslider-wrap)")
      var elem = videoContainers.find(selectors.join(","))
      if (elem) {
        elem.each(function () {
          $(this).wrap('<div class="embed-responsive embed-responsive-16by9"></div>')
        })
      }
    },
    counters: function () {
      var $counter = $(".counter")
      if ($counter.length > 0) {
        //Check if countTo plugin is loaded
        if (typeof $.fn.countTo === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery countTo plugin is missing in plugins.js file.", "danger")
          return true
        }
        //Initializing countTo plugin
        $counter.each(function () {
          var elem = $(this),
            prefix = elem.find("span").attr("data-prefix") || "",
            suffix = elem.find("span").attr("data-suffix") || ""
          setTimeout(function () {
            new Waypoint({
              element: elem,
              handler: function () {
                elem.find("span").countTo({
                  refreshInterval: 2,
                  formatter: function (value, options) {
                    return String(prefix) + value.toFixed(options.decimals) + String(suffix)
                  }
                })
                this.destroy()
              },
              offset: "104%"
            })
          }, 100);
        })
      }
    },
    countdownTimer: function () {
      var $countdownTimer = $(".countdown")
      if ($countdownTimer.length > 0) {
        //Check if countdown plugin is loaded
        if (typeof $.fn.countdown === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery countdown plugin is missing in plugins.js file.", "danger")
          return true
        }
        $(".countdown").each(function (index, element) {
          var elem = $(element),
            finalDate = elem.attr("data-countdown");

          elem.countdown(finalDate, function (event) {
            elem.html(event.strftime('<div class="countdown-container"><div class="countdown-box"><div class="number">%-D</div><span>Days</span></div>' + '<div class="countdown-box"><div class="number">%H</div><span>Hours</span></div>' + '<div class="countdown-box"><div class="number">%M</div><span>Minutes</span></div>' + '<div class="countdown-box"><div class="number">%S</div><span>Seconds</span></div></div>'))
          });
        })
      }
    },
    progressBar: function () {
      var $progressBar = $(".p-progress-bar") || $(".progress-bar")
      if ($progressBar.length > 0) {
        $progressBar.each(function (i, elem) {
          var $elem = $(this),
            percent = $elem.attr("data-percent") || "100",
            delay = $elem.attr("data-delay") || "60",
            type = $elem.attr("data-type") || "%"
          if (!$elem.hasClass("progress-animated")) {
            $elem.css({
              width: "0%"
            })
          }
          var progressBarRun = function () {
            $elem
              .animate({
                  width: percent + "%"
                },
                "easeInOutCirc"
              )
              .addClass("progress-animated")
            $elem.delay(delay).append('<span class="progress-type">' + type + '</span><span class="progress-number animated fadeIn">' + percent + "</span>")
          }
          if ($body.hasClass("breakpoint-lg") || $body.hasClass("breakpoint-xl")) {
            new Waypoint({
              element: $(elem),
              handler: function () {
                var t = setTimeout(function () {
                  progressBarRun()
                }, delay)
                this.destroy()
              },
              offset: "100%"
            })
          } else {
            progressBarRun()
          }
        })
      }
    },
    pieChart: function () {
      var $pieChart = $(".pie-chart")
      if ($pieChart.length > 0) {
        //Check if easyPieChart plugin is loaded
        if (typeof $.fn.easyPieChart === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery easyPieChart plugin is missing in plugins.js file.", "danger")
          return true
        }
        $pieChart.each(function () {
          var elem = $(this)
          //Plugin Options
          elem.options = {
            barColor: elem.attr("data-color") || $theme_color,
            trackColor: elem.attr("data-trackcolor") || "rgba(0,0,0,0.10)",
            scaleColor: elem.attr("data-scaleColor") || false,
            scaleLength: elem.attr("data-scaleLength") || 5,
            lineCap: elem.attr("data-lineCap") || "square",
            lineWidth: elem.attr("data-lineWidth") || 6,
            size: elem.attr("data-size") || 160,
            rotate: elem.attr("data-rotate") || 0,
            animate: elem.attr("data-animate") || 2600,
            elemEasing: elem.attr("data-easing") || "easeInOutExpo"
          }
          elem.find("span, i").css({
            "width": elem.options.size + "px",
            "height": elem.options.size + "px",
            "line-height": elem.options.size + "px"
          })
          //Initializing jQuery easyPieChart plugin and passing the options
          
          setTimeout(function() {
          new Waypoint({
            element: elem,
            handler: function () {
              elem.easyPieChart({
                barColor: elem.options.barColor,
                trackColor: elem.options.trackColor,
                scaleColor: elem.options.scaleColor,
                scaleLength: elem.options.scaleLength,
                lineCap: elem.options.lineCap,
                lineWidth: Number(elem.options.lineWidth),
                size: Number(elem.options.size),
                rotate: Number(elem.options.rotate),
                animate: Number(elem.options.animate),
                elemEasing: elem.options.elemEasing,
                onStep: function (from, to, percent) {
                  elem.find("span.percent").text(Math.round(percent))
                }
              })
              this.destroy()
            },
            offset: "100%"
          })
        }, 200);
        })
      }
    },
    maps: function () {
      var $map = $(".map")

      if ($map.length > 0) {
        //Check if gMap plugin is loaded
        if (typeof $.fn.gmap3 === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery gmap3 plugin is missing, please go to this <a href='//support.inspirothemes.com/help-center/articles/8/14/65/google-maps'>help article</a> and follow instructions on how to configure google maps.", "danger")
          return true
        }
        $map.each(function () {
          var elem = $(this)
          //Plugin Options
          elem.options = {
            latitude: elem.attr("data-latitude") || "-37.817240",
            longitude: elem.attr("data-longitude") || "144.955820",
            info: elem.attr("data-info"),
            maptype: elem.attr("data-type") || "ROADMAP",
            zoom: elem.attr("data-zoom") || 14,
            fullscreen: elem.data("fullscreen") == false ? false : true,
            icon: elem.attr("data-icon"),
            mapColor: elem.attr("data-style") || null
          }
          var mapsStyle
          if (window.MAPS) {
            if (elem.options.mapColor) {
              mapsStyle = MAPS[elem.options.mapColor]
            } else {
              mapsStyle = null
            }
          }
          //Initialize google maps plugin and passing the options
          elem.gmap3({
            center: [Number(elem.options.latitude), Number(elem.options.longitude)],
            zoom: Number(elem.options.zoom),
            mapTypeId: google.maps.MapTypeId[elem.options.maptype],
            scrollwheel: false,
            zoomControl: true,
            mapTypeControl: false,
            streetViewControl: true,
            fullscreenControl: elem.options.fullscreen,
            styles: mapsStyle
          })
          if (elem.options.icon) {
            elem.gmap3().marker({
              position: [Number(elem.options.latitude), Number(elem.options.longitude)],
              icon: elem.options.icon
            })
          } else {
            elem
              .gmap3()
              .marker({
                position: [Number(elem.options.latitude), Number(elem.options.longitude)],
                icon: " "
              })
              .overlay({
                position: [Number(elem.options.latitude), Number(elem.options.longitude)],
                content: '<div class="animated-dot"></div>'
              })
          }
          if (elem.options.info) {
            elem
              .gmap3()
              .infowindow({
                position: [Number(elem.options.latitude), Number(elem.options.longitude)],
                content: elem.options.info,
                pixelOffset: new google.maps.Size(0, -10)
              })
              .then(function (infowindow) {
                var map = this.get(0)
                var marker = this.get(1)
                marker.addListener("click", function () {
                  infowindow.open(map)
                })
              })
          }
        })
      }
    },
    gridLayout: function () {
      if ($gridLayout.length > 0) {
        //Check if isotope plugin is loaded
        if (typeof $.fn.isotope === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery isotope plugin is missing in plugins.js file.", "danger")
          return true
        }

        var isotopeRTL;

        if (INSPIRO.core.rtlStatus() == true) {
          isotopeRTL = false;
        } else {
          isotopeRTL = true;
        }

        $gridLayout.each(function () {
          var elem = $(this)
          elem.options = {
            itemSelector: elem.attr("data-item") || "portfolio-item",
            layoutMode: elem.attr("data-layout") || "masonry",
            filter: elem.attr("data-default-filter") || "*",
            stagger: elem.attr("data-stagger") || 0,
            autoHeight: elem.data("auto-height") == false ? false : true,
            gridMargin: elem.attr("data-margin") || 20,
            gridMarginXs: elem.attr("data-margin-xs"),
            transitionDuration: elem.attr("data-transition") || "0.45s",
            isOriginLeft: isotopeRTL
          }

          $(window).breakpoints("lessThan", "lg", function () {
            elem.options.gridMargin = elem.options.gridMarginXs || elem.options.gridMargin
          })

          elem.css("margin", "0 -" + elem.options.gridMargin + "px -" + elem.options.gridMargin + "px 0")
          elem.find("." + elem.options.itemSelector).css("padding", "0 " + elem.options.gridMargin + "px " + elem.options.gridMargin + "px 0")
          if (elem.attr("data-default-filter")) {
            var elemDefaultFilter = elem.options.filter
            elem.options.filter = "." + elem.options.filter
          }
          elem.append('<div class="grid-loader"></div>');
          var $isotopelayout = $(elem).imagesLoaded(function () {
            // init Isotope after all images have loaded
            $isotopelayout.isotope({
              layoutMode: elem.options.layoutMode,
              transitionDuration: elem.options.transitionDuration,
              stagger: Number(elem.options.stagger),
              resize: true,
              itemSelector: "." + elem.options.itemSelector + ":not(.grid-loader)",
              isOriginLeft: elem.options.isOriginLeft,
              autoHeight: elem.options.autoHeight,
              masonry: {
                columnWidth: elem.find("." + elem.options.itemSelector + ":not(.large-width)")[0]
              },
              filter: elem.options.filter
            })
            elem.remove(".grid-loader").addClass("grid-loaded");
          })

          //Infinity Scroll
          if (elem.next().hasClass("infinite-scroll")) {
            INSPIRO.elements.gridLayoutInfinite(elem, elem.options.itemSelector, elem.options.gridMargin)
          }
          if ($gridFilter.length > 0) {
            $gridFilter.each(function () {
              var elemFilter = $(this),
                $filterItem = elemFilter.find("a"),
                elemFilterLayout = elemFilter.attr("data-layout"),
                $filterItemActiveClass = "active"
              $filterItem.on("click", function () {
                elemFilter.find("li").removeClass($filterItemActiveClass);
                $(this).parent("li").addClass($filterItemActiveClass);

                var filterValue = $(this).attr("data-category");
                $(elemFilterLayout).isotope({
                  filter: filterValue
                }).on("layoutComplete", function () {
                  $window.trigger("scroll");
                  INSPIRO.elements.naTo();
                })
                if ($(".grid-active-title").length > 0) {
                  $(".grid-active-title")
                    .empty()
                    .append($(this).text())
                }
                return false
              })
              if (elemDefaultFilter) {
                var filterDefaultValue = elemFilter.find($('[data-category="' + elem.options.filter + '"]'))
                elemFilter.find("li").removeClass($filterItemActiveClass)
                filterDefaultValue.parent("li").addClass($filterItemActiveClass)
              } else {
                var filterDefaultValue = elemFilter.find($('[data-category="*"]'))
                filterDefaultValue.parent("li").addClass($filterItemActiveClass)
              }
            })
          }
        })
      }
    },
    gridLayoutInfinite: function (element, elementSelector, elemGridMargin) {

      //Check if infiniteScroll plugin is loaded
      if (typeof $.fn.infiniteScroll === 'undefined') {
        INSPIRO.elements.notification("Warning", "jQuery infiniteScroll plugin is missing, please add this code line <b> &lt;script src=&quot;plugins/metafizzy/infinite-scroll.min.js&quot;&gt;&lt;/script&gt;</b>, before <b>plugins.js</b>", "danger");
        return true;
      }
      var elem = element,
        gridItem = elementSelector,
        gridMargin = elemGridMargin,
        loadOnScroll = true,
        threshold = 500,
        prefilli = true,
        pathSelector,
        loadMoreElem = $("#showMore"),
        loadMoreBtn = $("#showMore a.btn"),
        loadMoreBtnText = $("#showMore a.btn").html(),
        loadMoreMessage = $(
          '<div class="infinite-scroll-message"><p class="animated visible fadeIn">No more posts to show</p></div>'
        );

      pathSelector = $(".infinite-scroll > a").attr("href");

      if (pathSelector.indexOf(".html") > -1) {
        pathSelector = pathSelector.replace(/(-\d+)/g, "-{{#}}");
      } else {
        pathSelector = ".infinite-scroll > a";
      }

      if (loadMoreElem.length > 0) {
        loadOnScroll = false;
        threshold = false;
        prefilli = false;
      }

      elem.infiniteScroll({
        path: pathSelector,
        append: '.' + gridItem,
        history: false,
        button: '#showMore a',
        scrollThreshold: threshold,
        loadOnScroll: loadOnScroll,
        prefill: prefilli,
      });

      elem.on('load.infiniteScroll', function (event, response, path, items) {
        var $items = $(response).find('.' + gridItem);
        $items.imagesLoaded(function () {
          elem.append($items);
          elem.isotope('insert', $items);
        });
      });

      elem.on('error.infiniteScroll', function (event, error, path) {
        loadMoreElem.addClass("animated visible fadeOut");
        var t = setTimeout(function () {
          loadMoreElem.hide();
          elem.after(loadMoreMessage);
        }, 500);
        var t = setTimeout(function () {
          $(".infinite-scroll-message").addClass("animated visible fadeOut");
        }, 3000);
      });
      elem.on('append.infiniteScroll', function (event, response, path, items) {
        INSPIRO.slider.carousel($(items).find('.carousel'));
        loadMoreBtn.html(loadMoreBtnText);
        element.css("margin", "0 -" + gridMargin + "px -" + gridMargin + "px 0");
        element.find('.' + gridItem).css("padding", "0 " + gridMargin + "px " + gridMargin + "px 0");
      });
    },

    tooltip: function () {
      var $tooltip = $('[data-toggle="tooltip"]')
      if ($tooltip.length > 0) {
        //Check if tooltip plugin is loaded
        if (typeof $.fn.tooltip === "undefined") {
          INSPIRO.elements.notification("Warning: jQuery tooltip plugin is missing in plugins.js file.", "warning")
          return true
        }
        //Initialize Tooltip plugin function
        $tooltip.tooltip()
      }
    },
    popover: function () {
      var $popover = $('[data-toggle="popover"]')
      if ($popover.length > 0) {
        //Check if popover plugin is loaded
        if (typeof $.fn.popover === "undefined") {
          INSPIRO.elements.notification("Warning: jQuery popover plugin is missing in plugins.js file.", "warning")
          return true
        }
        //Initialize Tooltip plugin function
        $popover.popover({
          container: "body",
          html: true
        })
      }
    },

    magnificPopup: function () {
      var $lightbox = $("[data-lightbox]")
      if ($lightbox.length > 0) {
        //Check if magnificPopup plugin is loaded
        if (typeof $.fn.magnificPopup === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery magnificPopup plugin is missing in plugins.js file.", "danger")
          return true
        }
        //Get lightbox data type
        var getType = {
          image: {
            type: "image",
            closeOnContentClick: true,
            removalDelay: 500,
            image: {
              verticalFit: true
            },
            callbacks: {
              beforeOpen: function () {
                this.st.image.markup = this.st.image.markup.replace("mfp-figure", "mfp-figure mfp-with-anim")
                this.st.mainClass = "mfp-zoom-out"
              }
            }
          },
          gallery: {
            delegate: 'a[data-lightbox="gallery-image"], a[data-lightbox="image"]',
            type: "image",
            image: {
              verticalFit: true
            },
            gallery: {
              enabled: true,
              navigateByImgClick: true,
              preload: [0, 1]
            },
            removalDelay: 500,
            callbacks: {
              beforeOpen: function () {
                this.st.image.markup = this.st.image.markup.replace("mfp-figure", "mfp-figure mfp-with-anim")
                this.st.mainClass = "mfp-zoom-out"
              }
            }
          },
          iframe: {
            type: "iframe",
            removalDelay: 500,
            callbacks: {
              beforeOpen: function () {
                this.st.image.markup = this.st.image.markup.replace("mfp-figure", "mfp-figure mfp-with-anim")
                this.st.mainClass = "mfp-zoom-out"
              }
            }
          },
          ajax: {
            type: "ajax",
            removalDelay: 500,
            callbacks: {
              ajaxContentAdded: function (mfpResponse) {
                INSPIRO.elements.functions();
                INSPIRO.slider.carouselAjax();
              }
            }
          },
          inline: {
            type: "inline",
            removalDelay: 500,
            closeBtnInside: true,
            midClick: true,
            callbacks: {
              beforeOpen: function () {
                this.st.image.markup = this.st.image.markup.replace("mfp-figure", "mfp-figure mfp-with-anim")
                this.st.mainClass = "mfp-zoom-out"
              },
              open: function () {
                  if ($(this.content).find("video").length > 0) {
                    $(this.content).find("video").get(0).play();
                  }
              },
              close: function () {
                 if ($(this.content).find("video").length > 0) {
                  $(this.content).find("video").get(0).load();
                }
              }           
            },
            fixedContentPos: true,
            overflowY: "scroll"
          }
        }
        //Initializing jQuery magnificPopup plugin and passing the options
        $lightbox.each(function () {
          var elem = $(this),
            elemType = elem.attr("data-lightbox")
          switch (elemType) {
            case "image":
              elem.magnificPopup(getType.image)
              break
            case "gallery":
              elem.magnificPopup(getType.gallery)
              break
            case "iframe":
              elem.magnificPopup(getType.iframe)
              break
            case "ajax":
              elem.magnificPopup(getType.ajax)
              break
            case "inline":
              elem.magnificPopup(getType.inline)
              break
          }
        })
      }
    },
    yTPlayer: function () {
      var $ytPlayer = $(".youtube-background")
      if ($ytPlayer.length > 0) {
        //Check if YTPlayer plugin is loaded
        if (typeof $.fn.YTPlayer === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery YTPlayer plugin is missing, please add this code line <b> &lt;script src=&quot;plugins/youtube-player/jquery.mb.YTPlayer.min.js&quot;&gt;&lt;/script&gt;</b>, before <b><--Template functions--></b>", "danger", 10000)
          return true
        }
        $ytPlayer.each(function () {
          var elem = $(this)
          //Plugin Options
          elem.options = {
            videoURL: elem.attr("data-youtube-url"),
            autoPlay: elem.data("youtube-autoplay") == false ? 0 : 1,
            mute: elem.data("youtube-mute") == false ? false : true,
            pauseOnScroll: elem.data("youtube-pauseOnScroll") == false ? false : true,
            loop: elem.data("youtube-loop") == false ? false : true,
            vol: elem.attr("data-youtube-volume") || 50,
            startAt: elem.attr("data-youtube-start") || 0,
            stopAt: elem.attr("data-youtube-stop") || 0,
            controls: elem.data("youtube-controls") == true ? 1 : 0
          }
          var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/
          var match = elem.options.videoURL.match(regExp)
          if (match && match[2].length == 11) {
            elem.options.videoURL = match[2]
          } else {
            elem.options.videoURL = elem.options.videoURL
          }
          elem.YTPlayer({
            fitToBackground: true,
            videoId: elem.options.videoURL,
            repeat: elem.options.loop,
            playerVars: {
              start: elem.options.start,
              end: elem.options.end,
              autoplay: elem.options.autoPlay,
              modestbranding: elem.options.logo,
              controls: elem.options.controls,
              origin: window.location.origin,
              branding: 0,
              rel: 0,
              showinfo: 0
            },
            events: {
              onReady: onPlayerReady
            }
          })

          function onPlayerReady(event) {
            if (elem.options.vol) {
              event.target.setVolume(elem.options.vol)
            }
            if (elem.options.mute) {
              event.target.mute()
            }
            if (elem.options.pauseOnScroll) {
              var waypoint = new Waypoint({
                element: elem,
                handler: function (direction) {
                  event.target.pauseVideo()
                  if (elem.options.autoPlay == true && direction == "up") {
                    event.target.playVideo()
                  }
                }
              })
            }
          }
        })
      }
    },
    vimeoPlayer: function () {
      var $vmPlayer = $(".vimeo-background")
      if ($vmPlayer.length > 0) {
        //Check if vimeo_player plugin is loaded
        if (typeof $.fn.vimeo_player === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery vimeo_player plugin is missing, please add this code line <b> &lt;script src=&quot;plugins/vimeo-player/jquery.mb.vimeo_player.min.js&quot;&gt;&lt;/script&gt;</b>, before <b><--Template functions--></b>", "danger", 10000)
          return true
        }
        $vmPlayer.each(function () {
          var elem = $(this),
            elemVideo = elem.attr("data-vimeo-url") || null,
            elemMute = elem.attr("data-vimeo-mute") || false,
            elemRatio = elem.attr("data-vimeo-ratio") || "16/9",
            elemQuality = elem.attr("data-vimeo-quality") || "hd720",
            elemOpacity = elem.attr("data-vimeo-opacity") || 1,
            elemContainer = elem.attr("data-vimeo-container") || "self",
            elemOptimize = elem.attr("data-vimeo-optimize") || true,
            elemLoop = elem.attr("data-vimeo-loop") || true,
            elemVolume = elem.attr("data-vimeo-volume") || 70,
            elemStart = elem.attr("data-vimeo-start") || 0,
            elemStop = elem.attr("data-vimeo-stop") || 0,
            elemAutoPlay = elem.attr("data-vimeo-autoplay") || true,
            elemFullScreen = elem.attr("data-vimeo-fullscreen") || true,
            elemControls = elem.attr("data-vimeo-controls") || false,
            elemLogo = elem.attr("data-vimeo-logo") || false,
            elemAutoPause = elem.attr("data-vimeo-autopause") || false
          elem.vimeo_player({
            videoURL: elemVideo,
            mute: elemMute,
            ratio: elemRatio,
            quality: elemQuality,
            opacity: elemOpacity,
            containment: elemContainer,
            optimizeDisplay: elemOptimize,
            loop: elemLoop,
            vol: elemVolume,
            startAt: elemStart,
            stopAt: elemStop,
            autoPlay: elemAutoPlay,
            realfullscreen: elemFullScreen,
            showvmLogo: elemLogo,
            showControls: elemControls
          })
        })
      }
    },
    modal: function () {
      //Check if magnificPopup plugin is loaded
      if (typeof $.fn.magnificPopup === "undefined") {
        INSPIRO.elements.notification("Warning", "jQuery magnificPopup plugin is missing in plugins.js file.", "danger")
        return true
      }
      var $modal = $(".modal"),
        $modalStrip = $(".modal-strip"),
        $btnModal = $(".btn-modal"),
        modalShow = "modal-auto-open",
        modalShowClass = "modal-active",
        modalDecline = $(".modal-close"),
        cookieNotify = $(".cookie-notify"),
        cookieConfirm = cookieNotify.find(".modal-confirm, .mfp-close");

      /*Modal*/
      if ($modal.length > 0) {
        $modal.each(function () {
          var elem = $(this),
            elemDelay = elem.attr("data-delay") || 3000,
            elemCookieExpire = elem.attr("data-cookie-expire") || 365,
            elemCookieName = elem.attr("data-cookie-name") || "cookieModalName2020_3",
            elemCookieEnabled = elem.data("cookie-enabled") == true ? true : false,
            elemModalDismissDelay = elem.attr("data-delay-dismiss")
          /*Modal Auto Show*/
          if (elem.hasClass(modalShow)) {
            var modalElem = $(this)
            var timeout = setTimeout(function () {
              modalElem.addClass(modalShowClass)
            }, elemDelay)
          }
          /*Modal Dissmis Button*/
          elem.find(modalDecline).click(function () {
            elem.removeClass(modalShowClass)
            return false
          });
          /*Modal Auto Show*/
          if (elem.hasClass(modalShow)) {
            if (elemCookieEnabled != true) {
              /*Cookie Notify*/
              var t = setTimeout(function () {
                $.magnificPopup.open({
                    items: {
                      src: elem
                    },
                    type: "inline",
                    closeBtnInside: true,
                    midClick: true,
                    callbacks: {
                      beforeOpen: function () {
                        this.st.image.markup = this.st.image.markup.replace("mfp-figure", "mfp-figure mfp-with-anim")
                        this.st.mainClass = "mfp-zoom-out"
                      },
                      open: function () {
                        if ($(this.content).find("video").length > 0) {
                          $(this.content).find("video").get(0).play();
                        }
                        
                    },
                    close: function () {
                       if ($(this.content).find("video").length > 0) {
                        $(this.content).find("video").get(0).load();
                      }
                    }
                    }
                  },
                  0
                )
              }, elemDelay)
            } else {
              if (typeof Cookies.get(elemCookieName) == "undefined") {
                /*Cookie Notify*/
                var t = setTimeout(function () {
                  $.magnificPopup.open({
                      items: {
                        src: elem
                      },
                      type: "inline",
                      closeBtnInside: true,
                      midClick: true,
                      callbacks: {
                        beforeOpen: function () {
                          this.st.image.markup = this.st.image.markup.replace("mfp-figure", "mfp-figure mfp-with-anim")
                          this.st.mainClass = "mfp-zoom-out"
                        },
                        open: function () {
                          if ($(this.content).find("video").length > 0) {
                            $(this.content).find("video").get(0).play();
                          }
                          cookieConfirm.click(function () {
                            Cookies.set(elemCookieName, true, {
                              expires: Number(elemCookieExpire)
                            })
                            $.magnificPopup.close();
                            cookieNotify.removeClass(modalShowClass);
                            return false
                          });
                      },
                        close: function () {
                          if ($(this.content).find("video").length > 0) {
                            $(this.content).find("video").get(0).load();
                          };

                          Cookies.set(elemCookieName, true, {
                            expires: Number(elemCookieExpire)
                          })
                        }
                      }
                    },
                    0
                  )
                }, elemDelay)
              }
            }
          }
          /*Modal Dissmis Button*/
          elem.find(modalDecline).click(function () {
            $.magnificPopup.close()
            return false
          })

          if (elemModalDismissDelay) {}
        })
      }
      /*Modal Strip*/
      if ($modalStrip.length > 0) {
        $modalStrip.each(function () {
          var elem = $(this),
            elemDelay = elem.attr("data-delay") || 3000,
            elemCookieExpire = elem.attr("data-cookie-expire") || 365,
            elemCookieName = elem.attr("data-cookie-name") || "cookieName2013",
            elemCookieEnabled = elem.data("cookie-enabled") == true ? true : false,
            elemModalDismissDelay = elem.attr("data-delay-dismiss")
          /*Modal Auto Show*/
          if (elem.hasClass(modalShow)) {
            var modalElem = $(this)
            var timeout = setTimeout(function () {
              modalElem.addClass(modalShowClass)
              if (elemModalDismissDelay) {
                var t = setTimeout(function () {
                  elem.removeClass(modalShowClass)
                }, elemModalDismissDelay)
              }
            }, elemDelay)
          }
          /*Modal Dissmis Button*/
          elem.find(modalDecline).click(function () {
            elem.removeClass(modalShowClass)
            return false
          })
          /*Cookie Notify*/
          if (elem.hasClass("cookie-notify")) {
            var timeout = setTimeout(function () {
              if (elemCookieEnabled != true) {
                cookieNotify.addClass(modalShowClass)
              } else {
                if (typeof Cookies.get(elemCookieName) == "undefined") {
                  cookieNotify.addClass(modalShowClass)
                }
              }
            }, elemDelay)
            cookieConfirm.click(function () {
              Cookies.set(elemCookieName, true, {
                expires: Number(elemCookieExpire)
              })
              $.magnificPopup.close()
              cookieNotify.removeClass(modalShowClass)
              return false
            })
          }
        })
      }
      /*Modal toggles*/
      if ($btnModal.length > 0) {
        $btnModal.each(function () {
          var elem = $(this),
            modalTarget = elem.attr("data-modal")
          elem.click(function () {
            $(modalTarget).toggleClass(modalShowClass, 1000)
            return false
          })
        })
      }
    },
    notification: function ($title, $message, $type, $element, $delay, $placement, $animateEnter, $animateExit, $backgroundImage, $timeout) {
      var $element,
        $elementContainer,
        $animateEnter = $animateEnter || "fadeInDown",
        $animateExit = $animateExit || "fadeOutDown",
        $placement,
        $backgroundImage,
        $backgroundImageContainer,
        $timeout

      if ($placement) {
        $placement = $placement
      } else {
        $placement = "top"
      }

      if ($element) {
        $elementContainer = "element-container";
        ($animateEnter = "fadeIn"), ($animateExit = "fadeOut")
      } else {
        $elementContainer = "col-11 col-md-4"
      }

      if ($backgroundImage) {
        $backgroundImageContainer = 'style="background-image:url(' + $backgroundImage + '); background-repeat: no-repeat; background-position: 50% 20%; height:120px !important; width:430px !important; border:0px;" '
      }

      if (!$message) {
        $message = ""
      }

      $element = "body"

      var notify = function () {
        $.notify({
          title: $title,
          message: $message
        }, {
          element: $element,
          type: $type || "warning",
          delay: $delay || 10000,
          template: '<div data-notify="container" ' + $backgroundImageContainer + ' class="bootstrap-notify ' + $elementContainer + ' alert alert-{0}" role="alert">' + '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' + '<span data-notify="icon"></span> ' + '<span data-notify="title">{1}</span> ' + '<span data-notify="message">{2}</span>' + "</div>",
          mouse_over: true,
          allow_dismiss: true,
          placement: {
            from: $placement
          },
          animate: {
            enter: "animated " + $animateEnter,
            exit: "animated " + $animateExit
          }
        })
      }

      if ($timeout) {
        setTimeout(function () {
          notify()
        }, 2000)
      } else {
        notify()
      }
    },
    sidebarFixed: function () {
      if (INSPIRO.core.rtlStatus()) {
        return true
      }
      var $sidebarFixed = $(".sticky-sidebar")
      if ($sidebarFixed.length > 0) {
        //Check if theiaStickySidebar plugin is loaded
        if (typeof $.fn.theiaStickySidebar === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery theiaStickySidebar plugin is missing in plugins.js file.", "danger")
          return true
        }
        $sidebarFixed.each(function () {
          var elem = $(this)
          elem.options = {
            additionalMarginTop: elem.attr("data-margin-top") || 120,
            additionalMarginBottom: elem.attr("data-margin-bottom") || 50
          }
          //Initialize theiaStickySidebar plugin and passing the options
          elem.theiaStickySidebar({
            additionalMarginTop: Number(elem.options.additionalMarginTop),
            additionalMarginBottom: Number(elem.options.additionalMarginBottom),
            disableOnResponsiveLayouts: true
          })
        })
      }
    },
    bootstrapSwitch: function () {
      var $bootstrapSwitch = $("[data-switch=true]")
      if ($bootstrapSwitch.length > 0) {
        //Check if bootstrapSwitch plugin is loaded
        if (typeof $.fn.bootstrapSwitch === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery bootstrapSwitch plugin is missing in plugins.js file.", "danger")
          return true
        }
        //Initialize jQuery BootstrapSwitch plugin
        $bootstrapSwitch.bootstrapSwitch()
      }
    },
    clipboard: function () {
      var $clipboardTarget = $("[data-clipboard-target]"),
        $clipboardText = $("[data-clipboard-text]")
      if ($clipboardTarget.length > 0) {
        //Check if ClipboardJS plugin is loaded
        if (typeof ClipboardJS === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery ClipboardJS plugin is missing in plugins.js file.", "danger")
          return true
        }
        if ($clipboardTarget) {
          new ClipboardJS("[data-clipboard-target]")
          clipboardInit($clipboardTarget)
        }
        if ($clipboardText) {
          new ClipboardJS("[data-clipboard-text]")
          clipboardInit($clipboardText)
        }

        function clipboardInit(clipboardType) {
          clipboardType.each(function () {
            var elem = $(this),
              title = elem.attr("data-original-title") || "Copy to clipboard",
              titleSuccess = elem.attr("data-original-title-success") || "Copied!"
            elem.tooltip({
              placement: "top",
              title: title
            })
            elem
              .on("click", function () {
                elem.attr("data-original-title", titleSuccess).tooltip("show")
              })
              .on("mouseleave", function () {
                elem.tooltip("hide").attr("data-original-title", title)
                return false
              })
          })
        }
      }
    },
    countdown: function () {
      var $countdown = $(".p-countdown")
      if ($countdown.length > 0) {
        $countdown.each(function () {
          var $elem = $(this),
            $elemCount = $elem.find(".p-countdown-count"),
            $elemShow = $elem.find(".p-countdown-show"),
            $elemSeconds = $elem.attr("data-delay") || 5
          $elemCount.find(".count-number").html($elemSeconds)
          new Waypoint({
            element: $elem,
            handler: function () {
              var interval = setInterval(function () {
                $elemSeconds--
                if ($elemSeconds == 0) {
                  clearInterval(interval)
                  $elemCount.fadeOut("slow")
                  setTimeout(function () {
                    $elemShow.fadeIn("show")
                  }, 1000)
                } else {
                  $elemCount.find(".count-number").html($elemSeconds)
                }
              }, 1000)
              this.destroy()
            },
            offset: "100%"
          })
        })
      }
    },
    videoBackground: function () {
      var $videoBackground = $("[data-bg-video]");
      if ($videoBackground.length > 0) {
        $videoBackground.each(function () {
          var elem = $(this);
          elem.options = {
            autoplay: elem.data("autoplay") == false ? false : true,
            controls: elem.attr("data-controls"),
            loop: elem.data("loop") == true ? true : false,
            muted: elem.data("muted") == false ? false : true,
            poster: elem.attr("data-poster") || "",
            preload: elem.attr("data-preload") || "auto",
            src: elem.attr("data-bg-video"),
            randomId: Math.random().toString(36).substr(2, 5)
          }

          if (elem.options.controls) {
            elem.options.controls = ' controls="' + elem.options.controls + '" '
          } else {
            elem.options.controls = ""
          }
          elem.prepend('<div class="html5vid" id="video-' + elem.options.randomId + '">' + "<video playsinline " + elem.options.controls + ' loop="' + elem.options.loop + '" muted="' + elem.options.muted + '" poster="' + elem.options.poster + '" preload="' + elem.options.preload + '">' + '<source src="' + elem.options.src + '" type="video/mp4">' + "</video>" + "</div>")
          if (elem.options.autoplay) {
            setTimeout(function () {

              $("#video-" + elem.options.randomId).waypoint(function (direction) {

                if (direction === "down") {
                  $("#video-" + elem.options.randomId).find("video").get(0).play();
                } else {
                  $("#video-" + elem.options.randomId).find("video").get(0).pause();
                }
              }, {
                offset: '50%',
              });
            }, 100);
          }
          setTimeout(function () {
            $("#video-" + elem.options.randomId).addClass("video-loaded");
          }, 300)
        })
      }
    }
  }
  INSPIRO.widgets = {
    functions: function () {
      INSPIRO.widgets.twitter()
      INSPIRO.widgets.flickr()
      INSPIRO.widgets.instagram()
      INSPIRO.widgets.subscribeForm()
    },
    twitter: function () {
      var $widget_twitter = $(".widget-tweeter") || $(".widget-twitter")
      if ($widget_twitter.length > 0) {
        //Check if twittie plugin is loaded
        if (typeof $.fn.twittie === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery twittie plugin is missing in plugins.js file.", "danger")
          return true
        }
        var t = setTimeout(function () {
          $widget_twitter.each(function () {
            var elem = $(this),
              twitterUsername = elem.attr("data-username") || "ardianmusliu",
              twitterLimit = elem.attr("data-limit") || 2,
              twitterDateFormat = elem.attr("data-format") || "%b/%d/%Y",
              twitterLoadingText = elem.attr("data-loading-text") || "Loading...",
              twitterApiPAth = elem.attr("data-loader") || "include/twitter/tweet.php",
              twitterAvatar = elem.attr("data-avatar") || false
            if (twitterAvatar == "true") {
              twitterAvatar = "{{avatar}}"
            } else {
              twitterAvatar = ""
            }
            elem.append('<div id="twitter-cnt"></div>');
            elem.find("#twitter-cnt").twittie({
                username: twitterUsername,
                count: twitterLimit,
                dateFormat: twitterDateFormat,
                template: twitterAvatar + "{{tweet}}<small>{{date}}</small>",
                apiPath: twitterApiPAth,
                loadingText: twitterLoadingText
              },
              function () {
                if (elem.parents(".grid-layout").length > 0) {
                  elem.parents(".grid-layout").isotope("layout")
                }
              }
            )
          })
        }, 2000)
      }
    },
    flickr: function () {
      var $flickr_widget = $(".flickr-widget");
      if ($flickr_widget.length > 0) {
        //Check if jflickrfeed plugin is loaded
        if (typeof $.fn.jflickrfeed === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery jflickrfeed plugin is missing in plugins.js file.", "danger")
          return true
        }
        $flickr_widget.each(function () {
          var elem = $(this)
          elem.options = {
            id: elem.attr("data-flickr-id") || "52617155@N08",
            limit: elem.attr("data-flickr-images") || "9",
            itemTemplate: '<a href="{{image}}" title="{{title}}"><img src="{{image_s}}" alt="{{title}}" /></a>'
          }
          //Initializing jflickrfeed plugin and passing the options
          $flickr_widget.jflickrfeed({
              limit: elem.options.limit,
              qstrings: {
                id: elem.options.id
              },
              itemTemplate: elem.options.itemTemplate
            },
            function () {
              var t = setTimeout(function () {
                elem.addClass("flickr-widget-loaded");
              }, 1000);
              elem.magnificPopup({
                  delegate: "a",
                  type: "image",
                  gallery: {
                    enabled: true
                  }
                },
                function () {
                  if (elem.parents(".grid-layout").length > 0) {
                    elem.parents(".grid-layout").isotope("layout")
                  }
                });
            }
          )
        })
      }
    },
    instagram: function () {
      var $widget_instagram = $(".widget-instagram");
      if ($widget_instagram.length > 0) {
        //Check if spectragram plugin is loaded
        if (typeof $.fn.spectragram === "undefined") {
          INSPIRO.elements.notification("Warning", "jQuery spectragram plugin is missing in plugins.js file.", "danger");
          return true;
        }

        $widget_instagram.each(function () {
          var elem = $(this),
            instagramLimit = elem.attr("data-limit") || 12,
            instagramColumns = elem.attr("data-col") || 3,
            instagramAccessToken = elem.attr("data-token") || "IGQVJYMjdIb3lOZAlBpTDZApY1lOakNVTk1xWVdWVk42Y0RWMFNDSUE4TDRad3M5d2JNZAUZAiLXBhY0ZAfWVZAYUEctMDF0R1QwZA2lTalRQWC1kMi1zd2pQc3U0V3lkMEE0Tk8wZAUlzQW55d3h3THFjRU94TgZDZD",
            instagramItems = "#instagram-cnt",
            instagramSize = elem.attr("data-size") || "small", //The size of the photos. 'small', 'medium' or 'big'. Default: 'medium'
            instagramGridColumns = "grid-" + instagramColumns
          elem.append('<div id="instagram-cnt" class="' + instagramGridColumns + '"></div>');

          jQuery.fn.spectragram.accessData = {
            accessToken: instagramAccessToken
          };
          
          elem.find($(instagramItems)).spectragram({
            complete : myCallbackFunc(),
            max: instagramLimit,
            size: instagramSize,
            wrapEachWith: "",
          });

          function myCallbackFunc(){
            elem.addClass("widget-instagram-loaded")
              setTimeout(function () {
                if (elem.parents(".grid-layout").length > 0) {
                  elem.parents(".grid-layout").isotope("layout")
                }
              }, 100);
          }
      });
      }
    },
    subscribeForm: function () {
      var $subscribeForm = $(".widget-subscribe-form")
      if ($subscribeForm.length > 0) {
        $subscribeForm.each(function () {
          var elem = $(this),
            elemSuccessMessage = elem.attr("data-success-message") || "You have successfully subscribed to our mailing list."
          var addonIcon = elem.find("#widget-subscribe-submit-button"),
            addonIconText = addonIcon.html()
          elem.submit(function (event) {
            event.preventDefault()
            var post_url = $(this).attr("action")
            var request_method = $(this).attr("method")
            var form_data = $(this).serialize()
            if (elem[0].checkValidity() === false) {
              event.stopPropagation()
              elem.addClass("was-validated")
            } else {
              $(elem).removeClass("was-validated")
              addonIcon.html('<i class="icon-loader fa-spin"></i>')
              $.ajax({
                url: post_url,
                type: request_method,
                data: form_data,
                dataType: "json",
                success: function (text) {
                  if (text.response == "success") {
                    $.notify({
                      message: elemSuccessMessage
                    }, {
                      type: "success"
                    })
                    $(elem)[0].reset()
                    $(elem).removeClass("was-validated")
                    addonIcon.html(addonIconText)
                  } else {
                    $.notify({
                      message: text.message
                    }, {
                      type: "warning"
                    })
                    $(elem)[0].reset()
                    $(elem).removeClass("was-validated")
                    addonIcon.html(addonIconText)
                  }
                },
                done: function () {
                  addonIcon.html(addonIconText)
                }
              })
            }
          })
        })
      }
    }
  }
  //Load Functions on document ready
  $(document).ready(function () {
    INSPIRO.core.functions();
    INSPIRO.header.functions();
    INSPIRO.slider.functions();
    INSPIRO.widgets.functions();
    INSPIRO.elements.functions();
  })
  //Recall Functions on window scroll
  $window.on("scroll", function () {
    INSPIRO.header.stickyHeader();
    INSPIRO.core.scrollTop();
    INSPIRO.header.dotsMenu();
  })
  //Recall Functions on window resize
  $window.on("resize", function () {
    INSPIRO.header.logoStatus();
    INSPIRO.header.stickyHeader();
  })
})(jQuery)