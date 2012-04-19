# encoding: utf-8

from __future__ import unicode_literals

from os import path

from marrow.templating.core import Engine

try:
    from genshi.input import ET, HTML, XML
    from genshi.filters import Translator
    from genshi.template import TemplateLoader, TextTemplate, MarkupTemplate

except ImportError:
    raise ImportError('You must install the genshi package.')


__all__ = ['Genshi']


class Genshi(Engine):
    def __init__(self, cache=25, **kw):
        super(Genshi, self).__init__(cache, **kw)
        
        # We hard-code this as Genshi performs its own monitoring.
        self.genshi_monitor = self.monitor
        self.monitor = False
    
    def prepare(self, filename, kind="markup", i18n=None, **options):
        bpath = path.dirname(filename)
        
        def template_loaded(template):
            template.filters.insert(0, Translator(i18n))
        
        try:
            loader = self.cache[bpath]
        
        except KeyError:
            callback = template_loaded if i18n else None
            loader = self.cache[bpath] = TemplateLoader([bpath],
                auto_reload=self.genshi_monitor, callback=callback)
        
        return loader, filename
    
    def render(self, template, data, kind='markup', **options):
        # Method can be one of xml, xhtml, html, or text.
        method = options.get('method', 'text' if kind == 'text' else 'xhtml')
        content_type = options.get('content_type', b'text/plain' if kind == 'text' else b'text/html')
        kind = TextTemplate if kind == 'text' else MarkupTemplate
        
        data.update({'ET': ET, 'HTML': HTML, 'XML': XML})
        
        loader, template = template
        
        tmpl = loader.load(template, cls=kind)
        
        return content_type, tmpl.generate(**data).render(method)
