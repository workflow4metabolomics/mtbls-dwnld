# vi: fdm=marker

from galaxy.datatypes import data
from galaxy.datatypes.data import Text

# ==============================================================
# ISATAB {{{1
# ==============================================================

class ISATAB(Text):
    composite_type = 'auto_primary_file'
