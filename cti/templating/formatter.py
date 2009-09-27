# encoding: utf-8

from __future__ import with_statement

if sys.version_info <= (2, 5):
    raise SystemExit("Python 2.5 or later is required.")

from string import Formatter


__all__ = ['render']

renderer = Formatter()



def render(data, template=None, string=None, content_type='text/plain'):
    """A basic string.Formatter string templating language.
    
    See:
    
        http://www.python.org/doc/2.6/library/string.html#string-formatting
    
    Simple (string-based) usage:
    
        >>> from cti.core import TemplateInterface
        >>> cti = TemplateInterface()
        >>> cti.render('formatter:', dict(name="world"), string="Hello {name}!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from cti.core import TemplateInterface
        >>> cti = TemplateInterface()
        >>> cti.render('formatter:./tests/templates/hello3.txt', dict(name="world"))
        ('text/plain', 'Hello world!')
    
    """
    
    content = string
    
    if template:
        with open(template):
            content = template.read()
    
    return content_type, renderer.vformat(
            content,
            data if isinstance(data, tuple) else tuple(),
            data if isinstance(data, dict) else dict()
        )
