# encoding: utf-8

from __future__ import with_statement

from os import path

from cti.util import Cache

try:
    from genshi.input import ET, HTML, XML
    from genshi.filters import Translator
    from genshi.template import TemplateLoader, TextTemplate, MarkupTemplate
    from genshi.template.loader import TemplateNotFound

except ImportError:
    raise ImportError('You must install the genshi package.')


__all__ = ['Genshi']



class Genshi(object):
    def __init__(self, cache=True, cache_size=15, **kw):
        self.cache = Cache(cache_size if cache else 0)
    
    def __call__(self, data, template, kind="markup", i18n=None, **options):
        # Method can be one of xml, xhtml, html, or text.
        method = options.get('method', 'text' if kind == 'text' else 'xhtml')
        content_type = options.get('content_type', 'text/plain' if kind == 'text' else 'text/html')
        kind = TextTemplate if kind == 'text' else MarkupTemplate
        
        data.update({'ET': ET, 'HTML': HTML, 'XML': XML})
        
        bpath = path.dirname(template)
        
        if i18n is None:
            if bpath not in self.cache:
                self.cache[bpath] = TemplateLoader([bpath], auto_reload=True)
            
            tmpl = self.cache[bpath].load(template, cls=kind)
            
            return content_type, tmpl.generate(**data).render(method)
        
        def template_loaded(template):
            template.filters.insert(0, Translator(i18n.ugettext))
        
        loader = TemplateLoader([bpath], auto_reload=True, callback=template_loaded)
        
        tmpl = loader.load(template, cls=kind)
        
        return content_type, tmpl.generate(**data).render(method)
