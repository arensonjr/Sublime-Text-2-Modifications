from AbstractBuild import AbstractBuild
from build_main import debug

import os

class MakefileBuilder( AbstractBuild ):
	"""
	Build system for .<extension> files. Should be invoked by build_main, not an
	end user.
	"""
	def __init__( self, filename, settings ):
		"""
		Set default values
		"""
		AbstractBuilt.__init__( self, filename, settings ) # super( filename, settings )
		self.compileOpts = []

	def buildOpts( self ):
		"""
		Sets a list of command-line elements usable by the commandLines()
		method.

		e.g. Java:
			self.compileOpts = [ "-cp", ".:..:/usr/include" ]
			self.runOpts = [ "-Xmx2000M" ]
		"""
		makeCmd = raw_input( "Command for make? [blank for none] " )
		if "" != makeCmd:
			self.compileOpts.append( makeCmd )

	def executable( self ):
		"""
		No executable for C files.
		"""
		return self.filename

	def compiler( self ):
		"""
		If applicable, returns the executable command necessary to compile this
		filetype.

		e.g. C returns:
			"make"

		e.g. Python:
			NotImplementedError
		"""
		# TODO: Windows support?
		if "nt" == os.name:
			raise NotImplementedError( "No windows support for Makefiles yet" )

		# Linux / Mac support:
		if "posix" == os.name:
			return "make"

	def commandLines( self ):
		"""
		Writes out any commands necessary (e.g. compile & run), and returns them
		as a list of lists.

		e.g. Java returns something similar to:
			[
				[ <compiler>, <options>, <files> ],
				[ <runtime>, <options>, <file> ]
			]
		"""
		lines = []
		lines.append( [ self.compiler() ] + self.compileOpts )
		lines.append( [ self.executable() ] + self.args )
		return lines
