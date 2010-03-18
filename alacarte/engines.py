# encoding: utf-8

import pkg_resources
import warnings

from functools import partial

from alacarte.resolver import Resolver
from alacarte.util import Cache


__all__ = ['Engines']



class EngineProxy(object):
    def __init__(self, engine, config=dict()):
        self.engine = engine
        self.config = config
    
    def __call__(self, *args, **kw):
        options = dict(self.config)
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
    def __init__(self, default=None, cache=50, container=None, **kw):
        """Engines creates a Resolver instance and configures Distribute
        entry point iteration.
        
        You may pass additional keyword arguments to pre-configure
        engine options.  Engine options will either be merged with
        the options passed at runtime or passed during engine
        initialization depending on if the engine is a simple callable
        or class, respectively.
        """
        
        super(Engines, self).__init__()
        
        self.resolve = Resolver(default, cache)
        
        collection = pkg_resources.WorkingSet()
        collection.subscribe(partial(self._distributions, config=kw))
    
    def __call__(self, template, data=None, **kw):
        """Resolve and execute the given template, passing data to the engine."""
        engine, filename = self.resolve(template)
        
        if not engine:
            # TODO: Examine the extension and use the appropriate engine.
            raise ValueError('You must explicitly define an engine in each template path if no default is given.')
        
        if '/' in engine:
            # TODO: Lookup by mimetype.
            raise ValueError('You can not currently request an engine by mimetype.')
        
        return self[engine](data=data, template=filename, **kw)
    
    def __setitem__(self, name, value):
        if not callable(value):
            raise TypeError("Engines must be callable, a bare function, method, or callable class instance.")
        
        if isinstance(value, EngineProxy):
            return super(Engines, self).__setitem__(name, value)
        
        return super(Engines, self).__setitem__(name, EngineProxy(value))
    
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        if name.startswith('_'): self.__dict__[name] = value
        self[name] = value
    
    def __delattr__(self, name):
        del self[name]
    
    def _distributions(self, dist, config):
        entries = dist.get_entry_map('web.templating')
        
        if entries:
            warnings.warn(
                    'The %s package has delcared "web.templating" entry points.\n'
                    'The "web.templating" entry_point namespace has been deprecated in favor of "alacarte".' % dist.egg_name(),
                    DeprecationWarning
                )
        
        entries.update(dist.get_entry_map('alacarte'))
        
        if not entries: return
        
        for name, engine in entries.iteritems():
            self[name] = EngineProxy(engine, config.get(name, dict()))
