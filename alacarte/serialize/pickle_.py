# encoding: utf-8

import pickle
import cPickle


__all__ = ['render_pickle', 'render_cpickle']


def render_pickle(data, template=None, i18n=None, **kw):
    """Serialize data using the Python pickle standard library.
    
    Accepts the same extended arguments as the pickle.dumps() function, see:
    
        http://www.python.org/doc/2.6/library/pickle.html#pickle.dumps
    
    """
    
    return 'application/octet-stream', pickle.dumps(data, **kw)


def render_cpickle(data, template=None, i18n=None, **kw):
    """Serialize data using the Python cPickle standard library.
    
    Accepts the same extended arguments as the pickle.dumps() function, see:
    
        http://www.python.org/doc/2.6/library/pickle.html#pickle.dumps
    
    """
    
    return 'application/octet-stream', cPickle.dumps(data, **kw)
