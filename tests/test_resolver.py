# encoding: utf-8

from unittest import TestCase

from alacarte.core import Resolver


class TestResolver(TestCase):
    def setUp(self):
        self.resolve = Resolver()
    
    def test_deep_file(self):
        engine, path = self.resolve('alacarte/core.py')
        
        self.assertEqual(engine, None)
        self.assertEqual(path.rsplit('/', 2)[-2:], ['alacarte', 'core.py'])
    
    def test_deep_file_cache(self):
        result1 = self.resolve('alacarte/core.py')
        result2 = self.resolve('alacarte/core.py')
        
        self.assertTrue(result1 is result2)
    
    def test_unambiguous_object_reference(self):
        engine, path = self.resolve('templates.hello-template')
        
        self.assertEqual(path.split('/')[-3:], ['tests', 'templates', 'hello-template.txt'])
    
    def test_ambiguous_error(self):
        try:
            self.resolve('genshi:alacarte.resolver')
        
        except ValueError:
            pass
        
        else:
            self.fail()
    
    def test_absolute(self):
        engine, path = self.resolve('/tmp/foo')
        
    def test_relative(self):
        engine, path = self.resolve('./tmp/foo')
    
    def test_bare(self):
        engine, path = self.resolve('json:')
        
        self.assertEqual(engine, 'json')
        self.assertEqual(path, None)
