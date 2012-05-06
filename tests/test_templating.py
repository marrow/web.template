# encoding: utf-8

import sys

from unittest import TestCase

from marrow.templating.core import Engines
from marrow.templating.resolver import Resolver



class TestTemplating(TestCase):
    def setUp(self):
        self.render = Engines()
    
    def test_formatter_string(self):
        self.assertEqual(self.render.formatter(dict(name="world"), string="Hello {name}!"),
                ('text/plain', 'Hello world!'))
    
    def test_formatter_file(self):
        self.assertEqual(self.render.formatter(dict(name="world"), './templates/hello-formatter.txt'),
                ('text/plain', 'Hello world!'))
    
    def test_sprintf_string(self):
        self.assertEqual(self.render.sprintf(dict(name="world"), string="Hello %(name)s!"),
                ('text/plain', 'Hello world!'))
    
    def test_sprintf_file(self):
        self.assertEqual(self.render.sprintf(dict(name="world"), './templates/hello-sprintf.txt'),
                ('text/plain', 'Hello world!'))
    
    def test_template_string(self):
        self.assertEqual(self.render.template(dict(name="world"), string="Hello $name!"),
                ('text/plain', 'Hello world!'))
    
    def test_template_string_unsafe(self):
        self.assertEqual(self.render.template(dict(name="world"), string="Hello $name!", safe=False),
                ('text/plain', 'Hello world!'))
    
    def test_template_file(self):
        self.assertEqual(self.render.template(dict(name="world"), './templates/hello-template.txt'),
                ('text/plain', 'Hello world!'))


class TestEngines(TestCase):
    def setUp(self):
        self.render = Engines()

    def test_kajiki_xml(self):
        rendered = self.render.kajiki(dict(name="world"), 'templates/hello-kajiki.xml')
        self.assertEqual(rendered, (u'text/xml', u'<html><body><h1>Hello world!</h1></body></html>'))
 
    def test_kajiki_text(self):
        rendered = self.render.kajiki(dict(name="world"), 'templates/hello-kajiki.txt')
        self.assertEqual(rendered, (u'text/plain', u'Hello world!'))

    def test_kajiki_include(self):
        rendered = self.render.kajiki(dict(name="world"), 'templates/hello-kajiki-include.xml')
        self.assertEqual(rendered, (u'text/xml', u'<html><body><h1>Hello world!</h1></body></html>'))

    def test_mako(self):
        self.assertEqual(self.render.mako(dict(name="world"), './templates/hello-mako.txt', content_type='text/plain'),
                ('text/plain', u'Hello world!'))

    def test_mako_include(self):
        self.assertEqual(self.render.mako(dict(name="world"), './templates/hello-mako-include.txt', content_type='text/plain'),
                ('text/plain', u'Hello world!'))

    def test_cheetah(self):
        self.assertEqual(self.render.cheetah(dict(name="world"), './templates/hello-cheetah.tmpl', content_type='text/plain'),
                ('text/plain', u'Hello world!\n'))
