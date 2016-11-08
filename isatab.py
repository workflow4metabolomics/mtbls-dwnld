# vi: fdm=marker

# This file should be placed in `lib/galaxy/datatypes`.

from galaxy.datatypes import data
from galaxy.datatypes.data import Text

# ==============================================================
# ISATab {{{1
# ==============================================================

class ISATab(Text):
	"""ISA-Tab composite dataset class for Galaxy"""

	composite_type = 'auto_primary_file'
	file_ext = "isatab"

	# Constructor {{{2
	# ----------------

	def __init__(self, **kwd):
		Text.__init__(self, **kwd)

		# Add investigation file
		self.add_composite_file('i_Investigation.txt', description = 'ISA-Tab investigation file.', optional = 'False', is_binary = False)

		# TODO Read investigation file and search study files and assay files ?

		# Add study files
		self.add_composite_file('s_*.txt', description = 'ISA-Tab study files.', optional = 'False', is_binary = False)

		# Add assay files
		self.add_composite_file('a_*.txt', description = 'ISA-Tab assay files.', optional = 'False', is_binary = False)

	# Generate primary file {{{2
	# --------------------------

	def generate_primary_file(self, dataset = None ):
		rval = ['<html><head><title>Files for Composite Dataset (%s)</title></head><p/>This composite dataset is composed of the following files:<p/><ul>' % ( self.file_ext ) ]
		for composite_name, composite_file in self.get_composite_files( dataset = dataset ).iteritems():
			opt_text = ''
			if composite_file.optional:
				opt_text = ' (optional)'
			rval.append( '<li><a href="%s">%s</a>%s' % ( composite_name, composite_name, opt_text ) )
		rval.append( '</ul></html>' )
		return "\n".join( rval )
