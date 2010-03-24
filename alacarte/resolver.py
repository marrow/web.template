# encoding: utf-8

import os

from pkg_resources import resource_listdir, resource_filename

from alacarte.util import Cache


__all__ = ['Resolver']



class Resolver(Cache):
    def __init__(self, default=None, capacity=50):
        super(Resolver, self).__init__(capacity)
        self.default = default
    
    def parse(self, path):
        # Split the engine and template parts.
        engine, _, template = path.rpartition(':')
        
        # Handle Windows paths.
        if engine and len(engine) == 1:
            template = engine + ':' + template
            engine = ''
        
        if not engine: engine = self.default
        if not template: return (engine, None, None)
        if template[0] in ('/', '.') or template[1] == ':': return (engine, None, template)
        package, _, path = template.partition('/')
        
        return (engine, package, path if path else None)
    
    def __call__(self, template):
        # If we already have this value cached, return the cached copy.
        if template in self:
            return self[template]
        
        # Parse the passed template.
        engine, package, path = self.parse(template)
        
        if not package:
            if not path:
                # Handle bare engines, e.g. serializers.
                self[template] = (engine, None)
                return self[template]
            
            # Handle absolute and relative paths.
            path = path.replace('/', os.path.sep)
            self[template] = (engine, os.path.abspath(path))
            return self[template]
        
        parts = package.split('.')
        if not path: parts, path = parts[:-1], parts[-1]
        
        path = path.split('/')
        
        possibilities = [i for i in resource_listdir('.'.join(parts), '/'.join(path[:-1])) if i.startswith(path[-1] + '.')]
        
        if len(possibilities) == 1:
            path[-1] = possibilities[0]
        
        elif len(possibilities) > 1:
            if path[-1] not in possibilities:
                raise ValueError('Ambiguous template name. Please use the following template path syntax: %s/%s.[%s]' % (
                        '.'.join(parts),
                        '/'.join(path),
                        ','.join([i.split('.')[-1] for i in possibilities])
                    ))
        
        self[template] = (engine, resource_filename('.'.join(parts), '/'.join(path)))
        return self[template]
