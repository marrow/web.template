import warnings
warnings.warn(
        'Access to the common template interface via the "cti" package has been deprecated.\n'
        'Update your imports to reference "marrow.templating" instead.',
        DeprecationWarning
    )

from marrow.templating.release import *
