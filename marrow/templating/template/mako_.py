# encoding: utf-8

from __future__ import unicode_literals

from marrow.templating.core import Engine
from marrow.templating.resolver import Resolver

try:
    from mako.template import Template

except ImportError:
    raise ImportError('You must install the mako package.')


__all__ = ['Mako']


resolve = Resolver()


class Mako(Engine):
    def prepare(self, filename, **options):
        return self.get_template(filename)
    
    def render(self, template, data, **options):
        return options.get('content_type', 'text/html'), template.render_unicode(**data)
    
    def get_template(self, uri):
        filename = resolve(uri)[1]
        return Template(filename=filename, lookup=self)
    
    def adjust_uri(self, uri, relativeto):
        return uri
