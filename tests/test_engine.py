# encoding: utf-8

from __future__ import unicode_literals

import os
from unittest import TestCase

from marrow.templating.core import Engine


class MyEngine(Engine):
    def prepare(self, filename, **options):
        assert 'foo' in options, repr(options)
        return ('foo', 'bar')
    
    def render(self, template, data, **options):
        assert 'bar' in options, repr(options)
        assert template == ('foo', 'bar'), repr(template)
        return b'text/plain', (template, data, options)


class SprintfEngine(Engine):
    def __init__(self, *args, **kw):
        super(SprintfEngine, self).__init__(*args, **kw)
        self.i = 0
        
    def prepare(self, filename, **options):
        self.i += 1
        
        with open(filename) as f:
            return (self.i, f.read())
    
    def render(self, template, data, **options):
        val, f = template
        return b'text/plain', (val, (f % data))


class TestEngineBaseClass(TestCase):
    def test_silly_engine(self):
        engine = MyEngine(foo=True)
        
        mime, result = engine(['baz', 'diz'], bar=False)
        
        self.assertEqual(mime, b'text/plain')
        self.assertEqual(result, (('foo', 'bar'), ['baz', 'diz'], {'foo': True, 'bar': False}))
    
    def test_sprintf_engine(self):
        engine = SprintfEngine()
        
        # Test template loading and execution.
        mime, result = engine(dict(name="world"), 'tests/templates/hello-sprintf.txt')
        self.assertEqual(mime, b'text/plain')
        self.assertEqual(result, (1, "Hello world!"))
        
        # Test template caching.
        mime, result = engine(dict(name="world"), 'tests/templates/hello-sprintf.txt')
        self.assertEqual(mime, b'text/plain')
        self.assertEqual(result, (1, "Hello world!"))
        
        # Update the modification time.
        os.utime('tests/templates/hello-sprintf.txt', None)
        
        # Test cache invalidation.
        mime, result = engine(dict(name="world"), 'tests/templates/hello-sprintf.txt')
        self.assertEqual(mime, b'text/plain')
        self.assertEqual(result, (2, "Hello world!"))
    
    def test_interface(self):
        engine = Engine()
        
        self.assertRaises(NotImplementedError, lambda: engine.render(None, None))
