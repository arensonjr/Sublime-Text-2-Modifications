from AbstractBuild import AbstractBuild
from build_main import debug

import os

class PyBuilder( AbstractBuild ):
	"""
	Build system for .py files. Should be invoked by build_main, not an end
	user.
	"""

	def buildOpts( self ):
		"""
		TODO
		"""
		print "TODO: No build options for python yet."
		self.opts = []
		debug( "buildOpts: using " + str( self.opts ) )

	def executable( self ):
		"""
		Returns the executable command necessary to run a python file (e.g. 
		'python', or 'C:/Python27/python.exe')
		"""
		# TODO: Windows support?
		if "nt" == os.name:
			return "C:/Python27/python.exe"
		
		# Linux / Mac:
		if "posix" == os.name:
			# Python should be on the path
			return "python"

	def commandLines( self ):
		"""
		TODO
		"""
		# There's no compiling for python files, so we only need one command:
		commandline = [ self.executable() ] + self.opts + [ self.filename ] + self.args
		return [ commandline ]
