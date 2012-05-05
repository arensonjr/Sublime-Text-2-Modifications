# 1. Parse for input file type
# 2. Given that, open a build system class that subclasses the generic builder
#  \-- First, ask for any changes to the path and append to sys.path
# 3. Parse for command-line opts, build options, etc.
#  \-- Build system does this
# 4. Run / invoke
#  \-- Build system does this (call to subprocess library? Maybe if we want to
#      pass in stdin data, or pipe stdout to a file?)

import os
import sys
import subprocess
from termbuild_settings import DEBUG

def debug( mesg ):
	"""
	If the global var DEBUG is true, prints the message. Else, does nothing.
	"""
	if DEBUG:
		print mesg

def getBuilder( filename ):
	"""
	Returns an AbstractBuild() instance of the correct concrete implementation
	for the provided filetype.

	Raises a ValueError on an invalid extension.
	"""
	# Create the name of the build class we should be looking for
	fileExtension = filename.split( "." )[ -1 ]
	debug( "Found extension: '" + fileExtension + "'" )
	buildName = fileExtension.title() + "Builder"

	# Look for the correct filename with the correct class
	try:
		exec( "from " + buildName + " import " + buildName )
		debug( "Successfully imported " + buildName )
	except ImportError:
		raise ValueError( "Unknown Filetype: '." + fileExtension + "'" )

	# If it's not there, we raised an error. If we successfully imported it,
	# instantiate a version
	exec( "newBuilder = " + buildName + "( '" + filename + "' )" )
	return newBuilder

def setupPath():
	"""
	Adds the Sublime packages folder (with our scripts / modules in it) to the
	path.
	"""
	if "posix" == os.name:
		sys.path.append( os.environ["HOME"] + "/.config/sublime-text-2/Packages/TermBuild" )

	# TODO: Don't know if this works for windows
	elif "nt" == os.name:
		sys.path.append( os.environ["HOME"] + "/AppData/Roaming/Sublime\ Text\ 2/Packages/TermBuild " )

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
	if checkFileName( filename ):
		builder = getBuilder( filename )
		builder.getIOOpts()
		builder.buildOpts()
		builder.execute()

	raw_input( "Press [ENTER] to exit..." )


if __name__ == "__main__":
	main( sys.argv[ 1 ] )