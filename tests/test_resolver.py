# encoding: utf-8

import os
from unittest import TestCase

from marrow.render.core import Resolver


class TestResolver(TestCase):
    def setUp(self):
        self.resolve = Resolver()
    
    def test_deep_file(self):
        engine, path = self.resolve('marrow/render/core.py')
        
        self.assertEqual(engine, None)
        self.assertEqual(path[0], '/')
        self.assertEqual(path.rsplit('/', 2)[-2:], ['render', 'core.py'])
    
    def test_deep_file_cache(self):
        result1 = self.resolve('marrow/render/core.py')
        result2 = self.resolve('marrow/render/core.py')
        
        self.assertTrue(result1 is result2)
    
    def test_unambiguous_object_reference(self):
        engine, path = self.resolve('templates.hello-template')
        
        self.assertEqual(path.split('/')[-3:], ['tests', 'templates', 'hello-template.txt'])
    
    def test_ambiguous_error(self):
        try:
            self.resolve('genshi:marrow.render.resolver')
        
        except ValueError:
            pass
        
        else:
            self.fail()
    
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
