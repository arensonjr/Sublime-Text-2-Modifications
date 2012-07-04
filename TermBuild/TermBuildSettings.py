settings = {
	### Per-file basis:

	### Filetype defaults:
	# Note that commenting out any of these lines will cause the program to
	# prompt you for the properties at runtime.
	"py":
	{
		# Uncomment this line to read input from the file "in.txt"
		# "input_file": "in.txt",

		# Uncomment this line to send your output to "out.txt"
		# "output_file": "out.txt",
	},

	"java":
	{
		# Default classpath (must be a list) - I highly suggest putting your junit jar on this path!
		# DEFAULT: ['.']
		"classpath": [ "." ]
	},

	"junit":
	{
		# Default classpath (must be a list) - I highly suggest putting
		# your junit jar on this path!
		# DEFAULT: ['.']
		"classpath": [ ".", "/home/arensonjr/files/downloads/linstall/junit-4.10.jar", "D:\\downloads\linstall\junit-4.10.jar" ]
		# TODO: Look up how junit is invoked in linux (`which junit`) so I can emulate it for windows
	},

	### File-specific settings
	"/home/arensonjr/classes/sof/comp215/hw2/DoubleVectorTester.java": {'classpath': ['.', '/home/arensonjr/files/downloads/linstall/junit-4.10.jar', 'D', '\\downloads\\linstall\\junit-4.10.jar', 'sparsearray.jar'], 'toCompile': ['ADoubleVector.java', 'DenseDoubleVector.java', 'DoubleVectorTester.java', 'IDoubleVector.java', 'IIndexedData.java', 'ISparseArray.java', 'OutOfBoundsException.java', 'SparseDoubleVector.java']},

	# Overall DEBUG setting for the whole plugin
	"DEBUG": False
}
