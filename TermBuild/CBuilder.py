from AbstractBuild import AbstractBuild
from MakefileBuilder import MakefileBuilder
from build_main import debug

import os

class CBuilder( AbstractBuild ):
	"""
	Build system for .c files without a Makefile. Should be invoked by
	build_main, not an end user.
	"""
	def __init__( self, filename, settings ):
		"""
		Set default values
		"""
		AbstractBuild.__init__( self, filename, settings ) # super( filename, settings )
		self.compilerFlags = []
		self.toCompile = []


	def buildOpts( self ):
		"""
		Sets a list of command-line elements usable by the commandLines()
		method.

		e.g. Java:
			self.compileOpts = [ "-cp", ".:..:/usr/include" ]
			self.runOpts = [ "-Xmx2000M" ]
		"""
		raise NotImplementedError( "Unfinished. For now, please use a Makefile" )

		# For reference, work from Makefile found in this directory (TEMPORARY).

		# (A) outfile: default = filename - extension
		# (B) Which files do we compile? For each file:
			# (1) outfile: default = filename - extension + ".o"
			# (2) CFLAGS
			# (3) libraries: -lnsl, -lm, -lrt, etc.
			# (4) Which files does it need? Headers, object files?
		# (C) Create a makefile based on what we know?

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
			return "bcc" # ???

		# Linux / Mac:
		if "posix" == os.name:
			return "gcc"

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
		raise NotImplementedError
