from AbstractBuild import AbstractBuild
from build_main import debug

class PyBuilder( AbstractBuild ):
	"""
	This is just a demo version - it does *not* include full functionality!
	"""

	def buildOpts( self ):
		"""
		TODO
		"""
		print "No build options for python implemented yet."
		self.opts = []
		debug( "buildOpts: using " + str( self.opts ) )

	def executable( self ):
		"""
		Returns the executable command necessary to run a python file (e.g. 
		['python'], or 'C:/Python27/python.exe')
		"""
		# TODO: Windows support?
		# ...
		
		# Linux / Mac:
		if "posix" == os.name:
			# Python should be on the path
			return "python"

	def commandLine( self ):
		"""
		TODO
		"""
		commandline = [ 'python' ] + self.opts + [ self.filename ]
		debug( "commandLine: using " + str( commandline ) )
		return commandline
