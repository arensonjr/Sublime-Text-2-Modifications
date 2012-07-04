$pshost = get-host
$pswindow = $pshost.ui.rawui

$newsize = $pswindow.buffersize
$newsize.height = 3000
$newsize.width = 120
$pswindow.buffersize = $newsize

$newsize = $pswindow.windowsize
$newsize.height = 50
$newsize.width = 120
$pswindow.windowsize = $newsize

$pswindow.windowtitle = "Windows Powershell"
$pswindow.foregroundcolor = "DarkYellow"
$pswindow.backgroundcolor = "DarkMagenta"

cls

# NEW:
If( -not $args[0] -eq "" ) { # If we were given a filename:
	# Get in the right directory
	$file = Get-ChildItem $args[0]
	cd $file.DirectoryName

	# Do the main build command
	python D:/programming/github-Sublime/TermBuild/build_main.py $args[0]
} Else { # Otherwise, just open the terminal
	powershell
}