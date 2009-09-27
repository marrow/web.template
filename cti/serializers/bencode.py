# encoding: utf-8

from web.extras import bencode


__all__ = ['render']

codecs = dict(
        basic = bencode.Bencode(),
        enhanced = bencode.EnhancedBencode()
    )



def render(data, template=None, kind='enhanced'):
    """A bencoding serializer templating language.
    
    Accepts the same extended arguments as the JSON dumps() function, see:
    
        http://docs.python.org/library/json.html#json.dump
    
    Data may be of any datatype supported by the json standard library or simplejson.
    
    Sample usage:
    
        >>> from sti import TemplateInterface
        >>> sti = TemplateInterface()
        >>> sti.render('bencode:', dict(hello="world"))
        ('application/x-bencode', 'd5:hello5:worlde')
        
    """
    
    return 'application/x-bencode', unicode(codecs[kind].encode(data))
