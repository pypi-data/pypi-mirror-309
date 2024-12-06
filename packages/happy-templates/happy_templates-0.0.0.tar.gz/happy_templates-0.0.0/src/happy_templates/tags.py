import io


class HappyDoc:
    def __init__(self):
        self.doc = io.StringIO()
        self.write = self.doc.write

    def __call__(self, text: str):
        self.write(text)

    def render(self):
        res = self.doc.getvalue()
        self.doc.close()
        return res


class _HTMLTag:
    __name__ = "htmltag"

    def __init__(self, _hd: HappyDoc, *, classes=None, id=None, **kwargs) -> None:
        if classes:
            kwargs["class"] = classes
        if id:
            kwargs["id"] = id

        self.tag_attrs = kwargs
        self.happy_doc = _hd

    def _format_attributes(self) -> str:
        attrs = " ".join(
            f'{key.replace("_", "-")}="{value}"'
            for key, value in self.tag_attrs.items()
        )
        return " " + attrs if len(attrs) > 0 else ""


class _HTMLContainerTag(_HTMLTag):
    def __enter__(self) -> None:
        self.happy_doc(f"<{self.__name__}{self._format_attributes()}>")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.happy_doc(f"</{self.__name__}>")


class _HTMLSelfClosingTag(_HTMLTag):
    def __init__(self, _hd=None, *, classes=None, id=None, **kwargs) -> None:
        super().__init__(_hd=_hd, classes=classes, id=id, **kwargs)
        self.happy_doc(f"<{self.__name__}{self._format_attributes()}/>")


################################################################################
# Tags are in alphabetic order
################################################################################


class a(_HTMLContainerTag):
    __name__ = "a"


class abbr(_HTMLContainerTag):
    __name__ = "abbr"


class acronym(_HTMLContainerTag):
    __name__ = "acronym"


class address(_HTMLContainerTag):
    __name__ = "address"


class area(_HTMLSelfClosingTag):
    __name__ = "area"


class article(_HTMLContainerTag):
    __name__ = "article"


class aside(_HTMLContainerTag):
    __name__ = "aside"


class b(_HTMLContainerTag):
    __name__ = "b"


class base(_HTMLSelfClosingTag):
    __name__ = "base"


class bdi(_HTMLContainerTag):
    __name__ = "bdi"


class bdo(_HTMLContainerTag):
    __name__ = "bdo"


class blockquote(_HTMLContainerTag):
    __name__ = "blockquote"


class body(_HTMLContainerTag):
    __name__ = "body"


class br(_HTMLSelfClosingTag):
    __name__ = "br"


class button(_HTMLContainerTag):
    __name__ = "button"


class canvas(_HTMLContainerTag):
    __name__ = "canvas"


class caption(_HTMLContainerTag):
    __name__ = "caption"


class cite(_HTMLContainerTag):
    __name__ = "cite"


class code(_HTMLContainerTag):
    __name__ = "code"


class col(_HTMLSelfClosingTag):
    __name__ = "col"


class colgroup(_HTMLContainerTag):
    __name__ = "colgroup"


class data(_HTMLContainerTag):
    __name__ = "data"


class datalist(_HTMLContainerTag):
    __name__ = "datalist"


class dd(_HTMLContainerTag):
    __name__ = "dd"


class del_(_HTMLContainerTag):
    __name__ = "del"


class details(_HTMLContainerTag):
    __name__ = "details"


class dfn(_HTMLContainerTag):
    __name__ = "dfn"


class dialog(_HTMLContainerTag):
    __name__ = "dialog"


class div(_HTMLContainerTag):
    __name__ = "div"


class dl(_HTMLContainerTag):
    __name__ = "dl"


class dt(_HTMLContainerTag):
    __name__ = "dt"


class em(_HTMLContainerTag):
    __name__ = "em"


class embed(_HTMLSelfClosingTag):
    __name__ = "embed"


class fieldset(_HTMLContainerTag):
    __name__ = "fieldset"


class figcaption(_HTMLContainerTag):
    __name__ = "figcaption"


class figure(_HTMLContainerTag):
    __name__ = "figure"


class footer(_HTMLContainerTag):
    __name__ = "footer"


class form(_HTMLContainerTag):
    __name__ = "form"


class h1(_HTMLContainerTag):
    __name__ = "h1"


class h2(_HTMLContainerTag):
    __name__ = "h2"


class h3(_HTMLContainerTag):
    __name__ = "h3"


class h4(_HTMLContainerTag):
    __name__ = "h4"


class h5(_HTMLContainerTag):
    __name__ = "h5"


class h6(_HTMLContainerTag):
    __name__ = "h6"


class head(_HTMLContainerTag):
    __name__ = "head"


class header(_HTMLContainerTag):
    __name__ = "header"


class hr(_HTMLSelfClosingTag):
    __name__ = "hr"


class html(_HTMLContainerTag):
    __name__ = "html"


class i(_HTMLContainerTag):
    __name__ = "i"


class iframe(_HTMLContainerTag):
    __name__ = "iframe"


class img(_HTMLSelfClosingTag):
    __name__ = "img"


class input(_HTMLSelfClosingTag):
    __name__ = "input"


class ins(_HTMLContainerTag):
    __name__ = "ins"


class kbd(_HTMLContainerTag):
    __name__ = "kbd"


class label(_HTMLContainerTag):
    __name__ = "label"


class legend(_HTMLContainerTag):
    __name__ = "legend"


class link(_HTMLSelfClosingTag):
    __name__ = "link"


class main(_HTMLContainerTag):
    __name__ = "main"


class map(_HTMLContainerTag):
    __name__ = "map"


class mark(_HTMLContainerTag):
    __name__ = "mark"


class marquee(_HTMLContainerTag):
    __name__ = "marquee"


class math(_HTMLContainerTag):
    __name__ = "math"


class menu(_HTMLContainerTag):
    __name__ = "menu"


class meta(_HTMLSelfClosingTag):
    __name__ = "meta"


class meter(_HTMLContainerTag):
    __name__ = "meter"


class nav(_HTMLContainerTag):
    __name__ = "nav"


class noscript(_HTMLContainerTag):
    __name__ = "noscript"


class object(_HTMLContainerTag):
    __name__ = "object"


class ol(_HTMLContainerTag):
    __name__ = "ol"


class optgroup(_HTMLContainerTag):
    __name__ = "optgroup"


class option(_HTMLSelfClosingTag):
    __name__ = "option"


class output(_HTMLContainerTag):
    __name__ = "output"


class p(_HTMLContainerTag):
    __name__ = "p"


class param(_HTMLSelfClosingTag):
    __name__ = "param"


class picture(_HTMLContainerTag):
    __name__ = "picture"


class pre(_HTMLContainerTag):
    __name__ = "pre"


class progress(_HTMLContainerTag):
    __name__ = "progress"


class q(_HTMLContainerTag):
    __name__ = "q"


class rb(_HTMLContainerTag):
    __name__ = "rb"


class rp(_HTMLContainerTag):
    __name__ = "rp"


class rt(_HTMLContainerTag):
    __name__ = "rt"


class ruby(_HTMLContainerTag):
    __name__ = "ruby"


class s(_HTMLContainerTag):
    __name__ = "s"


class samp(_HTMLContainerTag):
    __name__ = "samp"


class script(_HTMLContainerTag):
    __name__ = "script"


class section(_HTMLContainerTag):
    __name__ = "section"


class select(_HTMLContainerTag):
    __name__ = "select"


class slot(_HTMLContainerTag):
    __name__ = "slot"


class small(_HTMLContainerTag):
    __name__ = "small"


class source(_HTMLSelfClosingTag):
    __name__ = "source"


class source(_HTMLSelfClosingTag):
    __name__ = "source"


class span(_HTMLContainerTag):
    __name__ = "span"


class strong(_HTMLContainerTag):
    __name__ = "strong"


class style(_HTMLContainerTag):
    __name__ = "style"


class sub(_HTMLContainerTag):
    __name__ = "sub"


class summary(_HTMLContainerTag):
    __name__ = "summary"


class sup(_HTMLContainerTag):
    __name__ = "sup"


class svg(_HTMLContainerTag):
    __name__ = "svg"


class table(_HTMLContainerTag):
    __name__ = "table"


class tbody(_HTMLContainerTag):
    __name__ = "tbody"


class td(_HTMLContainerTag):
    __name__ = "td"


class template(_HTMLContainerTag):
    __name__ = "template"


class textarea(_HTMLContainerTag):
    __name__ = "textarea"


class tfoot(_HTMLContainerTag):
    __name__ = "tfoot"


class th(_HTMLContainerTag):
    __name__ = "th"


class thead(_HTMLContainerTag):
    __name__ = "thead"


class time(_HTMLContainerTag):
    __name__ = "time"


class title(_HTMLContainerTag):
    __name__ = "title"


class tr(_HTMLContainerTag):
    __name__ = "tr"


class track(_HTMLSelfClosingTag):
    __name__ = "track"


class u(_HTMLContainerTag):
    __name__ = "u"


class ul(_HTMLContainerTag):
    __name__ = "ul"


class var(_HTMLContainerTag):
    __name__ = "var"


class video(_HTMLContainerTag):
    __name__ = "video"


class wbr(_HTMLSelfClosingTag):
    __name__ = "wbr"
