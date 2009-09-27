# encoding: utf-8

try:
    from json import dumps

except ImportError:
    try:
        from simplejson import dumps
    
    except ImportError:
        raise ImportError('Your version of Python requires that you install the simplejson package for JSON support.')


__all__ = ['render']



def render(data, template=None, **kw):
    """A basic JSON serializer templating language.
    
    Accepts the same extended arguments as the JSON dumps() function, see:
    
        http://docs.python.org/library/json.html#json.dump
    
    Data may be of any datatype supported by the json standard library or simplejson.
    
    Sample usage:
    
        >>> from cti.core import TemplateInterface
        >>> cti = TemplateInterface()
        >>> cti.render('json:', dict(hello="world"))
        ('application/json', '{"hello": "world"}')
    
    More compact notation:
        
        >>> from cti.core import TemplateInterface
        >>> cti = TemplateInterface()
        >>> cti.render('json:', dict(hello="world"), separators=(',', ':'))
        ('application/json', '{"hello":"world"}')
        
    """
    
    return 'application/json', dumps(data, **kw)
