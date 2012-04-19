# encoding: utf-8

from __future__ import unicode_literals

from threading import RLock

from marrow.templating.core import Engine

try:
    from Cheetah.Template import Template

except ImportError:
    raise ImportError('You must install the cheetah package.')


__all__ = ['Cheetah']


class Cheetah(Engine):
    def prepare(self, filename, **options):
        return Template(file=filename), RLock()
    
    def render(self, template, data, **options):
        template, lock = template
        
        lock.acquire()
        template.searchList().append(data)
        result = unicode(template)
        template.searchList()[0:-1] = []
        lock.release()
        
        return options.get('content_type', b'text/html'), result
