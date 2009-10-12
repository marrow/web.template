# encoding: utf-8

"""
"""


import os

from cti.core import Engines
from cti.resolver import Resolver


try:
    from web.core import response
    yapwf = True

except ImportError:
    from webob import Response
    yapwf = False


__all__ = ['template', 'TemplatingMiddleware']
log = __import__('logging').getLogger(__name__)

render = Engines()
resolve = Resolver()

registry = []



def template(template, **extras):
    def outer(func):
        def inner(*args, **kw):
            result = func(*args, **kw)
            
            if not isinstance(result, dict):
                return result
            
            result = TemplatingMiddleware.variables(result, template)
            
            mime, result = render(template, result, **extras)
            
            return result
        
        # Become more transparent.
        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        inner.__dict__ = func.__dict__
        inner.__module__ = func.__module__
        
        return inner
    return outer


class TemplatingMiddleware(object):
    def __init__(self, application, config=dict(), **kw):
        self.config = config.copy()
        self.config.update(kw)
        self.application = application
        render.resolve.default = config.get('web.templating.engine', 'genshi')
    
    @staticmethod
    def lookup(template):
        return resolve(template)[1]
    
    @staticmethod
    def relative(parent):
        parent = resolve(parent)[1]
        def inner(template):
            return os.path.relpath(resolve(template)[1], os.path.dirname(parent))
        return inner
    
    @classmethod
    def variables(cls, udata, template):
        data = dict(
                lookup = cls.lookup,
                relative = cls.relative(template)
            )
        
        for i in registry:
            if callable(i):
                data.update(i())
            else:
                data.update(i)
        
        data.update(udata)
        
        return data
    
    @classmethod
    def response(cls, result, environ, start_response):
        if not yapwf:
            response = Response()
        else:
            global response
        
        response.content_type = result[0]
        
        if isinstance(result[1], str):
            response.body = result[1]
        
        elif isinstance(result[1], unicode):
            response.unicode_body = result[1]
        
        return response(environ, start_response)
    
    def __call__(self, environ, start_response):
        result = self.application(environ, start_response)
        
        # Bail if the returned value is not a tuple.
        if not isinstance(result, tuple):
            return result
        
        if len(result) == 2: template, data, extras = result + (dict(), )
        elif len(result) == 3: template, data, extras = result
        
        if not isinstance(template, str) or not isinstance(data, dict) or not isinstance(extras, dict):
            raise TypeError("Invalid tuple values returned to TemplatingMiddleware.")
        
        options = dict()
        options.update(extras)
        
        if 'web.translator' in environ:
            options['i18n'] = environ['web.translator']
        
        return self.response(render(template, self.variables(data, template), **options), environ, start_response)
