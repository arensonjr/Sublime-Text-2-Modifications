import os
import sys
import subprocess
import time
import traceback

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

	### Special cases:
	# Java
	if extension == "java":
		# Check for junit
		with open( filename, "r" ) as f:
			for line in f.readlines():
				if "extends TestCase" in line or "@Test" in line:
					filetype = "junit"
		# Others? (java special cases)

	# C
	if extension == "c":
		# Check for existence of a makefile
		pathname = os.path.sep.join( filename.split( os.path.sep )[ :-1 ] )
		if "Makefile" in os.listdir( pathname ):
			filetype = "makefile"
		# Others? (c special cases)

	# Others? (languages with special cases)

	return filetype

def getBuilder( filename, noPrompt ):
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

	# Look for a file-specific settings file
	found = False
	if filename in settings:
		fileSettings = settings[ filename ]
		found = True
	else:
		fileSettings = {}

	# Extend w/ syntax-specific settings file
	if fileType in settings:
		syntaxSettings = settings[ fileType ]
		found = True
		for key in syntaxSettings:
			if key not in fileSettings:
				fileSettings[ key ] = syntaxSettings[ key ]
	if found == False:
		raise ValueError( "Don't have any valid settings for " + filename )

	# If it's not there, we raised an error. If we successfully imported it,
	# instantiate a version
	exec( "newBuilder = " + buildName + "( '" + filename + "', fileSettings, noPrompt )" )
	return newBuilder

def setupPath():
	"""
	Adds the Sublime packages folder (with our scripts / modules in it) to the
	path.
	"""
	if "posix" == os.name:
		settings[ "PACKAGE_DIR" ] = os.environ["HOME"] + "/.config/sublime-text-2/Packages/TermBuild"
		sys.path.append( settings[ "PACKAGE_DIR" ] )

		# Development purposes:
		# sys.path.append( os.environ["HOME"] + "/programming/github-Sublime/TermBuild" )

	# TODO: Don't know if this works for windows
	elif "nt" == os.name:
		settings[ "PACKAGE_DIR" ] = "%APPDATA%/Sublime\ Text\ 2/Packages/TermBuild"
		sys.path.append( settings[ "PACKAGE_DIR" ] )

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
	# Clear the existing keypresses:

	# Unix-only import:
	if "posix" == os.name:
		from termios import tcflush, TCIOFLUSH
		tcflush( sys.stdin, TCIOFLUSH )

	# Windows-only import:
	elif "nt" == os.name:
		import msvcrt
		while msvcrt.kbhit():
			msvcrt.getch()

	# Actual prompt to exit (which they can't hit ENTER early for!)
	raw_input( "Press [ENTER] to exit..." )

def saveOpts( settingsToSave, filename ):
	"""
	Saves a settings dictionary to our settings file, so that it's present the
	next time they want to run this file.
	"""
	# Should we save?
	yesOrNo = raw_input( "Would you like to save your settings for later? [Y|n] " )
	if yesOrNo.strip().lower() in [ "n", "no" ]:
		return

	settingsFilename = settings[ "PACKAGE_DIR" ] + os.path.sep + "TermBuildSettings.py"
	with open( settingsFilename, "r" ) as f:
		fullTxt = f.read()

	quotedFilename = "\"" + filename + "\": "
	if ( quotedFilename + "{" ) in fullTxt:
		# Find its old settings by start & end index
		bracketCount = 1
		start = fullTxt.index( quotedFilename + "{" )
		print "\tFound it at " + str( start )
		end = start + len( quotedFilename ) + 3 # first char after bracket
		while bracketCount != 0:
			if fullTxt[ end ] == "{":
				bracketCount += 1
			if fullTxt[ end ] == "}":
				bracketCount -= 1
			end += 1

		# Generate new settings
		newSettings = quotedFilename + str( settingsToSave )
		fullTxt = fullTxt[ :start ] + newSettings + fullTxt[ end: ]

	else:
		# Append the old settings onto the end
		insertAfter = "### File-specific settings\n"
		insertPos = fullTxt.index( insertAfter ) + len( insertAfter )

		newSettings = quotedFilename + str( settingsToSave )
		fullTxt = fullTxt[ :insertPos ] + "\t" + newSettings + ",\n" + fullTxt[ insertPos: ]

	with open( settingsFilename, "w") as f:
		f.write( fullTxt )


def main( argv ):
	"""
	Builds and executes whatever source file we are passed in on the command
	line.

	Raises an exception if we do not have logic in place to deal with the
	provided file type.
	"""
	# Extract the filename
	if argv[ 1 ] == "--noprompt":
		noPrompt = True
		filename = argv[ 2 ]
	else:
		noPrompt = False
		filename = argv[ 1 ]

	# Add the Sublime packages folder we need onto our path
	setupPath()

	# Check for a valid extension:
	try:
		if checkFileName( filename ):
			try:
				builder = getBuilder( filename, noPrompt )
				builder.getIOOpts()
				builder.buildOpts()
				builder.getArgs()

				# If we've prompted for options, save them now
				if not noPrompt:
					saveOpts( builder.settings, filename )

				builder.execute()
			except ValueError as e: 
				print "Unrecognized filetype: " + getFiletype( filename )
				debug( "\tError was: \"" + e.message + "\"" )
	except KeyboardInterrupt:
		time.sleep( 1 ) # Let it print its own error message before we hit the screen
		print "\nExecution interrupted.\n"
	except NotImplementedError as e:
		print "\n", e
	except Exception as e:
		print "Something went wrong: \"" + e.message + "\""
		print traceback.print_exc()

	exitSequence()


if __name__ == "__main__":
	main( sys.argv )
