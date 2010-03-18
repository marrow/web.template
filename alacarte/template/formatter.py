# encoding: utf-8

from __future__ import with_statement

from string import Formatter


__all__ = ['render']

renderer = Formatter()



def render(data, template=None, string=None, content_type='text/plain'):
    """A basic string.Formatter string templating language.
    
    See:
    
        http://www.python.org/doc/2.6/library/string.html#string-formatting
    
    Simple (string-based) usage:
    
        >>> from cti.core import Engines
        >>> render = Engines()
        >>> render('formatter:', dict(name="world"), string="Hello {name}!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from cti.core import Engines
        >>> render = Engines()
        >>> render('formatter:./tests/templates/hello3.txt', dict(name="world"))
        ('text/plain', 'Hello world!')
    
    """
    
    content = string
    
    if template:
        with open(template) as f:
            content = f.read()
    
    return content_type, renderer.vformat(
            content,
            data if isinstance(data, tuple) else tuple(),
            data if isinstance(data, dict) else dict()
        )
