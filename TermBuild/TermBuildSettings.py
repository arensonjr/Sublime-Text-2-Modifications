settings = {
	"defaults":
	{
		# Any filetype can have 
		"py":
		{
			# Use stdin, not a filename
			# DEFAULT: None
			"input_file": None,

			# Use stdout, not a filename
			# DEFAULT: None
			"output_file": None
		},

		"java":
		{
			# Default classpath (must be a list) - I highly suggest putting
			# your junit jar on this path!
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
		}
	},

	# Overall DEBUG setting for the whole plugin
	# DEFAULT: False
	"DEBUG": False
}
