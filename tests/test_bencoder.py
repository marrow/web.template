# encoding: utf-8

import sys

from unittest import TestCase

from marrow.render.serialize import bencode



class TestBasicBencoder(TestCase):
    def setUp(self):
        self.codec = bencode.Bencode()
    
    def test_encode_simple(self):
        self.assertEqual(self.codec.encode('str'), '3:str', 'invalid string encoding')
        self.assertEqual(self.codec.encode(2), 'i2e', 'invalid integer encoding')
        self.assertEqual(self.codec.encode(2l), 'i2e', 'invalid long integer encoding')
        self.assertEqual(self.codec.encode(dict(name="value")), 'd4:name5:valuee', 'invalid dictionary encoding')
        self.assertEqual(self.codec.encode([1,2,3]), 'li1ei2ei3ee', 'invalid list encoding')
    
    def test_encode_complex(self):
        self.assertEqual(self.codec.encode(
                dict(string="value", list=[1, 'foo'], nested=[2, 'bar', dict(hello="world")])),
                'd4:listli1e3:fooe6:nestedli2e3:bard5:hello5:worldee6:string5:valuee'
            )
    
    def test_encode_unsupported(self):
        try:
            self.codec.encode(u"foo")
        
        except bencode.EncodeError:
            pass
        
        except:
            self.fail()
    
    def test_decode_simple(self):
        self.assertEqual(self.codec.decode('4:spam'), 'spam')
        self.assertEqual(self.codec.decode('i3e'), 3)
        self.assertEqual(self.codec.decode('l4:spam4:eggse'), ['spam', 'eggs'])
        self.assertEqual(self.codec.decode('d3:cow3:moo4:spam4:eggse'), dict(cow="moo", spam="eggs"))
    
    def test_decode_complex(self):
        self.assertEqual(self.codec.decode('d4:spaml1:a1:bee'), dict(spam=['a', 'b']))
    
    def test_decode_failure(self):
        try:
            self.codec.decode("foo")
        
        except bencode.DecodeError:
            pass
        
        except:
            self.fail()


class TestEnhancedBencoder(TestCase):
    def setUp(self):
        self.codec = bencode.EnhancedBencode()

    def test_encode_simple(self):
        self.assertEqual(self.codec.encode((1, 2)), 'ti1ei2ee', 'invalid tuple encoding')
        self.assertEqual(self.codec.encode(2.0), 'f2.000000e', 'invalid float encoding')
        self.assertEqual(self.codec.encode(None), 'n', 'invalid encoding of None')
        self.assertEqual(self.codec.encode(set([1, 2])), 'si1ei2ee', 'invalid set encoding')
        self.assertEqual(self.codec.encode(u"hello"), 'u5:hello', 'invalid unicode encoding')
    
    def test_encode_unsupported(self):
        from datetime import datetime
        
        try:
            self.codec.encode(datetime.now())
        
        except bencode.EncodeError:
            pass
        
        except:
            self.fail()
    
    def test_decode_simple(self):
        self.assertEqual(self.codec.decode('ti1ei2ee'), (1, 2))
        self.assertEqual(self.codec.decode('f2.000000e'), 2.0)
        self.assertEqual(self.codec.decode('n'), None)
        self.assertEqual(self.codec.decode('si1ei2ee'), set([1, 2]))
        self.assertEqual(self.codec.decode('u5:hello'), u"hello")
