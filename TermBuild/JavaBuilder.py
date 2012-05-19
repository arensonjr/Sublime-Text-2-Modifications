from AbstractBuild import AbstractBuild
from build_main import debug, settings

import os
import subprocess

class JavaBuilder( AbstractBuild ):
	"""
	Build system for .java files. Should be invoked by build_main, not an end
	user.
	"""

	def buildOpts( self ):
		"""
		Sets a list of command-line elements usable by the commandLines()
		method.
		"""
		self.compileOpts = []
		self.runOpts = []

		self.setCompileOpts()
		self.setRunOpts()

	def setCompileOpts( self ):
		"""
		Configure the compile-time options (classpath, files, etc.)
		"""
		# Classpath
		# Windows & Linux have different classpath separators
		cpsep = ":" if "posix" == os.name else ";"
		classpath = cpsep.join( settings[ "defaults" ][ self.filetype ][ "classpath" ] )
		morePath = raw_input( "Add (space-separated) locations to classpath: [" + classpath + "] " )
		if morePath != "":
			classpath += cpsep + cpsep.join( morePath.split() )
		os.environ[ "CLASSPATH" ] = classpath 


		# self.compileOpts.extend( [ "-cp", "." ] ) # os.environ[ "CLASSPATH" ] + ":" + os.getcwd() ] )
		# self.runOpts.extend( [ "-cp", "." ] ) # os.environ[ "CLASSPATH" ] + ":" + os.getcwd() ] )

		# Files to compile
		toCompile = raw_input( "Space-separated list to compile in addition to " + self.filenameOnly + " (spacebar for none)? [*.java] " )
		if toCompile != "":
			# Only the files they ask for
			self.toCompile = toCompile.split()
			self.toCompile.append( self.filenameOnly + ".java" )
		else:
			self.toCompile = filter( lambda x: x.endswith( '.java' ), os.listdir( '.' ) )

	def setRunOpts( self ):
		"""
		Configure the run-time options (heap size, etc.)
		"""
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
		# Windows:
		if "nt" == os.name:
			return "java"

		# Linux / Mac:
		if "posix" == os.name:
			# Java should be on the path
			return "java"

	def compiler( self ):
		"""
		Returns the build command necessary to compile the Java files.
		"""
		# TODO: Windows support?
		if "nt" == os.name:
			try:
				os.stat( "C:/Program Files/Java/jdk1.6.0_29/bin/javac.exe" )
				return "C:/Program Files/Java/jdk1.6.0_29/bin/javac.exe"
			except:
				raise NotImplementedError( "I don't know where javac is." )

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
