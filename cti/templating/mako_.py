# encoding: utf-8

from cti.core import Engine
from cti.middleware import resolve

try:
    from mako.template import Template

except ImportError:
    raise ImportError('You must install the mako package.')


__all__ = ['Mako']


class Mako(Engine):
    def load(self, filename, **options):
        return self.get_template(filename)
    
    def render(self, template, data, **options):
        return self.mimetype, template.render_unicode(**data)

    def get_template(self, uri):
        filename = resolve(uri)[1]
        return Template(filename=filename, lookup=self)
    
    def adjust_uri(self, uri, relativeto):
        return uri
