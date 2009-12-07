# encoding: utf-8

from cti.util import Cache

try:
    from mako.template import Template

except ImportError:
    raise ImportError('You must install the mako package.')


__all__ = ['Mako']



class Mako(object):
    def __init__(self, cache=True, cache_size=15, **kw):
        self.cache = Cache(cache_size if cache else 0)
    
    def __call__(self, data, template, content_type='text/html', **options):
        # TODO: create a temp folder on init and pass it as module_directory.
        tmpl = self.cache.get(template, Template(filename=template, **options))
        
        if template not in self.cache: self.cache[template] = tmpl
        
        return content_type, tmpl.render_unicode(**data)
