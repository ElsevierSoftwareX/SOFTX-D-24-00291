from subprocess import run
from sys import argv
from os import path
from shutil import rmtree

# Constants for the source directory path, for the build directory path and for the options of the "sphinx-build" command.
# - They can be changed from the command line.
SOURCEDIR = "source"
BUILDDIR = "build"
SPHINX_OPTIONS = ""

def _run_os_command(command_and_args):
    run(command_and_args, check=True, shell=True)

def clean_command():
    # Delete SOURCEDIR/project_files subdirectory.
    if path.isdir(SOURCEDIR + "/project_files"):
        rmtree(SOURCEDIR + "/project_files")
    # Delete build subdirectory.
    if path.isdir(BUILDDIR):
        rmtree(BUILDDIR)

def sphinx_build_command(M_option):
    # The "M_option" parameter cannot be an empty string.
    if not M_option: # If empty string.
        raise ValueError("The 'M_option' parameter cannot be an empty string.")
    # List of "sphinx-build" options (apart from -M option).
    other_options = SPHINX_OPTIONS
    other_options = [elem for elem in other_options if elem != ""] # Delete the empty elements.
    # Run the corresponding command.
    _run_os_command(["sphinx-build", "-M", M_option] + other_options + [SOURCEDIR, BUILDDIR])

# Entry point of the python script.
if __name__ == "__main__":
    # Get the command and the arguments.
    arguments_without_program_name = argv[1:] # The first element in "sys.argv" is the program name.
    # Parse them.
    if (len(arguments_without_program_name) >= 1):
        if (arguments_without_program_name[0] == "clean"): # clean command.
            clean_command()
        else: # sphinx-build with a value for -M option (maybe valid or maybe not).
            sphinx_build_command(arguments_without_program_name[0])
    else: # The script has been called without arguments.
        sphinx_build_command("help")
