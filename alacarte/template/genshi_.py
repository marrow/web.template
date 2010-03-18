# encoding: utf-8

from os import path

from cti.core import Engine
from cti.util import Cache

try:
    from genshi.input import ET, HTML, XML
    from genshi.filters import Translator
    from genshi.template import TemplateLoader, TextTemplate, MarkupTemplate
    from genshi.template.loader import TemplateNotFound

except ImportError:
    raise ImportError('You must install the genshi package.')


__all__ = ['Genshi']



class Genshi(Engine):
    def __init__(self, cache=25, **kw):
        super(Genshi, self).__init__(cache, **kw)
        
        # We hard-code this as Genshi performs its own monitoring.
        self.genshi_monitor = self.monitor
        self.monitor = False
    
    def load(self, filename, kind="markup", i18n=None, **options):
        bpath = path.dirname(filename)
        
        def template_loaded(template):
            template.filters.insert(0, Translator(i18n.ugettext))
        
        try:
            loader = self.cache[bpath]
        
        except KeyError:
            loader = self.cache[bpath] = TemplateLoader([bpath], auto_reload=self.genshi_monitor, callback=None if i18n is None else template_loaded)
        
        return loader, filename
    
    def render(self, template, data, kind='markup', **options):
        # Method can be one of xml, xhtml, html, or text.
        method = options.get('method', 'text' if kind == 'text' else 'xhtml')
        content_type = options.get('content_type', 'text/plain' if kind == 'text' else 'text/html')
        kind = TextTemplate if kind == 'text' else MarkupTemplate
        
        data.update({'ET': ET, 'HTML': HTML, 'XML': XML})
        
        loader, template = template
        
        tmpl = loader.load(template, cls=kind)
        
        return content_type, tmpl.generate(**data).render(method)
