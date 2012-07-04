import os
import sys
import subprocess
import time

from build_main import debug

class AbstractBuild:
	"""
	Interface for the build system handlers
	"""

	def __init__( self, filename, settings, noPrompt ):
		"""
		Set default values.
		"""
		self.stdin = sys.stdin
		self.stdout = sys.stdout
		self.filename = filename
		self.extension = filename.split( '.' )[ -1 ]
		self.settings = settings
		self.noPrompt = noPrompt

		# Isolate the filetype from the concrete class name
		self.filetype = self.__module__.replace( 'Builder', '' ).lower()
		debug( "Filetype is: '" + self.filetype + "'" )
		# Eliminate the file extension
		self.filenameOnly = "".join( self.filename.split( '.' )[ :-1 ] )
		# Eliminate the /path/to/
		self.filenameOnly = self.filenameOnly.split( os.path.sep )[ -1 ]

		# Just in case: Get in the correct directory
		os.chdir( os.path.sep.join( self.filename.split( os.path.sep )[ :-1 ] ) )

	def execute( self ):
		"""
		Once we have all of the command-line options and such, invokes the
		program using the correct syntax.
		"""
		# Essentially, just a semantic wrapper to subprocess in case we want to
		# change the execution method.
		print "==============================================================\n"

		for command in self.commandLines():
			debug( "Executing: '" + " ".join( command ) + "'" )
			try:
				subprocess.call( command, stdin=self.stdin, stdout=self.stdout )
			except OSError as e:
				print "Error during execution:", e
				print "(Command was '" + " ".join( command ) + "')"

		# If the user had output piped to a file, be nice and show them anyway
		if self.stdout != sys.stdout:
			with open( self.stdout.name, "r" ) as f:
				print f.read()
		else:
			# Keep the number of whitespace lines even
			print ""

		print "=============================================================="

	def buildOpts( self ):
		"""
		Each type of build system parses for its own command-line / build
		options (e.g. If it's C, do you want to use a Makefile? If you don't use
		a Makefile, what options do you want / what compiler do you want? Do you
		want a Makefile generated for you from this call? etc.)
		"""
		raise NotImplementedError

	def getIOOpts( self ):
		"""
		Asks the user whether they want to use the default stdin / stdout or
		whether they want to pipe from / into different files.
		"""
		if self.noPrompt:
			if "input_file" in self.settings:
				try:
					infilename = self.settings[ "input_file" ]
					infile = open( infilename, "r" )
					self.stdin = infile
				except:
					print self.settings[ "input_file" ]
					print "Could not open " + infilename + ", using stdin."

			if "output_file" in self.settings:
				try:
					outfilename = self.settings[ "output_file" ]
					outfile = open( outfilename, "w" )
					self.stdout = outfile
				except:
					print "Could not open " + outfilename + ", using stdout."

		else: # prompt
			# Get stdin
			infilename = raw_input( "Input file [blank for stdin]: " )
			if infilename != "":
				try:
					infile = open( infilename, "r" )
					self.stdin = infile
				except:
					print "Could not open " + infilename + ", using stdin."

			# Get stdout
			outfilename = raw_input( "Output file [blank for stdout]: " )
			if outfilename != "":
				try:
					outfile = open( outfilename, "w" )
					self.stdout = outfile
				except:
					print "Could not open " + outfilename + ", using stdout."

	def commandLine( self ):
		"""
		This command requires the buildOpts() and getIOOpts() methods to already
		have been run.

		Returns a bash command (list of strings) to run the specified file.
		"""
		raise NotImplementedError

	def getArgs( self ):
		"""
		Get the arguments to the file we're running (not the options to the
		runtime environment)
		"""
		if self.noPrompt:
			if "args" in self.settings:
				self.args = self.settings[ "args" ].split()
			else:
				self.args = []

		else: # prompt
			args = raw_input( "Arguments to your program? [none] " )
			if args != "":
				self.args = args.split()
			else:
				self.args = []