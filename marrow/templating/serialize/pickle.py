# encoding: utf-8

from __future__ import unicode_literals

from warnings import warn

try:
	from cPickle import dumps
except ImportError:
	from pickle import dumps


__all__ = ['render_pickle', 'render_cpickle']


def render_pickle(data, template=None, i18n=None, **kw):
	"""Serialize data using the Python pickle standard library.
	
	Accepts the same extended arguments as the pickle.dumps() function, see:
	
		https://docs.python.org/3/library/pickle.html
	
	"""
	
	return b'application/octet-stream', dumps(data, **kw)


def render_cpickle(data, template=None, i18n=None, **kw):
	"""Serialize data using the Python pickle standard library.
	
	Accepts the same extended arguments as the pickle.dumps() function, see:
	
		https://docs.python.org/3/library/pickle.html
	
	"""
	warn("Use is deprecated: will always use cPickle if present.", DeprecationWarning)
	
	return b'application/octet-stream', dumps(data, **kw)
