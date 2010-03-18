import warnings
warnings.warn(
        'Access to the common template interface via the "cti" package has been deprecated.\n'
        'Update your imports to reference "alacarte" instead.',
        DeprecationWarning
    )

import alacarte.resolver
from alacarte.resolver import *

__all__ = alacarte.resolver.__all__
