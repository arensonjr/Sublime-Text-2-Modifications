import os
import sys
import subprocess

from build_main import debug

class AbstractBuild:
	"""
	Interface for the build system handlers
	"""

	def __init__( self, filename, settings ):
		"""
		Set default values.
		"""
		self.stdin = sys.stdin
		self.stdout = sys.stdout
		self.filename = filename
		self.extension = filename.split( '.' )[ -1 ]
		self.settings = settings

		# Eliminate the file extension
		self.filenameOnly = "".join( self.filename.split( '.' )[ :-1 ] )
		# Eliminate the /path/to/
		self.filenameOnly = self.filenameOnly.split( os.path.sep )[ -1 ]

		debug( "Filename = " + filename )
		if self.extension in settings:
			debug( "Found extension in settings" )
		else:
			debug( "Extension '" + self.extension + "' not in settings" )

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
			subprocess.call( command, stdin=self.stdin, stdout=self.stdout )

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
		args = raw_input( "Arguments to your program? [none] " )
		if args != "":
			self.args = args.split()
		else:
			self.args = []