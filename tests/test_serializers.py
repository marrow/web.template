# encoding: utf-8

import sys

from functools import partial
from unittest import TestCase

from marrow.templating.core import Engines


def serializer(engine, expected, *args, **kw):
    assert engine(*args, **kw) == expected, "%r != %r" % (engine(*args, **kw), expected)


def test_builtin_serializers():
    render = Engines()
    
    tests = [
            (render.bencode, ("foo", ),  dict(kind='basic'), ('application/x-bencode', '3:foo')),
            (render.bencode, (u"foo", ), {}, ('application/x-bencode', 'u3:foo')),
            (render.json,    ("foo", ),  {}, ('application/json', '"foo"')),
            (render.pickle,  ("foo", ),  {}, ('application/octet-stream', "S'foo'\np0\n.")),
            (render.cpickle, ("foo", ),  {}, ('application/octet-stream', "S'foo'\np1\n.")),
            (render.yaml,    ("foo", ),  {}, ('application/x-yaml', 'foo\n...\n'))
        ]
    
    # Marshal is version-specific.
    if sys.version_info < (2, 6):
        tests.append((render.marshal, ("foo", ),  {}, ('application/octet-stream', 't\x03\x00\x00\x00foo')))
    
    elif sys.version_info < (3, 0):
        tests.append((render.marshal, ("foo", ),  {}, ('application/octet-stream', 's\x03\x00\x00\x00foo')))
    
    for engine, args, kw, expected in tests:
        yield partial(serializer, engine, expected, *args, **kw)


# class TestSerializers(TestCase):
#     def setUp(self):
#         self.render = Engines()
#     
#     def test_simplejson(self):
#         json_ = sys.modules['json']
#         sys.modules['json'] = None
#         
#         if 'marrow.templating.serialize.json_' in sys.modules:
#             del sys.modules['marrow.templating.serialize.json_']
#         
#         self.assertEqual(self.render.json("foo"), ('application/json', '"foo"'))
#         
#         sys.modules['json'] = json_
