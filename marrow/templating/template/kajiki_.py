# encoding: utf-8

from __future__ import unicode_literals

from os import path, stat
from threading import RLock

from marrow.templating.core import Engine
from marrow.templating.resolver import Resolver

try:
    import kajiki

except ImportError:
    raise ImportError('You must install the kajiki package.')


__all__ = ['Kajiki']


resolve = Resolver()


class Kajiki(Engine):
    extmap = dict(xml="xml", htm="html", html="html", xhtml="xml", html5="html5", txt="text", text="text", kajiki="xml")
    mimetypes = dict(xml="text/xml", html="text/html", html5="text/html", text="text/plain")
    
    def prepare(self, filename, i18n=None, autoescape=False, **options):
        kind = self.extmap.get(path.splitext(filename)[1], None)
        assert kind is not None
        
        source = open(filename, 'rb').read()
        
        if kind == "xml":
            template = kajiki.XMLTemplate(source=source, filename=filename)
        
        elif kind == "html":
            template = kajiki.XMLTemplate(mode='html', source=source, filename=filename)
        
        elif kind == "html5":
            template = kajiki.XMLTemplate(mode='html5', source=source, filename=filename)
        
        elif kind == "text":
            template = kajiki.TextTemplate(source=source, filename=filename, autoescape=autoescape)
        
        template.loader = self
        
        return template, RLock()
    
    def render(self, template, data, **options):
        template, lock = template
        
        lock.acquire() # Might be unnessicary.
        result = template(data).render()
        lock.release()
        
        return options.get('content_type', self.mimetypes[kind]), result
    
    def _filename(self, name):
        return resolve(name)[1]
    
    def _load(self, name):
        filename = self._filename(name)
        
        try:
            tmpl, mtime = self.cache[filename]
        
        except KeyError:
            tmpl, mtime = None, None
        
        if tmpl is None or (self.monitor and stat(template).st_mtime > mtime):
            tmpl, mtime = self.cache[template] = self.prepare(filename), stat(filename).st_mtime
        
        return tmpl
    
    def import_(self, name):
        return self._load(name)
    
    load=import_
