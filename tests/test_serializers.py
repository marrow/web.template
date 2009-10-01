# encoding: utf-8

import sys

from unittest import TestCase

from cti.core import Engines



class TestBencode(TestCase):
    def setUp(self):
        self.render = Engines()
    
    def test_bencode_basic(self):
        self.assertEqual(self.render.bencode("foo", kind='basic'), ('application/x-bencode', '3:foo'))
    
    def test_bencode_enhanced(self):
        self.assertEqual(self.render.bencode(u"foo"), ('application/x-bencode', 'u3:foo'))


class TestJSON(TestCase):
    def setUp(self):
        self.render = Engines()
    
    def test_json(self):
        self.assertEqual(self.render.json("foo"), ('application/json', '"foo"'))
    
    def test_simplejson(self):
        sys.modules['json'] = None
        
        if 'cti.serializers.json_' in sys.modules:
            del sys.modules['cti.serializers.json_']
        
        self.assertEqual(self.render.json("foo"), ('application/json', '"foo"'))
        
        del sys.modules['json']
        # del sys.modules['cti.serializers.json_']


class TestMarshal(TestCase):
    def setUp(self):
        self.render = Engines()
    
    def test_marshal(self):
        self.assertEqual(self.render.marshal("foo"), ('application/octet-stream', 't\x03\x00\x00\x00foo'))


class TestPickle(TestCase):
    def setUp(self):
        self.render = Engines()
    
    def test_pickle(self):
        self.assertEqual(self.render.pickle("foo"), ('application/octet-stream', "S'foo'\np0\n."))
    
    def test_cpickle(self):
        self.assertEqual(self.render.cpickle("foo"), ('application/octet-stream', "S'foo'\np1\n."))


class TestYaml(TestCase):
    def setUp(self):
        self.render = Engines()
    
    def test_yaml(self):
        self.assertEqual(self.render.yaml("foo"), ('application/x-yaml', 'foo\n...\n'))



