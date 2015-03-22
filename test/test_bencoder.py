# encoding: utf-8

from __future__ import unicode_literals

from unittest import TestCase

from web.template.serialize import bencode



class TestBasicBencoder(TestCase):
	def setUp(self):
		self.codec = bencode.Bencode()
	
	def encode(self, value, expected, failure_reason=None):
		assert self.codec.encode(value) == expected, failure_reason
	
	def decode(self, value, expected, failure_reason=None):
		assert self.codec.decode(value) == expected, failure_reason
	
	def test_encode_simple(self):
		for value, expected in (
					(b'str', b'3:str'),
					(2, b'i2e'),
					(0x80000000, b'i2147483648e'),
					(dict(name=b"value"), b'd4:name5:valuee'),
					([1,2,3], b'li1ei2ei3ee'),
				):
			yield self.encode, (value, expected), 'invalid {0} encoding'.format(type(value).__name__)
	
	def test_encode_complex(self):
		self.encode(
				{b'string': b"value", b'list': [1, b'foo'], b'nested': [2, b'bar', {b'hello': b"world"}]},
				b'd4:listli1e3:fooe6:nestedli2e3:bard5:hello5:worldee6:string5:valuee'
			)
	
	def test_encode_unsupported(self):
		try:
			result = self.codec.encode("foo")
		except bencode.EncodeError:
			return
		assert result == 'CANARY', "Failed to raise EncodeError."
	
	def test_decode_simple(self):
		for value, expected, kind in (
					(b'4:spam', b'spam', 'bytestring'),
					(b'i3e', 3, 'integer'),
					(b'l4:spam4:eggse', [b'spam', b'eggs'], 'list'),
					(b'd3:cow3:moo4:spam4:eggse', dict(cow=b"moo", spam=b"eggs"), 'dict'),
				):
			yield self.decode, (value, expected), 'invalid {0} decoding'.format(kind)
	
	def test_decode_complex(self):
		self.assertEqual(self.codec.decode(b'd4:spaml1:a1:bee'), {b'spam': [b'a', b'b']})
	
	def test_decode_failure(self):
		try:
			self.codec.decode(b"foo")
		
		except bencode.DecodeError:
			pass
		
		except:
			self.fail()


class TestEnhancedBencoder(TestCase):
	def setUp(self):
		self.codec = bencode.EnhancedBencode()
	
	def encode(self, value, expected, failure_reason=None):
		assert self.codec.encode(value) == expected, failure_reason
		
	def decode(self, value, expected, failure_reason=None):
		assert self.codec.decode(value) == expected, failure_reason
	
	def test_encode_simple(self):
		for value, expected in (
					((1, 2), b'ti1ei2ee'),
					(2.0, b'f2.000000e'),
					(None, b'n'),
					(set([1, 2]), b'si1ei2ee'),
					("hello", b'u5:hello'),
				):
			yield self.encode, (value, expected), 'invalid {0} encoding'.format(type(value).__name__)
	
	def test_encode_unsupported(self):
		from datetime import datetime
		
		try:
			self.codec.encode(datetime.now())
		
		except bencode.EncodeError:
			pass
		
		except:
			self.fail()
	
	def test_decode_simple(self):
		for value, expected in (
					(b'ti1ei2ee', (1, 2)),
					(b'f2.000000e', 2.0),
					(b'n', None),
					(b'si1ei2ee', set([1, 2])),
					(b'u5:hello', "hello")
				):
			yield self.decode, (value, expected)
