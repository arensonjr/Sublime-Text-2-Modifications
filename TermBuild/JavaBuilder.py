from AbstractBuild import AbstractBuild
from build_main import debug

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
		# Classpath config
		cpsep = ":" if "posix" == os.name else ";"
		if "classpath" in self.settings:
			classpath = cpsep.join( self.settings[ "classpath" ] )
		else:
			classpath = "."

		if self.noPrompt:
			# Classpath is already done
			# Files to compile
			if "toCompile" in self.settings:
				self.toCompile = self.settings[ "toCompile" ]
				if "*.java" in self.toCompile:
					self.toCompile.remove( "*.java" )
					self.toCompile.extend( filter( lambda x: x.endswith( '.java' ), os.listdir( '.' ) ) ) # TODO: MAKE THIS RECURSIVELY SEARCH DIRS
				self.toCompile.append( self.filenameOnly + ".java" )
			else:
				self.toCompile = filter( lambda x: x.endswith( '.java' ), os.listdir( '.' ) ) # TODO: MAKE THIS RECURSIVELY SEARCH DIRS

		else: # prompt
			# Classpath
			morePath = raw_input( "Space-separated classpath: " )
			if morePath != "":
				classpath += cpsep + cpsep.join( morePath.split() )
				self.settings[ "classpath" ] = classpath.split( cpsep )

			# Files to compile
			toCompile = raw_input( "Space-separated list to compile in addition to " + self.filenameOnly + " (spacebar for none)? [*.java] " )
			if toCompile != "":
				# Only the files they ask for
				self.toCompile = toCompile.split()
				if "*.java" in self.toCompile:
					self.toCompile.remove( "*.java" )
					self.toCompile.extend( filter( lambda x: x.endswith( '.java' ), os.listdir( '.' ) ) ) # TODO: MAKE THIS RECURSIVELY SEARCH DIRS
				self.toCompile.append( self.filenameOnly + ".java" )
			else:
				self.toCompile = filter( lambda x: x.endswith( '.java' ), os.listdir( '.' ) )
			self.settings[ "toCompile" ] = self.toCompile

		os.environ[ "CLASSPATH" ] = classpath

	def setRunOpts( self ):
		"""
		Configure the run-time options (heap size, etc.)
		"""
		if self.noPrompt:
			# Heap Size
			if "heapSize" in self.settings:
				heapSize = self.settings[ "heapSize" ]
				self.runOpts.extend( [ "-Xms" + heapSize, "-Xmx" + heapSize ] )

		else: # prompt
			# Heap Size
			heapSize = raw_input( "Heap size (e.g. 700M, 1.5G): [default] " )
			if heapSize != "":
				self.runOpts.append( "-Xmx" + heapSize )
				self.runOpts.append( "-Xms" + heapSize )
				self.settings[ "heapSize" ] = heapSize

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
