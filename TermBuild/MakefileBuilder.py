from AbstractBuild import AbstractBuild
from build_main import debug

import os

class MakefileBuilder( AbstractBuild ):
	"""
	Build system for .<extension> files. Should be invoked by build_main, not an
	end user.
	"""
	def buildOpts( self ):
		"""
		Sets a list of command-line elements usable by the commandLines()
		method.

		e.g. Java:
			self.compileOpts = [ "-cp", ".:..:/usr/include" ]
			self.runOpts = [ "-Xmx2000M" ]
		"""
		self.compileOpts = []

		if self.noPrompt:
			if "targets" in self.settings:
				self.compileOpts.extend( self.settings[ "targets" ] )
		else: # prompt
			targets = raw_input( "Space-separated targets for make: [blank for none] " )
			targets = targets.split()
			self.compileOpts.extend( targets )
			self.settings[ "targets" ] = targets

	def executable( self ):
		"""
		No executable for C files.
		"""
		return ".".join( self.filename.split( '.' )[ :-1 ] )

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
