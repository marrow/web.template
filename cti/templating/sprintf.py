# encoding: utf-8

from __future__ import with_statement


__all__ = ['render']



def render(template, data):
    """A basic sprintf-based string templating language.
    
    Sample usage:
    
        >>> from cti.core import TemplateInterface
        >>> cti = TemplateInterface()
        >>> cti.render('sprintf:./tests/templates/hello.txt', dict(hello="world"))
        ('application/json', 'Hello world!')
    """
    
    with open(template):
        content = template.read()
    
    return 'application/json', content % data
