# encoding: utf-8

from __future__ import unicode_literals

from unittest import TestCase

from marrow.templating.core import Engines


class TestEnginesDictCommonUsage(TestCase):
	def test_no_defaults(self):
		render = Engines()
		
		assert 'json' in render
		assert callable(render.json)
		assert render.options['json'] == dict()
	
	def test_defaults(self):
		render = Engines(json=dict(content_type="foo"))
		assert render.options['json'] == dict(content_type="foo")
		
		render.options['json'] = dict(content_type="bar")
		assert render.options['json'] == dict(content_type="bar")
	
	def test_engine_func(self):
		def engine(data, template=None):
			return b'text/plain', data
		
		render = Engines()
		render['raw'] = engine
		
		assert render.raw("foo") == (b'text/plain', 'foo')
		
		del render.raw
	
	def test_engine_class(self):
		class Engine(object):
			def __call__(self, data, template=None):
				return b'text/plain', data
		
		render = Engines()
		render['raw'] = Engine
		
		assert render.raw("foo") == (b'text/plain', 'foo')
		
		del render.raw
	
	def test_bad_engine_name(self):
		render = Engines()
		self.assertRaises(ValueError, lambda: render('text/html:'))
	
	def test_render(self):
		result = Engines()('sprintf:./tests/templates/hello-sprintf.txt', dict(name='world'))
		
		assert result == (b'text/plain', "Hello world!")
	
	def test_render_no_engine(self):
		render = Engines()
		
		try:
			assert render('./tests/templates/hello-sprintf.txt', dict(name='world')) == (b'text/plain', "Hello world!")
		
		except ValueError:
			pass
		
		except:
			self.fail()