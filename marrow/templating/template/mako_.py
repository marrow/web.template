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
        return self.get_template(filename, options)
    
    def render(self, template, data, **options):
        return options.get('content_type', b'text/html'), template.render_unicode(**data)
    
    def get_template(self, uri, options):
        filename = resolve(uri)[1]
        options.pop('content_type', None)
        return Template(filename=filename, lookup=self, **options)
    
    def adjust_uri(self, uri, relativeto):
        return uri
