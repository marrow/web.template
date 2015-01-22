# encoding: utf-8

from __future__ import unicode_literals

import pytest

from unittest import TestCase

from marrow.templating.core import Engines



class TestTemplating(TestCase):
	def setUp(self):
		self.render = Engines()
	
	def test_formatter_string(self):
		assert self.render.formatter(dict(name="world"), string="Hello {name}!") == \
				(b'text/plain', 'Hello world!')
	
	def test_formatter_file(self):
		assert self.render.formatter(dict(name="world"), './test/templates/hello-formatter.txt') == \
				(b'text/plain', 'Hello world!')
	
	def test_sprintf_string(self):
		assert self.render.sprintf(dict(name="world"), string="Hello %(name)s!") == \
				(b'text/plain', 'Hello world!')
	
	def test_sprintf_file(self):
		assert self.render.sprintf(dict(name="world"), './test/templates/hello-sprintf.txt') == \
				(b'text/plain', 'Hello world!')
	
	def test_template_string(self):
		assert self.render.template(dict(name="world"), string="Hello $name!") == \
				(b'text/plain', 'Hello world!')
	
	def test_template_string_unsafe(self):
		assert self.render.template(dict(name="world"), string="Hello $name!", safe=False) == \
				(b'text/plain', 'Hello world!')
	
	def test_template_file(self):
		assert self.render.template(dict(name="world"), './test/templates/hello-template.txt') == \
				(b'text/plain', 'Hello world!')


class TestEngines(TestCase):
	def setUp(self):
		self.render = Engines()
	
	def test_kajiki_xml(self):
		pytest.importorskip("kajiki")
		rendered = self.render.kajiki(dict(name="world"), './test/templates/hello-kajiki.xml')
		assert rendered == (b'text/xml', '<html><body><h1>Hello world!</h1></body></html>')
	 
	def test_kajiki_text(self):
		pytest.importorskip("kajiki")
		rendered = self.render.kajiki(dict(name="world"), './test/templates/hello-kajiki.txt')
		assert rendered == (b'text/plain', 'Hello world!')
	
	def test_kajiki_include(self):
		pytest.importorskip("kajiki")
		rendered = self.render.kajiki(dict(name="world"), './test/templates/hello-kajiki-include.xml')
		assert rendered == (b'text/xml', '<html><body><h1>Hello world!</h1></body></html>')
	
	def test_mako(self):
		pytest.importorskip("mako")
		assert self.render.mako(dict(name="world"), './test/templates/hello-mako.txt', content_type=b'text/plain') == \
				(b'text/plain', 'Hello world!')
	
	def test_mako_include(self):
		pytest.importorskip("mako")
		assert self.render.mako(dict(name="world"), './test/templates/hello-mako-include.txt', content_type=b'text/plain') == \
				(b'text/plain', 'Hello world!\n')
