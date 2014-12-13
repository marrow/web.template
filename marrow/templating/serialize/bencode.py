# encoding: utf-8

from __future__ import unicode_literals

import sys

# from ..compat import str, unicode, native

if sys.version_info > (3, 0):
	unicode = str
	str = bytes
	native = unicode
else:
	native = str


__all__ = ['render', 'CodecError', 'EncodeError', 'DecodeError', 'Encoding', 'ChunkedEncoder', 'Bencode', 'EnhancedBencode']


def render(data, template=None, kind='enhanced', i18n=None, **kw):
	"""A bencoding serializer templating language.
	
	Accepts the same extended arguments as the JSON dumps() function, see:
	
		http://docs.python.org/library/json.html#json.dump
	
	Data may be of any datatype supported by the json standard library or simplejson.
	
	Sample usage:
	
		>>> from marrow.templating.core import Engines
		>>> render = Engines()
		>>> render.bencode(dict(hello="world"))
		('application/x-bencode', 'd5:hello5:worlde')
		
	"""
	
	codecs = dict(basic=Bencode, enhanced=EnhancedBencode)
	
	return b'application/x-bencode', codecs[kind]().encode(data)


class CodecError(Exception):
	"""Useful superclass to group all codec-related errors."""


class EncodeError(CodecError):
	"""Raised by C{Encoding} implementations if encode fails."""


class DecodeError(CodecError):
	"""Raised by C{Encoding} implementations if decode fails."""


class Encoding(object):
	"""Interface for RPC message encoders/decoders.
	
	All encoding implementations used with this library should inherit and implement this.
	"""
	
	def encode(self, data): # pragma: no cover
		"""Encode data.
		
		@param data: The data to encode.  Must, at a minimum, implement encoding of C{str}, C{int}, and C{long} values.
		
		@return: The encoded data.
		@rtype: str
		"""
		raise NotImplementedError
	
	def decode(self, data): # pragma: no cover
		"""Decode data.
		
		@param data: The data (byte string) to decode.
		@type data: str
		
		@return: The decoded data (in its correct type).
		"""
		raise NotImplementedError


class ChunkedEncoder(Encoding):
	"""A mix-in class to easily support chunked encoders."""
	
	def encode(self, data):
		try:
			return getattr(self, 'encode_' + type(data).__name__)(data)
		
		except AttributeError:
			raise EncodeError("Unable to encode a chunk of type '%s'." % (type(data), ))


class Bencode(ChunkedEncoder):
	"""Implementation of the bencode algorithm used by Bittorrent.
	
	See: http://en.wikipedia.org/wiki/Bencode
	
	Suported Values: C{str}, C{int}, C{long}, C{dict}, C{list}
	"""
	
	def decode(self, data):
		length = len(data)
		
		if length == 0: raise DecodeError("Can not decode an empty string.")
		
		data, processed = self._decode(data)
		
		if processed != length: raise DecodeError("Did not fully decode input. %d of %d processed, %d bytes remaining." % (processed, length, length - processed))
		
		return data
	
	def _decode(self, data, offset=0):
		signature = data[offset : offset + 1]
		signaturen = native(signature.decode('ascii') if hasattr(signature, 'decode') else signature)
		print('decode_' + signaturen)
		if hasattr(self, 'decode_' + signaturen):
			print("has")
			return getattr(self, 'decode_' + signaturen)(data, offset + 1)
		
		if signature.isdigit():
			print('digit')
			return self.decode_bytes(data, offset)
		
		raise DecodeError("Unable to decode unknown signature '%s'." % (signaturen, ))
	
	def encode_int(self, data):
		return b'i' + unicode(data).encode('ascii') + b'e'
	
	encode_long = encode_int
	encode_bool = encode_int
	
	def decode_i(self, data, o):
		index = data.index(b'e', o)
		return int(data[o:index]), index + 1
	
	def encode_bytes(self, data):
		return unicode(len(data)).encode('ascii') + b':' + data
	
	def decode_bytes(self, data, o):
		index = data.index(b':', o)
		length = int(data[o:index])
		offset = index + 1
		return data[offset : offset + length], offset + length
	
	if sys.version_info < (3, ):
		encode_str = encode_bytes
	
	def encode_list(self, data):
		return b'l' + b''.join([self.encode(item) for item in data]) + b'e'
	
	encode_tuple = encode_list
	
	def decode_l(self, data, o):
		offset = o
		values = []
		
		while data[offset : offset + 1] != b'e':
			value, offset = self._decode(data, offset)
			values.append(value)
		
		return values, offset + 1
	
	def encode_dict(self, data):
		processed = [(self.encode(key) + self.encode(data[key])) for key in sorted(data.keys())]
		return b'd' + b''.join(processed) + b'e'
	
	def decode_d(self, data, o):
		offset = o
		values = {}
		
		while data[offset : offset + 1] != b'e':
			key, offset = self._decode(data, offset)
			value, offset = self._decode(data, offset)
			values[key] = value
		
		return values, offset + 1


class EnhancedBencode(Bencode):
	"""Implementation of a Bencode-based algorithm.
	
	Suported Values: C{str}, C{int}, C{long}, C{dict}, C{list}, C{float}, C{None}, C{tuple}, C{set}, C{unicode}
	
	@note: This algorithm differs from the "official" Bencode algorithm in that it can encode/decode additional data types.
	"""
	
	def encode_float(self, data):
		return 'f%fe' % (data, )
	
	def decode_f(self, data, o):
		index = data.index(b'e', o)
		return float(data[o:index]), index + 1
	
	def encode_NoneType(self, data):
		return 'n'
	
	def decode_n(self, data, o):
		return None, o
	
	def encode_tuple(self, data):
		return b't' + b''.join([self.encode(item) for item in data]) + b'e'
	
	def decode_t(self, data, o):
		offset = o
		values = []
		
		while data[offset : offset + 1] != b'e':
			value, offset = self._decode(data, offset)
			values.append(value)
		
		return tuple(values), offset + 1
	
	def encode_set(self, data):
		return b's' + b''.join([self.encode(item) for item in data]) + b'e'
	
	def decode_s(self, data, o):
		offset = o
		values = []
		
		while data[offset : offset + 1] != b'e':
			value, offset = self._decode(data, offset)
			values.append(value)
		
		return set(values), offset + 1
	
	def encode_unicode(self, data):
		encoded = data.encode('utf-8')
		return b'u' + unicode(len(encoded)).encode('ascii') + b':' + encoded
	
	if sys.version_info >= (3, ):
		encode_str = encode_unicode
	
	def decode_u(self, data, o):
		index = data.index(b':', o)
		length = int(data[o:index])
		offset = index + 1
		return data[offset : offset + length].decode('utf-8'), offset + length
