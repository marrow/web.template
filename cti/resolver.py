import warnings
warnings.warn(
        'Access to the common template interface via the "cti" package has been deprecated.\n'
        'Update your imports to reference "alacarte" instead.',
        DeprecationWarning
    )

import marrow.templating.resolver
from marrow.templating.resolver import *

__all__ = marrow.templating.resolver.__all__
