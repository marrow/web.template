# encoding: utf-8

from os import path

from cti.core import Engine

try:
    from mako.template import Template
    from mako.lookup import TemplateLookup

except ImportError:
    raise ImportError('You must install the mako package.')


__all__ = ['Mako']



class Mako(Engine):
    def load(self, filename, **options):
        bpath = path.dirname(filename)
        
        try:
            loader = self.cache[bpath]
        
        except KeyError:
            loader = self.cache[bpath] = TemplateLookup(
                    directories=[bpath],
                    filesystem_checks=self.monitor
                )
        
        return Template(filename=filename, lookup=loader)
    
    def render(self, template, data, **options):
        return self.mimetype, template.render_unicode(**data)
