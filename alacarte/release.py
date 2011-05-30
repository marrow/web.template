# encoding: utf-8

import warnings
warnings.warn(
        'Access to the common template interface via the "alacarte" package has been deprecated.\n'
        'Update your imports to reference "marrow.templating" instead.',
        DeprecationWarning
    )

import marrow.templating.release
from marrow.templating.release import *

__all__ = marrow.templating.release.__all__
