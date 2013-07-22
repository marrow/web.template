# encoding: utf-8

from __future__ import unicode_literals, absolute_import

from marrow.templating.core import Engine
from marrow.templating.resolver import Resolver

try:
    from mako.template import Template
except ImportError:  # pragma: no cover
    raise ImportError('You must install the mako package.')


__all__ = ['Mako']


resolve = Resolver()


class Mako(Engine):
    def prepare(self, filename, **options):
        return self.get_template(filename, **options)
    
    def render(self, template, data, **options):
        if 'only' in options:
            part = options.get('only')
            return options.get('content_type', b'text/html'), template.get_def(part).render_unicode(**data)
        
        return options.get('content_type', b'text/html'), template.render_unicode(**data)
    
    def get_template(self, uri, **options):
        filename = resolve(uri)[1]
        options.pop('i18n', None)  # Mako is satisfied with getting translation functions passed in.
        options.pop('content_type', None)
        options.pop('only', None)
        return Template(filename=filename, lookup=self, **options)
    
    def adjust_uri(self, uri, relativeto):
        return uri
