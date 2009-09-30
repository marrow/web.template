# encoding: utf-8

import pkg_resources


__all__ = ['Engines']


class Engines(dict):
    """Engines is a dictionary subclass that allows easy reference to
    rendering engines.
    
    It also acts as an attribute dictionary for even easier reference.
    
    Rendering engines are stored internally as entry point references,
    and are .load()'ed on demand.  If an engine can't be loaded from
    the initial cache, the cache will be updated once, then a
    ValueError will be raised.
    
    Auto-reloading like this allows templating languages to be added
    at runtime.
    """
    
    def __init__(self):
        engines = []
        
        for engine in pkg_resources.iter_entry_points('web.templating'):
            engines.append((engine.name, engine))
        
        super(Engines, self).__init__(engines)
    
    def __getitem__(self, name):
        engine = super(Engines, self).__getitem__(name)
        return engine.load()
    
    def __getattr__(self, name):
        return self[name]
    
    def __missing__(self, name):
        engines = []
        
        for engine in pkg_resources.iter_entry_points('web.templating'):
            engines.append((engine.name, engine))
        
        self.clear()
        self.update(engines)
        
        if name not in dict(engines): raise KeyError
        return self[name]
