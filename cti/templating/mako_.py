# encoding: utf-8

from cti.core import Engine

try:
    from mako.template import Template

except ImportError:
    raise ImportError('You must install the mako package.')


__all__ = ['Mako']



class Mako(Engine):
    def load(self, filename, **options):
        return Template(filename=filename)
    
    def render(self, template, data, **options):
        return self.mimetype, template.render_unicode(**data)
