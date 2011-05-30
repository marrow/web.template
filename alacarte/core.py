# encoding: utf-8

import warnings
warnings.warn(
        'Access to the common template interface via the "alacarte" package has been deprecated.\n'
        'Update your imports to reference "marrow.render" instead.',
        DeprecationWarning
    )

import marrow.render.core
from marrow.render.core import *

__all__ = marrow.render.core.__all__
