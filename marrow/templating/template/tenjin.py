# encoding: utf-8

from __future__ import unicode_literals, absolute_import

from marrow.templating.core import Engine
from marrow.templating.resolver import Resolver

try:
	from tenjin import Engine as TenjinEngine
except ImportError:  # pragma: no cover
	raise ImportError('You must install the pyTenjin package.')


__all__ = ['Tenjin']


resolve = Resolver()


class Tenjin(Engine):
	def __init__(self, **options):
		default_encoding = options.pop('defualt_encoding', 'utf8')
		tenjin.set_template_encoding(encode=default_encoding)
		
		# preprocess, layout, 
		self.engine = TenjinEngine(postfix=options.pop('postfix', '.pyhtml'), **options)
	
	def prepare(self, filename, **options):
		return filename  # TODO: Caching.
	
	def render(self, template, data, **options):
		return options.get('content_type', b'text/html'), self.engine.render(template, data)
