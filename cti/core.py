import warnings
warnings.warn(
        'Access to the common template interface via the "cti" package has been deprecated.\n'
        'Update your imports to reference "marrow.templating" instead.',
        DeprecationWarning
    )

import marrow.templating.core
from marrow.templating.core import *

__all__ = marrow.templating.core.__all__
