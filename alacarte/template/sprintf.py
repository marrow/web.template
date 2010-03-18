# encoding: utf-8

from __future__ import with_statement

from alacarte.template.engine import Engine


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
    
    mapping = {
            'sprintf': 'text/plain',
            None: 'text/plain'
        }
    
    def render(self, template, data, options):
        return self.mapping[None], template % data
