echo $1

FILENAME="$1"
if [[ -z "FILENAME" ]]; then
	echo "ERROR: No filename provided."
	exit 1
fi

# Get the file extension of the input:
extension()
{
	# ${ evaluate what's in here }
	# ${ 1: the input parameter }
	# ${ 1##: match the longest version of the following regex }
	# ${ 1##*.: match the longest string followed by at least one period }
	echo ${1##*.}
}

FILE_EXTENSION=`extension $FILENAME`

echo "Filename is: \"$FILENAME\", extension: \"$FILE_EXTENSION\""

if [[ "$FILE_EXTENSION" == "py" ]]; then
	./PythonBuild.bash "$FILENAME"
elif [[ "$FILE_EXTENSION" == "java" ]]; then
	./JavaBuild.bash "$FILENAME"
elif [[ "$FILE_EXTENSION" == "c" ]]; then
	./CBuild.bash "$FILENAME"
elif [[ "$FILE_EXTENSION" == "sh" ]]; then
	./ShellBuild.bash "$FILENAME"
else
	echo "Unsupported file extension: $FILE_EXTENSION"
fi

##############################################################################

echo "================================"
echo "Going to file directory..."
echo "    $ dirname \"$FILENAME\""
cd `dirname "$FILENAME"`
echo ""

echo "================================"
echo "Compiling..."
echo "    $ make all"
make all
echo ""

echo "================================"
echo "Running..."
echo "------------------------ EXECUTION BEGINS"
echo ""
echo "    $ ./`basename "$FILENAME" .c`"
echo ""
echo "------------------------ EXECUTION ENDS"


echo "Output stored in " # ...

### I'll include this for an "easy exit"; no closing the window necessary.
read -p "Press enter to exit..." JUNKVAR
