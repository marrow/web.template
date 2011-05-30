# encoding: utf-8

from unittest import TestCase

from marrow.templating.core import Engines


class TestEnginesDictCommonUsage(TestCase):
    def test_no_defaults(self):
        render = Engines()
        
        self.assertTrue('json' in render)
        self.assertTrue(callable(render.json))
        self.assertEqual(render.options['json'], dict())
    
    def test_defaults(self):
        render = Engines(json=dict(content_type="foo"))
        self.assertEqual(render.options['json'], dict(content_type="foo"))
        
        render.options['json'] = dict(content_type="bar")
        self.assertEqual(render.options['json'], dict(content_type="bar"))
    
    def test_engine_func(self):
        def engine(data, template=None):
            return 'text/plain', data
        
        render = Engines()
        render['raw'] = engine
        
        self.assertEqual(render.raw("foo"), ('text/plain', 'foo'))
        
        del render.raw
    
    def test_engine_class(self):
        class Engine(object):
            def __call__(self, data, template=None):
                return 'text/plain', data
        
        render = Engines()
        render['raw'] = Engine
        
        self.assertEqual(render.raw("foo"), ('text/plain', 'foo'))
        
        del render.raw
    
    def test_bad_engine_name(self):
        render = Engines()
        self.assertRaises(ValueError, lambda: render('text/html:'))
    
    def test_render(self):
        render = Engines()
        
        self.assertEqual(render('sprintf:./tests/templates/hello-sprintf.txt', dict(name='world')), ('text/plain', "Hello world!"))
    
    def test_render_no_engine(self):
        render = Engines()
        
        try:
            self.assertEqual(render('./tests/templates/hello-sprintf.txt', dict(name='world')), ('text/plain', "Hello world!"))
        
        except ValueError:
            pass
        
        except:
            self.fail()