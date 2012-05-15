"""
The template class in this file should help you in writing your own build
systems. Good luck, enjoy, and thanks for using TermBuild!
"""

from AbstractBuild import AbstractBuild
from build_main import debug

import os

class CBuilder( AbstractBuild ):
	"""
	Build system for .c files without a Makefile. Should be invoked by
	build_main, not an end user.
	"""
	self.compilerFlags = []


	def buildOpts( self ):
		"""
		Sets a list of command-line elements usable by the commandLines()
		method.

		e.g. Java:
			self.compileOpts = [ "-cp", ".:..:/usr/include" ]
			self.runOpts = [ "-Xmx2000M" ]
		"""
		raise NotImplementedError

		# self.outfile = [default] filename - extension

	def executable( self ):
		"""
		Returns the executable command necessary to run this filetype.

		e.g. Python on Windows returns:
			"C:\\Python27\\python.exe"
		"""
		# For C, everything compiles down to an executable --> no runtime
		# needed. commandLines() doesn't even call this method.
		raise NotImplementedError( "You don't need a runtime environment for C" )

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
