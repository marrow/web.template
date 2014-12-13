# encoding: utf-8

from __future__ import unicode_literals

from pprint import pformat
from unittest import TestCase

from marrow.templating.util import Cache


class TestCommonUsage(TestCase):
    def setUp(self):
        self.cache = Cache(3)
        
        self.cache['A'] = 0
        self.cache['B'] = 1
        self.cache['C'] = 2
    
    def test_basic(self):
        assert pformat(self.cache) == pformat({'A': 0, 'B': 1, 'C': 2})
        assert len(self.cache) == 3
        assert self.cache['A'] == 0
    
    def test_overflow(self):
        self.cache['D'] = 3
        
        assert len(self.cache) == 3
        assert 'A' not in self.cache
        
    def test_sort(self):
        self.cache['E'] = 4
        self.cache['B']
        
        assert [i for i in self.cache] == ['B', 'E', 'C']
    
    def test_reassignment(self):
        self.cache['A'] = 5
        assert self.cache['A'] == 5
        assert [i for i in self.cache] == ['A', 'C', 'B']
        
        self.cache['C'] = 6
        assert self.cache['C'] == 6
        assert [i for i in self.cache] == ['C', 'A', 'B']

    def test_capacity(self):
        self.cache.capacity = 1
        self.cache._restrict()
        
        assert len(self.cache) == 1
        assert 'A' not in self.cache
        assert 'C' in self.cache
        
        self.cache['A'] = 0
        assert len(self.cache) == 1
        assert 'A' in self.cache
        assert 'C' not in self.cache
        
        self.cache.capacity = 0
        self.cache._restrict()
        
        assert len(self.cache) == 0
