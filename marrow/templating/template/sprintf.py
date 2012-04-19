# encoding: utf-8

from __future__ import unicode_literals

from marrow.templating.core import Engine


__all__ = ['SprintfEngine']


class SprintfEngine(Engine):
    """A basic sprintf-based string templating language.
    
    Simple (string-based) usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('sprintf:', dict(hello="world"), string="Hello %(hello)s!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('sprintf:./tests/templates/hello.txt', dict(hello="world"))
        ('text/plain', 'Hello world!')
    
    """
    
    def render(self, template, data, **options):
        return options.get('content_type', b'text/plain'), template % data
