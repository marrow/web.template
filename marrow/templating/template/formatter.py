# encoding: utf-8

from __future__ import unicode_literals

from string import Formatter

from marrow.templating.core import Engine


__all__ = ['FormatterEngine']


renderer = Formatter()


class FormatterEngine(Engine):
    """A basic string.Formatter string templating language.
    
    This templating engine is associated with the '.formatter' filename extension
    and defaults to the 'text/plain' mimetype.
    
    See:
    
        http://www.python.org/doc/2.6/library/string.html#string-formatting
    
    Simple (string-based) usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('formatter:', dict(name="world"), string="Hello {name}!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('formatter:./tests/templates/hello3.txt', dict(name="world"))
        ('text/plain', 'Hello world!')
    
    """
    
    def render(self, template, data, **options):
        """Implemented by a sub-class, this returns the 2-tuple of mimetype and unicode content."""
        
        return options.get('content_type', b'text/plain'), renderer.vformat(
                template,
                data if not isinstance(data, dict) else tuple(),
                data if isinstance(data, dict) else dict()
            )
