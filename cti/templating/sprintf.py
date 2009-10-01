# encoding: utf-8

from __future__ import with_statement


__all__ = ['render']



def render(data, template=None, string=None, content_type='text/plain'):
    """A basic sprintf-based string templating language.
    
    Simple (string-based) usage:
    
        >>> from cti.core import TemplateInterface
        >>> cti = TemplateInterface()
        >>> cti.render('sprintf:', dict(hello="world"), string="Hello %(hello)s!")
        ('application/json', 'Hello world!')
    
    File-based usage:
    
        >>> from cti.core import TemplateInterface
        >>> cti = TemplateInterface()
        >>> cti.render('sprintf:./tests/templates/hello.txt', dict(hello="world"))
        ('application/json', 'Hello world!')
    
    """
    
    content = string
    
    if template:
        with open(template) as f:
            content = f.read()
    
    return content_type, content % data
