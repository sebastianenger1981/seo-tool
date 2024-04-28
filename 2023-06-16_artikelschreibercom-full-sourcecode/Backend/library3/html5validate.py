#!/usr/bin/env python3
"""
    html5validate
    ------
    HTML5Lib based HTML5 validation module.
    MIT Licence - (C) 2019 Daniel Fairhead

"""

import warnings
from collections import namedtuple
import re
from xml.dom import Node

import html5lib

# in case we do need to track elements, here are some objects to hold them in:
DocType = namedtuple('DocType', ('name', 'publicId', 'systemId'))
StartTag = namedtuple('StartTag', ('name', 'attributes'))
VoidTag = namedtuple('VoidTag', ('name', 'attributes', 'has_children'))
EndTag = namedtuple('EndTag', ('name'))
Entity = namedtuple('Entity', ('name',))

SpaceCharacters = namedtuple('SpaceCharacters', ('data'))
Characters = namedtuple('Characters', ('data'))
Comment = namedtuple('Comment', ('data'))

# Splits <whitespace><anything><whitespace> apart.
TEXT_MATCH = re.compile(r'(\s*)(\S?.*\S)(\s*)')

from html5lib.html5parser import ParseError

class HTML5Invalid(Exception):
    pass

#class ParseError(HTML5Invalid):
#    pass

#class LintError(HTML5Invalid):
#    pass

class ValidationException(HTML5Invalid):
    pass

class InvalidTag(ValidationException):
    pass

class EmptyPage(ValidationException):
    pass

class MisplacedElement(ValidationException):
    pass

class InvalidAttribute(ValidationException):
    pass

class NonSecureRequestInSecurePage(ValidationException):
    pass

class UnclosedTags(ValidationException):
    pass

# 8. Namespaces:

namespaces = {
        'html': 'http://www.w3.org/1999/xhtml',
        'mathml': "http://www.w3.org/1998/Math/MathML",
        'svg': "http://www.w3.org/2000/svg",
        'xlink': "http://www.w3.org/1999/xlink",
        'xml': "http://www.w3.org/XML/1998/namespace",
        'xmlns': "http://www.w3.org/2000/xmlns/",
        }

metadata_elements = frozenset(('base','link','meta','noscript','script','style','template','title'))

html_elements = {
    'html': ('',),
    'head': ('html',),
    'body': ('html',),
# 3.2.5.2.1 "Metadata content"
    'base': ("head",),
    'link': ("head", "body"),
    'meta': ("head", "body"),
    'noscript': ("head", "body"),
    'script': ("head", "body"),
    'style': ("head", "body"),
    'template': ("head", "body"),
    'title': ("head",),

# 3.2.5.2.2 "Flow content"
    "a": ("body",),
    "abbr": ("body",),
    "address": ("body",),
    "area": ("map",),
    "article": ("body",),
    "aside": ("body",),
    "audio": ("body",),
    "b": ("body",),
    "bdi": ("body",),
    "bdo": ("body",),
    "blockquote": ("body",),
    "br": ("body",),
    "button": ("body",),
    "canvas": ("body",),
    "cite": ("body",),
    "code": ("body",),
    "data": ("body",),
    "datalist": ("body",),
    "del": ("body",),
    "details": ("body",),
    "summary": ("details",), #4.11.2
    "dfn": ("body",),
    "dialog": ("body",),
    "div": ("body",),
    "dl": ("body",),
    "em": ("body",),
    "embed": ("body",),
    "fieldset": ("body",),
    "legend": ('fieldset',), #4.10.16
    "figure": ("body",),
    "figcaption": ("figure",), #4.4.13
    "footer": ("body",),
    "form": ("body",),
    "h1": ("body",),
    "h2": ("body",),
    "h3": ("body",),
    "h4": ("body",),
    "h5": ("body",),
    "h6": ("body",),
    "header": ("body",),
    "hgroup": ("body",),
    "hr": ("body",),
    "i": ("body",),
    "iframe": ("body",),
    "img": ("body",),
    "input": ("body",),
    "ins": ("body",),
    "kbd": ("body",),
    "label": ("body",),
    "li": ('ol', 'ul', 'menu'), # 4.4.8
    "main": ("body",),
    "map": ("body",),
    "mark": ("body",),
    "math": ("body",),
    "menu": ("body",),
    "meter": ("body",),
    "nav": ("body",),
    "object": ("body",),
    "param": ('object',), #4.8.8
    "ol": ("body",),
    "output": ("body",),
    "p": ("body",),
    "picture": ("body",),
    "pre": ("body",),
    "progress": ("body",),
    "q": ("body",),
    "ruby": ("body",),
    "rt": ('ruby',), #4.5.11
    "rp": ('ruby',), #4.5.12
    "s": ("body",),
    "samp": ("body",),
    "section": ("body",),
    "select": ("body",),
    "optgroup": ('select',), # 4.10.9
    "option": ('select', 'datalist', 'optgroup'), # 4.10.10
    "slot": ("body",),
    "small": ("body",),
    "source": ("video", "audio",), # embedded element
    "span": ("body",),
    "strong": ("body",),
    "sub": ("body",),
    "sup": ("body",),
    "svg": ("body",),
    "table": ("body",),
    "caption": ('table',), # 4.9.2
    "colgroup": ('table',), # 4.9.3
    "col": ('colgroup',), # 4.9.4
    "tbody": ('table',), # 4.9.5
    "thead": ('table',), # 4.9.6
    "tfoot": ('table',), # 4.9.7
    "tr": ('thead', 'tbody', 'tfoot', 'table'), # 4.9.8
    "td": ("tr",), # 4.9.9
    "th": ("tr",), # 4.9.10
    "dl": ('body',), #4.4.9
    "dt": ('dl',), # 4.4.10
    "dd": ('dl',), # 4.4.11
    "textarea": ("body",),
    "time": ("body",),
    "u": ("body",),
    "ul": ("body",),
    "var": ("body",),
    "video": ("body",),
    "wbr": ("body",),
    "track": ('video', 'audio'),
}

non_recursable = frozenset(('html', 'head', 'body','video','audio', 'noscript', 'form'))

# 12.1.2
void_elements = frozenset(('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'))

global_attributes = frozenset((
    # 3.2.6 - Can be for ANY
    "class",
    "id",
    "slot",
    # 3.2.6 - for HTML elements:
    "accesskey",
    "autocapitalize",
    "contenteditable",
    "dir",
    "draggable",
    "enterkeyhint",
    "hidden",
    "inputmode",
    "is",
    "itemid",
    "itemprop",
    "itemref",
    "itemscope",
    "itemtype",
    "lang",
    "nonce",
    "spellcheck",
    "tabindex",
    "title",
    "translate",
    # JS for any:
    "onabort",
    "onauxclick",
    "onblur",
    "oncancel",
    "oncanplay",
    "oncanplaythrough",
    "onchange",
    "onclick",
    "onclose",
    "oncontextmenu",
    "oncopy",
    "oncuechange",
    "oncut",
    "ondblclick",
    "ondrag",
    "ondragend",
    "ondragenter",
    "ondragexit",
    "ondragleave",
    "ondragover",
    "ondragstart",
    "ondrop",
    "ondurationchange",
    "onemptied",
    "onended",
    "onerror",
    "onfocus",
    "onformdata",
    "oninput",
    "oninvalid",
    "onkeydown",
    "onkeypress",
    "onkeyup",
    "onload",
    "onloadeddata",
    "onloadedmetadata",
    "onloadend",
    "onloadstart",
    "onmousedown",
    "onmouseenter",
    "onmouseleave",
    "onmousemove",
    "onmouseout",
    "onmouseover",
    "onmouseup",
    "onpaste",
    "onpause",
    "onplay",
    "onplaying",
    "onprogress",
    "onratechange",
    "onreset",
    "onresize",
    "onscroll",
    "onsecuritypolicyviolation",
    "onseeked",
    "onseeking",
    "onselect",
    "onstalled",
    "onsubmit",
    "onsuspend",
    "ontimeupdate",
    "ontoggle",
    "onvolumechange",
    "onwaiting",
    "onwheel",
    # ARIA
    'aria-describedby',
    'aria-disabled',
    'aria-label',
    'role',
    ))

# 15.1
element_attribute_warnings={
        'html':
            ('xmlns', 'xml:lang', 'prefix',),
        'script':
            ('charset', 'language',),
        'img':
            ('border',),
        'style':
            ('type',),
        'a':
            ('name',),
        }

element_attributes={
        'html': #4.1.1
            ('manifest',),
        'base': # 4.2.3
            ('href', 'target'),
        'canvas': # 4.12.5
            ('width', 'height'),
        'link': #4.2.4
            ('href', 'crossorigin', 'rel', 'media', 'integrity', 'hreflang',
                'type', 'referrerpolicy', 'sizes', 'imgsrcset', 'imagesizes',
                'as', 'color'),
        'meta': # 4.2.5
            ('name', 'http-equiv', 'content', 'charset'),
        'style': # 4.2.6
            ('media',),
        'q': # 4.5.7
            ('cite',),
        'img': # 4.8.3
            ('alt', 'src', 'srcset', 'sizes', 'crossorigin', 'usemap', 'ismap',
             'width', 'height', 'referrerpolicy', 'decoding'),
        'map':  #4.8.13
            ('name',),
        'area': # 4.8.14
            ('alt', 'coords', 'shape', 'href', 'target', 'download', 'ping',
             'rel','referrerpolicy'),
        'col': #4.9.3
            ('span',),
        'td': #4.9.9
            ('colspan', 'rowspan', 'headers'),
        'th': # 4.9.10
            ('colspan', 'rowspan', 'headers', 'scope', 'abbr'),
        'form': #4.10.3
            ('accept-charset', 'action', 'autocomplete', 'enctype', 'method',
             'name', 'novalidate', 'target', 'rel'),
        'label': #4.10.4
            ('for',),
        'input': #4.10.5
            ('accept', 'alt', 'autocomplete', 'autofocus', 'checked',
             'dirname', 'disabled', 'form', 'formaction', 'formenctype',
             'formmethod', 'formnovalidate', 'formtarget', 'height', 'list',
             'max', 'maxlength', 'min', 'minlength', 'multiple', 'name',
             'pattern', 'placeholder', 'readonly', 'required', 'size', 'src',
             'step', 'type', 'value', 'width'),
        'button': # 4.10.6
            ('autofocus', 'disabled', 'form', 'formaction', 'formenctype',
             'formmethod', 'formnovalidate', 'formtarget', 'name', 'type',
             'value'),
        'select': #4.10.7
            ('autocomplete', 'autofocus', 'disabled', 'form', 'multiple',
             'name', 'required', 'size'),
        'optgroup': #4.10.9
            ('disabled', 'label'),
        'option': #4.10.10
            ('disabled', 'label', 'selected', 'value'),
        'textarea': #4.10.11
            ('autocomplete', 'autofocus', 'cols', 'dirname', 'disabled', 'form',
             'maxlength', 'minlength', 'name', 'placeholder', 'readonly',
             'required', 'rows', 'wrap'),
        'output': #4.10.12
            ('for', 'form', 'name'),
        'progress': #4.10.13
            ('value', 'max'),
        'meter': #4.10.14
            ('value', 'min', 'max', 'low', 'high', 'optimum'),
        'fieldset': #4.10.15
            ('disabled', 'form', 'name'),
        'details': #4.11.1
            ('open',),
        'object': # 4.8.7
            ('data', 'type','name', 'usemap', 'form', 'width', 'height'),
        'param': # 4.8.8
            ('name', 'value'),
        'video': # 4.8.9
            ('src','crossorigin','poster','preload','autoplay','playsinline',
             'loop','muted','controls','width','height'),
        'audio': # 4.8.10
            ('src','crossorigin', 'preload', 'autoplay', 'loop', 'muted',
             'controls'),
        'track': #4.8.11
            ('kind', 'src', 'srclang', 'label', 'default'),
        ####
        'body': # 4.3.1
            ("onafterprint",
            "onbeforeprint",
            "onbeforeunload",
            "onhashchange",
            "onlanguagechange",
            "onmessage",
            "onmessageerror",
            "onoffline",
            "ononline",
            "onpagehide",
            "onpageshow",
            "onpopstate",
            "onrejectionhandled",
            "onstorage",
            "onunhandledrejection",
            "onunload",),

        ####
        'a':
            ('href', 'target', 'download', 'ping', 'rel', 'hreflang', 'type', 'referrerpolicy'),
        ###
        'source':
            ('src', 'type', 'srcset', 'sizes', 'media'),
        'script': #4.12.1
            ('src', 'type', 'nomodule', 'async', 'defer', 'crossorigin',
             'integrity', 'referrerpolicy'),
        'li':
            ('value',)
        }

PARSER = html5lib.HTMLParser(html5lib.treebuilders.getTreeBuilder('dom'), strict=True)

class Validator:
    """
        Drills through a html5lib HTML tree, and checks all the elements
        against various rules.
    """
    def __init__(self, tree):
        self.tree = tree
        self._in_doctype = False
        self._inside = [] # a stack of 

    def __call__(self):
        """
            Actually validate the tree.
        """

        currentNode = self.tree
        while currentNode is not None:

            if currentNode.nodeType == Node.DOCUMENT_TYPE_NODE:
                self.doctype(currentNode.name, currentNode.publicId, currentNode.systemId)

            elif currentNode.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
                self.text(currentNode.nodeValue)

            elif currentNode.nodeType == Node.ELEMENT_NODE:
                if hasattr(currentNode, 'tagName'):
                    if currentNode.tagName in void_elements:
                        self.voidTag(currentNode.tagName, currentNode.attributes)
                    else:
                        self.startTag(currentNode.tagName, currentNode.attributes)

            elif currentNode.nodeType == Node.COMMENT_NODE:
                self.comment(currentNode)

            elif currentNode.nodeType in (Node.DOCUMENT_NODE, Node.DOCUMENT_FRAGMENT_NODE):
                self.document_node(currentNode)

            else:
                self.unknown(currentNode)

            # Go on to the next node, closing this one if needed.
            # NOTE: we don't actually get given the closing tag from html5lib
            # here - it's already (theoretically) been parsed.

            if currentNode.firstChild:
                currentNode = currentNode.firstChild
            elif currentNode.nextSibling:
                currentNode = currentNode.nextSibling
            else:
                self.endTag(currentNode.parentNode.tagName)
                currentNode = currentNode.parentNode.nextSibling or None

            if currentNode == self.tree:
                break

    def check_valid_place(self, name):
        if name in ('html', 'head', 'body') and not self._inside:
            return True

        try:
            required_parents = html_elements[name]
        except KeyError:
            raise InvalidTag(f"{name} is not a valid HTML5 tag.")

        if not self._inside or self._inside == ['html']:
            if name in metadata_elements:
                return True

        if self._inside == ['html', 'head'] and name == 'body':
            self._inside.pop()

        if not any(parent in self._inside for parent in required_parents):
            raise MisplacedElement(f"{name} must be inside {required_parents}")

    def check_valid_attrs(self, name, attributes):

        for (k, v) in attributes.items():
            if k in global_attributes:
                continue
            if k in element_attributes.get(name, ()):
                continue
            if k.startswith('data-'):
                warnings.warn("data-attributes aren't checked for validity yet")
                continue # TODO
            if k in element_attribute_warnings.get(name, ()):
                warnings.warn(f"{name} should NOT have {k}={v} in HTML5.")
                continue
            #if k.startswith('aria-'):
            #    continue # TODO are there other possibilities?

            # TODO: ng-, vue-, other custom attributes?  Should be spec'd by
            #       library users.
            raise InvalidAttribute(f' {k} is not a valid attribute for {name}')

    def startTag(self, name, attributes):


        if name in void_elements:
            raise InvalidTag(f"{name} cannot be used as a Start Tag")
        if name in non_recursable and name in self._inside:
            raise MisplacedElement(f"{name} cannot be inside {name}")

        self.check_valid_place(name)
        self.check_valid_attrs(name, attributes)
        self._inside.append(name)

        return StartTag(name, attributes)

    def document_node(self, node):
        self._in_doctype = True

    def endTag(self, name):
        if self._inside[-1] == name:
            self._inside.pop()
        else:
            if self._inside == ['html', 'body'] and name == 'html':
                return
            raise MisplacedElement(f"End tag for {name} when not inside.")

        self.check_valid_place(name)
        return EndTag(name)

    def voidTag(self, name, attrs, hasChildren=False):
        self.check_valid_place(name)
        self.check_valid_attrs(name, attrs)

        return VoidTag(name, attrs, hasChildren)

    def text(self, data):
        try:
            prefix, mid, suffix = TEXT_MATCH.match(data).groups()
        except AttributeError:
            yield Characters(data)
            return

        if prefix:
            yield SpaceCharacters(prefix)
        if mid:
            yield Characters(mid)
            if suffix:
                yield SpaceCharacters(suffix)

    def comment(self, data):
        return Comment(data)

    def doctype(self, name, publicId=None, systemId=None):
        self._in_doctype = True
        return DocType(name, publicId, systemId)

    def unknown(self, nodeType):
        raise Exception(f'Unknown! {nodeType}')




def validate(text):
    """
        If text is valid HTML5, return None.
        Otherwise, raise some kind of Parsing or Linting Exception.
    """
    if not text.strip():
        raise EmptyPage()

    dom = PARSER.parse(text)

    validator = Validator(dom)
    validator()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            with open(f) as fh:
                validate(fh.read())
    else:
        validate(sys.stdin.read())
