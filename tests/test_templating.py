# encoding: utf-8

from __future__ import unicode_literals

from unittest import TestCase

from marrow.templating.core import Engines



class TestTemplating(TestCase):
	def setUp(self):
		self.render = Engines()
	
	def test_formatter_string(self):
		self.assertEqual(self.render.formatter(dict(name="world"), string="Hello {name}!"),
				(b'text/plain', 'Hello world!'))
	
	def test_formatter_file(self):
		self.assertEqual(self.render.formatter(dict(name="world"), './tests/templates/hello-formatter.txt'),
				(b'text/plain', 'Hello world!'))
	
	def test_sprintf_string(self):
		self.assertEqual(self.render.sprintf(dict(name="world"), string="Hello %(name)s!"),
				(b'text/plain', 'Hello world!'))
	
	def test_sprintf_file(self):
		self.assertEqual(self.render.sprintf(dict(name="world"), './tests/templates/hello-sprintf.txt'),
				(b'text/plain', 'Hello world!'))
	
	def test_template_string(self):
		self.assertEqual(self.render.template(dict(name="world"), string="Hello $name!"),
				(b'text/plain', 'Hello world!'))
	
	def test_template_string_unsafe(self):
		self.assertEqual(self.render.template(dict(name="world"), string="Hello $name!", safe=False),
				(b'text/plain', 'Hello world!'))
	
	def test_template_file(self):
		self.assertEqual(self.render.template(dict(name="world"), './tests/templates/hello-template.txt'),
				(b'text/plain', 'Hello world!'))


class TestEngines(TestCase):
	def setUp(self):
		self.render = Engines()

	def test_kajiki_xml(self):
		rendered = self.render.kajiki(dict(name="world"), './tests/templates/hello-kajiki.xml')
		self.assertEqual(rendered, (b'text/xml', '<html><body><h1>Hello world!</h1></body></html>'))
 
	def test_kajiki_text(self):
		rendered = self.render.kajiki(dict(name="world"), './tests/templates/hello-kajiki.txt')
		self.assertEqual(rendered, (b'text/plain', 'Hello world!'))

	def test_kajiki_include(self):
		rendered = self.render.kajiki(dict(name="world"), './tests/templates/hello-kajiki-include.xml')
		self.assertEqual(rendered, (b'text/xml', '<html><body><h1>Hello world!</h1></body></html>'))

	def test_mako(self):
		self.assertEqual(self.render.mako(dict(name="world"), './tests/templates/hello-mako.txt', content_type=b'text/plain'),
				(b'text/plain', 'Hello world!'))

	def test_mako_include(self):
		self.assertEqual(self.render.mako(dict(name="world"), './tests/templates/hello-mako-include.txt', content_type=b'text/plain'),
				(b'text/plain', 'Hello world!'))
