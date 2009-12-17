# encoding: utf-8

import sys

from unittest import TestCase

from cti.core import Engines
from cti.resolver import Resolver
from cti.middleware import TemplatingMiddleware



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
    
    def test_mako(self):
        self.assertEqual(self.render.mako(dict(name="world"), './templates/hello-mako.txt', content_type='text/plain'),
                ('text/plain', u'Hello world!'))


# class TestBuffete(TestCase):
#     def setUp(self):
#         self.resolve = Resolver()
#         self.middleware = TemplatingMiddleware(None, **{'web.templating.buffet': True})
#     
#     def test_cheetah(self):
#         self.assertEqual(self.middleware.buffet('cheetah', 'templates.hello-cheetah', dict(name="world"), content_type="text/plain"),
#                 ('text/plain', u'Hello world!'))
