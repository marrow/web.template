# encoding: utf-8

from os.path import dirname

try:
    from genshi.template import TemplateLoader, TextTemplate, MarkupTemplate

except ImportError:
    raise ImportError('You must install the genshi package.')


__all__ = ['render']



class Genshi(object):
    def __init__(self, **kw):
        self.cache = TemplateLoader()
    
    def text(self):
        pass
    
    def markup(self):
        pass
    
    def __call__(template, data, **kw):
        
        template = self.cache.load(
                template,
                cls = cls,
                encoding = encoding,
            )
        
        template.lookup = 'strict' if strict else 'lenient'
        
        if kind == 'markup':
            mime_type = self.method_mapping[method]
        
        stream = template.generate(**data)
        return mime_type, stream.render(method)
