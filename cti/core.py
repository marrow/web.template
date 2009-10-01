# encoding: utf-8

import pkg_resources


__all__ = ['Engines']



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


class Engines(dict):
    """Engines is a dictionary subclass that allows easy reference to
    rendering engines.
    
    It also acts as an attribute dictionary for even easier reference.
    
    Rendering engines are stored internally as entry point references,
    and are .load()'ed on demand.  Support is present for both simple
    callable entry points and new-style classes whose instances are
    callable.  This allows your rendering engine to have startup code.
    """
    
    def __init__(self, **kw):
        super(Engines, self).__init__()
        self.refresh(**kw)
    
    def refresh(self, **kw):
        engines = []
        
        for engine in pkg_resources.iter_entry_points('web.templating'):
            engines.append((engine.name, EngineProxy(engine, kw.get(engine.name, dict()))))
        
        self.clear()
        self.update(engines)
    
    def __setitem__(self, name, value):
        if not callable(value):
            raise TypeError("Engines must be callable, a bare function, method, or callable class instance.")
        
        super(Engines, self).__setitem__(name, EngineProxy(value))
    
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        self[name] = value
