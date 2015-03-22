# encoding: utf-8

from __future__ import unicode_literals

import os
from unittest import TestCase

from web.template.core import Resolver


class TestResolver(TestCase):
	def setUp(self):
		self.resolve = Resolver()
	
	def test_deep_file(self):
		engine, path = self.resolve('web.template/core.py')
		
		assert engine is None
		assert path[0] == '/'
		assert path.rsplit('/', 2)[-2:] == ['template', 'core.py']
	
	def test_deep_file_cache(self):
		result1 = self.resolve('web.template/core.py')
		result2 = self.resolve('web.template/core.py')
		
		assert result1 is result2
	
	def test_unambiguous_object_reference(self):
		engine, path = self.resolve('test.templates.hello-template')
		
		assert path.split('/')[-3:] == ['test', 'templates', 'hello-template.txt']
	
	def test_ambiguous_error(self):
		try:
			result = self.resolve('genshi:test.templates.duplicate')
		
		except ValueError:
			return
		
		assert False and result, "Failed to raise a ValueError."
	
	def test_absolute_nix(self):
		engine, package, path = self.resolve.parse('/tmp/foo')
		
		self.assertEqual(engine, None)
		self.assertEqual(package, None)
		self.assertEqual(path, '/tmp/foo')
	
	def test_absolute_win(self):
		engine, package, path = self.resolve.parse('C:\\tmp\\foo')
		
		self.assertEqual(engine, None)
		self.assertEqual(package, None)
		self.assertEqual(path, 'C:\\tmp\\foo')
		
	def test_relative(self):
		engine, path = self.resolve('./tmp/foo')
		
		self.assertEqual(engine, None)
		self.assertEqual(path, os.path.normpath(os.path.abspath('./tmp/foo')))
	
	def test_bare(self):
		engine, path = self.resolve('json:')
		
		self.assertEqual(engine, 'json')
		self.assertEqual(path, None)
