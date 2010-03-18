# encoding: utf-8

from __future__ import with_statement

from os import stat

from alacarte.resolver import Resolver
from alacarte.util import Cache


__all__ = ['Engines']



class Engine(object):
    __cache__ = True
    
    def __init__(self, cache=10, monitor=True, **options):
        """Initialize a templating/serialization engine.
        
        The cache integer argument defines the number of templates to cache; use 0 to disable.
        
        The monitor boolean argument enables or disables file modification monitoring and template reloading.
        
        The mimetype string argument defines the default mimetype for this engine.
        """
        
        super(Engine, self).__init__()
        
        self.cache = Cache(cache if cache is not None and self.__cache__ else 0)
        
        self.monitor = monitor
        self.options = options
    
    def __call__(self, data, template=None, **kw):
        """Handle intelligent caching and reloading of templates."""
        
        options = dict(self.options)
        options.update(kw)
        
        if not template:
            return self.render(self.load(None, options), data, options)
        
        try:
            tmpl, mtime = self.cache[template]
        
        except KeyError:
            tmpl, mtime = None, None
        
        if tmpl is None or (self.monitor and stat(template).st_mtime > mtime):
            print "got here"
            tmpl, mtime = self.cache[template] = self.load(template, options), stat(template).st_mtime
        
        return self.render(tmpl, data, options)
    
    def load(self, filename, options):
        """Optionally overridden in a sub-class, this returns a template object usable by the render method.
        
        By default this loads the template from the given filename, or the "string" option, if specified.
        
        Also utilizes a decoding (defaulting to 'utf8', overridden by the 'encoding' option) if needed.
        """
        
        if not filename:
            return options['string']
        
        with open(filename) as f:
            content = f.read()
            
            if not isinstance(content, unicode):
                content = content.decode(options.get('encoding', 'utf8'))
        
        return content
    
    def render(self, template, data, options):
        """Implemented by a sub-class, this returns the 2-tuple of mimetype and unicode content."""
        
        raise NotImplementedError
