import warnings
warnings.warn(
        'Access to the common template interface via the "cti" package has been deprecated.\n'
        'Update your imports to reference "alacarte" instead.',
        DeprecationWarning
    )

import alacarte.core
from alacarte.core import *

__all__ = alacarte.core.__all__
