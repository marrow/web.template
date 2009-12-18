# encoding: utf-8

import pkg_resources

from os import stat

from cti.resolver import Resolver
from cti.util import Cache


__all__ = ['Engine', 'Engines']



class Engine(object):
    __cache__ = True
    
    def __init__(self, cache=10, monitor=True, content_type='text/html', **options):
        """Initialize a templating/serialization engine.
        
        The cache integer argument defines the number of templates to cache; use 0 to disable.
        
        The monitor boolean argument enables or disables file modification monitoring and template reloading.
        
        The mimetype string argument defines the default mimetype for this engine.
        """
        
        super(Engine, self).__init__()
        
        self.cache = Cache(cache if cache is not None and self.__cache__ else 0)
        
        self.monitor = monitor
        self.mimetype = content_type
        self.options = options
    
    def __call__(self, data, template=None, **options):
        """Handle intelligent caching and reloading of templates."""
        
        try:
            tmpl, mtime = self.cache[template]
        
        except KeyError:
            tmpl, mtime = None, None
        
        if tmpl is None or (self.monitor and stat(template).st_mtime > mtime):
            tmpl, mtime = self.cache[template] = self.load(template, **options), stat(template).st_mtime
        
        return self.render(tmpl, data, **options)
    
    def load(self, filename, **options):
        """Implemented in a sub-class, this returns a template object usable by the render method."""
        
        raise NotImplementedError
    
    def render(self, template, data, **options):
        """Implemented by a sub-class, this returns the 2-tuple of mimetype and unicode content."""
        
        raise NotImplementedError


class Engines(dict):
    """Engines is a dictionary subclass that allows easy reference to
    rendering engines.
    
    It also acts as an attribute dictionary for even easier reference.
    
    Rendering engines are stored internally as entry point references,
    and are .load()'ed on demand.  Support is present for both simple
    callable entry points and new-style classes whose instances are
    callable.  This allows your rendering engine to have startup code.
    """
    class EngineProxy(object):
        def __init__(self, engine, defaults=dict()):
            self.engine = engine
            self.defaults = defaults
        
        def __call__(self, *args, **kw):
            options = dict(self.defaults)
            options.update(kw)
            
            if isinstance(self.engine, pkg_resources.EntryPoint):
                self.engine = self.engine.load()
            
            if isinstance(self.engine, type):
                self.engine = self.engine(**options)
            
            return self.engine(*args, **options)
    
    def __init__(self, default=None, cache=50, **kw):
        super(Engines, self).__init__()
        super(Engines, self).__setattr__('resolve', Resolver(default, cache))
        
        self.refresh(**kw)
    
    def __call__(self, template, data, **kw):
        engine, filename = self.resolve(template)
        
        if not engine:
            raise ValueError('You must explicitly define an engine in each template path if no default is given.')
        
        return self[engine](data=data, template=filename, **kw)
    
    def refresh(self, **kw):
        engines = []
        
        for engine in pkg_resources.iter_entry_points('web.templating'):
            engines.append((engine.name, self.EngineProxy(engine, kw.get(engine.name, dict()))))
        
        self.clear()
        self.update(engines)
    
    def __setitem__(self, name, value):
        if not callable(value):
            raise TypeError("Engines must be callable, a bare function, method, or callable class instance.")
        
        super(Engines, self).__setitem__(name, self.EngineProxy(value))
    
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        self[name] = value
