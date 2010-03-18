import warnings
warnings.warn(
        'Access to the common template interface via the "cti" package has been deprecated.\n'
        'Update your imports to reference "alacarte" instead.',
        DeprecationWarning
    )

from alacarte.release import *
