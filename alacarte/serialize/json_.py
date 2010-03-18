# encoding: utf-8

try:
    from json import dumps

except ImportError:
    try:
        from simplejson import dumps
    
    except ImportError: # pragma: no cover
        raise ImportError('Your version of Python requires that you install the simplejson package for JSON support.')


__all__ = ['render']



def render(data, template=None, content_type='application/json', **kw):
    """A basic JSON serializer templating language.
    
    Accepts the same extended arguments as the JSON dumps() function, see:
    
        http://docs.python.org/library/json.html#json.dump
    
    Data may be of any datatype supported by the json standard library or simplejson.
    
    Sample usage:
    
        >>> from cti.core import Engines
        >>> render = Engines()
        >>> render.json(dict(hello="world"))
        ('application/json', '{"hello": "world"}')
    
    More compact notation:
        
        >>> from cti.core import Engines
        >>> render = Engines()
        >>> render.json(dict(hello="world"), separators=(',', ':'))
        ('application/json', '{"hello":"world"}')
        
    """
    
    return content_type, dumps(data, **kw)
