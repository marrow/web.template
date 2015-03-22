# encoding: utf-8

from __future__ import unicode_literals, absolute_import

import cgi

from web.template.core import Engine
from web.template.resolver import Resolver

try:
	import tenjin
except ImportError:  # pragma: no cover
	raise ImportError('You must install the pyTenjin package.')


__all__ = ['Tenjin']


resolve = Resolver()



class CustomTenjinLoader(tenjin.FileSystemLoader):
	def find(self, filename, dirs=None):
		return super(CustomTenjinLoader, self).find(resolve(filename)[1], dirs)


class Tenjin(Engine):
	def __init__(self, **options):
		default_encoding = options.pop('defualt_encoding', 'utf8')
		tenjin.set_template_encoding(encode=default_encoding)
		
		# preprocess, layout, 
		from tenjin import Engine as TenjinEngine
		
		pp = [ tenjin.TemplatePreprocessor(), tenjin.PrefixedLinePreprocessor() ]
		if options.pop('trim', False): pp.append(TrimPreprocessor(True))
		
		# preamble
		# postamble
		# encoding
		
		self.engine = TenjinEngine(
				pp = pp,
				escapefunc = options.pop('escapefunc', 'cgi.escape'),
				tostrfunc = options.pop('tostrfunc', 'str'),
				cache = options.pop('cache', tenjin.MemoryCacheStorage()),
				loader = options.pop('loader', CustomTenjinLoader()),
				trace = options.pop('trace', True),
				**options
			)

		super(Tenjin, self).__init__()
	
	def _tenjin_context(self, **options):
		context = dict(
				options,
				include = self.engine.include,
				cgi = cgi,
			)
		
		context.update((i, getattr(tenjin.helpers, i)) for i in tenjin.helpers.__all__)
		context.update((i, getattr(tenjin.html, i)) for i in ('escape_html', 'checked', 'selected', 'disabled', 'nl2br', 'text2html', 'tagattr', 'tagattrs', 'nv'))
		
		return context
	
	def prepare(self, filename, **options):
		return filename
	
	def render(self, template, data, **options):
		return options.get('content_type', b'text/html'), self.engine.render(template, data, self._tenjin_context(**dict(options, **data)), layout=True)
