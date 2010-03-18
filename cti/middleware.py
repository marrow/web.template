import warnings
warnings.warn(
        'The Common Template Interface middleware has been deprecated and moved into WebCore.\n'
        'Update your imports to reference "web.extras.templating" instead.',
        DeprecationWarning
    )

import web.extras.templating
from web.extras.templating import *

__all__ = web.extras.templating.__all__
