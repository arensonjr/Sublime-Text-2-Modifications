import os
import sys
import subprocess

def debug( mesg ):
	"""
	If the global var DEBUG is true, prints the message. Else, does nothing.
	"""
	if DEBUG:
		print mesg

# Import sublime settings for this module
from TermBuildSettings import settings
DEBUG = settings[ 'DEBUG' ]
debug( "Settings Dictionary: " + str( settings ) )

def getFiletype( filename ):
	"""
	Given a filename, determines its filetype. Sometimes this can be as easy as
	parsing for the extension (e.g. '.py'); other times, it can require some
	looking (e.g. differentiating between java and junit runtimes)
	"""
	# Check the basic extension; sometimes this is enough
	extension = filename.split( "." )[ -1 ]
	filetype = extension

	# Special cases:
	if extension == "java":
		# Check for junit
		with open( filename, "r" ) as f:
			for line in f.readlines():
				if "extends TestCase" in line:
					filetype = "junit"
		# Others? (java special cases)
	# Others? (special cases)

	return filetype

def getBuilder( filename ):
	"""
	Returns an AbstractBuild() instance of the correct concrete implementation
	for the provided filetype.

	Returns None on an invalid filetype (or one for which we have no build
	system).
	"""
	# Create the name of the build class we should be looking for
	# fileType = filename.split( "." )[ -1 ]
	# debug( "Found extension: '" + fileType + "'" )
	fileType = getFiletype( filename )
	buildName = fileType.title() + "Builder"

	# Look for the correct filename with the correct class
	debug( "Importing " + buildName + "..." )
	try:
		debug( "\t'from " + buildName + " import " + buildName + "'" )
		exec( "from " + buildName + " import " + buildName )
	except ImportError:
		raise ValueError( "Unrecognized filetype" )

	# If it's not there, we raised an error. If we successfully imported it,
	# instantiate a version
	exec( "newBuilder = " + buildName + "( '" + filename + "', settings )" )
	return newBuilder

def setupPath():
	"""
	Adds the Sublime packages folder (with our scripts / modules in it) to the
	path.
	"""
	if "posix" == os.name:
		sys.path.append( os.environ["HOME"] + "/.config/sublime-text-2/Packages/TermBuild" )

		# Development purposes:
		sys.path.append( os.environ["HOME"] + "/programming/github-Sublime/TermBuild" )

	# TODO: Don't know if this works for windows
	elif "nt" == os.name:
		sys.path.append( os.environ["HOME"] + "/AppData/Roaming/Sublime\ Text\ 2/Packages/TermBuild " )

	debug( "sys.path is " + str( sys.path ) )

def checkFileName( filename ):
	"""
	Returns True if the given file exists on the system; otherwise, prints an
	error message and returns False.
	"""
	try:
		os.stat( filename )
		return True
	except:
		print "Build Error: Could not find file '" + filename + "'"
		return False

def exitSequence():
	"""
	Clears stdin (so that the user doesn't accidentally hit [ENTER] one too many
	times and race through the exit screen), and then prompts for a single
	[ENTER] keystroke.
	"""
	# Unix-only import:
	if "posix" == os.name:
		# Clear the existing stdin stuff
		from termios import tcflush, TCIOFLUSH
		tcflush( sys.stdin, TCIOFLUSH )

	elif "nt" == os.name:
		# ??? TODO
		pass

	raw_input( "Press [ENTER] to exit..." )

def main( filename ):
	"""
	Builds and executes whatever source file we are passed in on the command
	line.

	Raises an exception if we do not have logic in place to deal with the
	provided file type.
	"""
	# Add the Sublime packages folder we need onto our path
	setupPath()

	# Check for a valid extension:
	try:
		if checkFileName( filename ):
			try:
				builder = getBuilder( filename )
				builder.getIOOpts()
				builder.buildOpts()
				builder.getArgs()
				builder.execute()
			except ValueError: 
				print "Unrecognized filetype: " + getFiletype( filename )
	except KeyboardInterrupt:
			time.sleep( 1 ) # Let it print its own error message
			print "\nExecution interrupted.\n"

	exitSequence()


if __name__ == "__main__":
	main( sys.argv[ 1 ] )
