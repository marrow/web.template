# encoding: utf-8

from __future__ import with_statement

from cti.util import Cache

try:
    from genshi.template import TemplateLoader, TextTemplate, MarkupTemplate
    from genshi.template.loader import TemplateNotFound

except ImportError:
    raise ImportError('You must install the genshi package.')


__all__ = ['Genshi']



class Genshi(object):
    def __init__(self, cache=True, cache_size=30, **kw):
        self.cache = Cache(cache_size if cache else 0)
    
    def __call__(self, data, template, kind="markup", **options):
        # Method can be one of xml, xhtml, html, or text.
        method = options.get('method', 'text' if kind == 'text' else 'xhtml')
        
        if kind == "markup":
            return self.markup(data, template, method, **options)
        
        return self.text(data, template, method, **options)
    
    def text(self, data, template, method, strict=False, content_type="text/plain", **options):
        if template not in self.cache:
            with open(template) as f:
                tmpl = TextTemplate(f.read())
                tmpl.lookup = 'strict' if strict else 'lenient'
                self.cache[template] = tmpl
        
        return content_type, self.cache[template].generate(**data).render(method)
    
    def markup(self, data, template, method, strict=False, content_type="text/html", doctype='xhtml', strip_whitespace=True, namespace_prefixes=None, drop_xml_decl=True, strip_markup=False, **kw):
        if template not in self.cache:
            with open(template) as f:
                tmpl = MarkupTemplate(f.read())
                tmpl.lookup = 'strict' if strict else 'lenient'
                self.cache[template] = tmpl
        
        return content_type, self.cache[template].generate(**data).render(method)
