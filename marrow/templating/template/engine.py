# encoding: utf-8

from os import stat

from marrow.templating.util import Cache


__all__ = ['Engine']


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
            return self.render(self.prepare(None, **options), data, **options)
        
        try:
            tmpl, mtime = self.cache[template]
        
        except KeyError:
            tmpl, mtime = None, None
        
        if tmpl is None or (self.monitor and stat(template).st_mtime > mtime):
            tmpl, mtime = self.cache[template] = self.prepare(template, **options), stat(template).st_mtime
        
        return self.render(tmpl, data, **options)
    
    def prepare(self, filename, **options):
        """Optionally overridden in a sub-class, this returns a template object usable by the render method.
        
        By default this loads the template from the given filename, or the "string" option, if specified.
        When subclassing you can choose to keep this behaviour or roll your own by optionally using super.
        
        Also utilizes unicode decoding (defaulting to 'utf8', overridden by the 'encoding' option) if needed.
        """
        
        if not filename:
            content = options['string']
            del options['string']
            return content
        
        with open(filename) as f:
            content = f.read()
            
            if not isinstance(content, unicode):
                content = content.decode(options.get('encoding', 'utf8')) if isinstance(content, str) else content
        
        return content
    
    def render(self, template, data, **options):
        """Implemented by a sub-class, this returns the 2-tuple of mimetype and unicode content."""
        
        raise NotImplementedError
