from AbstractBuild import AbstractBuild
from JavaBuilder import JavaBuilder
from build_main import debug

import os

class JunitBuilder( JavaBuilder ):
	"""
	Build system for JUnit TestCase classes. Should be invoked by build_main,
	not an end user.
	"""

	def executable( self ):
		"""
		Returns the executable command necessary to run this filetype.
		"""
		# TODO: Windows support?
		#...

		# Linux / Mac:
		if "posix" == os.name:
			# JUnit should be on the path
			return "junit"

	def setRunOpts( self ):
		"""
		Noop: JUnit has no runtime options.
		"""
		pass

	# commandLines() inherited from JavaBuilder
	# compiler() inherited from JavaBuilder
	# buildOpts() inherited from JavaBuilder
