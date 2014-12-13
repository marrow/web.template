# encoding: utf-8

from __future__ import unicode_literals

import sys

from unittest import TestCase

try:
	from cPickle import dumps
except ImportError:
	from pickle import dumps

from marrow.templating.core import Engines


class TestSerializers(TestCase):
	def serializer(self, engine, expected, args, kw):
		assert engine(*args, **kw) == expected, "%r != %r" % (engine(*args, **kw), expected)
	
	def test_builtin_serializers(self):
		render = Engines()
		tests = [
				(render.bencode, (b"foo", ),  dict(kind='basic'), (b'application/x-bencode', b'3:foo')),
				(render.bencode, ("foo", ), {}, (b'application/x-bencode', b'u3:foo')),
				(render.json,	("foo", ),  {}, (b'application/json', '"foo"')),
				(render.pickle,  ("foo", ),  {}, (b'application/octet-stream', dumps("foo"))),
				(render.cpickle, ("foo", ),  {}, (b'application/octet-stream', dumps("foo"))),
				(render.yaml,	("foo", ),  {}, (b'application/x-yaml', 'foo\n...\n'))
			]
		
		# Marshal is version-specific.
		if sys.version_info < (2, 6):
			tests.append((render.marshal, ("foo", ),  {}, (b'application/octet-stream', 't\x03\x00\x00\x00foo')))
		
		elif sys.version_info < (3, 0):
			tests.append((render.marshal, ("foo", ),  {}, (b'application/octet-stream', 's\x03\x00\x00\x00foo')))
		
		for engine, args, kw, expected in tests:
			yield self.serializer, (engine, expected, args, kw), engine.__name__
