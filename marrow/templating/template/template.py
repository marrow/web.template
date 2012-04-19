# encoding: utf-8

from __future__ import unicode_literals

from string import Template


__all__ = ['render']


def render(data, template=None, string=None, safe=True, content_type=b'text/plain'):
    """A basic string.Template string templating language.
    
    See:
    
        http://www.python.org/doc/2.5/lib/node40.html
    
    Simple (string-based) usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('template:', dict(name="world"), string="Hello $name!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('template:./tests/templates/hello2.txt', dict(name="world"))
        ('text/plain', 'Hello world!')
    
    """
    
    content = string
    
    if template:
        with open(template) as f:
            content = f.read()
    
    renderer = Template(content)
    
    if safe:
        return content_type, renderer.safe_substitute(data)
    
    return content_type, renderer.substitute(data)
