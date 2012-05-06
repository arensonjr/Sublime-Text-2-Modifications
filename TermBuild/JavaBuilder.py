from AbstractBuild import AbstractBuild
from build_main import debug

import os

class JavaBuilder( AbstractBuild ):
	"""
	Build system for .java files. Should be invoked by build_main, not an end
	user.
	"""

	def buildOpts( self ):
		"""
		TODO
		"""
		self.compileOpts = []
		self.runOpts = []

		### COMPILE TIME OPTIONS
		# Classpath
		morePath = raw_input( "Add locations to classpath: [.] " )
		if morePath != "":
			morePath = [ "-cp", ".:" + morePath ]
			self.compileOpts.extend( morePath )
			self.runOpts.extend( morePath )

		# Files to compile
		toCompile = raw_input( "Space-separated list to compile in addition to " + self.filenameOnly + " (spacebar for none)? [*.java] " )
		if toCompile != "":
			# Only the files they ask for
			self.toCompile = toCompile.split()
			self.toCompile.append( self.filenameOnly + ".java" )
		else:
			self.toCompile = filter( lambda x: x.endswith( 'java' ), os.listdir( '.' ) )

		### RUN TIME OPTIONS
		# Heap Size
		maxHeap = raw_input( "Max heap size (e.g. 700M, 1.5G)? [default] " )
		if maxHeap != "":
			self.runOpts.append( "-Xmx" + maxHeap )
		minHeap = raw_input( "Min heap size (e.g. 700M, 1.5G)? [default] " )
		if minHeap != "":
			self.runOpts.append( "-Xms" + minHeap )

	def executable( self ):
		"""
		Returns the executable command necessary to run a Java file (e.g.
		'javac', or 'C:/<I dont know>')
		"""
		# TODO: Windows support?
		#...

		# Linux / Mac:
		if "posix" == os.name:
			# Java should be on the path
			return "java"

	def compiler( self ):
		"""
		Returns the build command necessary to compile the Java files.
		"""
		# TODO: Windows support?
		# ...

		# Linux / Mac:
		if "posix" == os.name:
			# Javac should be on the path
			return "javac"

	def commandLines( self ):
		"""
		TODO
		"""
		# Java compiling
		compileLine = [ self.compiler() ] + self.compileOpts + self.toCompile
		debug( "Compile Line: " + str( compileLine ) )

		# Java running
		runLine = [ self.executable() ] + self.runOpts + [ self.filenameOnly ] + self.args
		debug( "Run Line:     " + str( runLine ) )

		return [ compileLine, runLine ]
