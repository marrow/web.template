import warnings
warnings.warn(
        'Access to the common template interface via the "cti" package has been deprecated.\n'
        'Update your imports to reference "marrow.templating" instead.',
        DeprecationWarning
    )

import marrow.templating.engines
from marrow.templating.engines import *

__all__ = marrow.templating.engines.__all__
