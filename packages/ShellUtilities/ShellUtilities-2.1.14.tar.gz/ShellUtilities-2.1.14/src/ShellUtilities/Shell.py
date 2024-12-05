import subprocess
import logging
import time
from ShellUtilities.ShellCommandException import ShellCommandException
from ShellUtilities.ShellCommandResults import ShellCommandResults, AsynchronousShellCommandResults
import os
import json
import platform
from unittest.mock import patch
import sys


logger = logging.getLogger(__name__)


def __execute_shell_command(command, env, cwd, executable=None, shell=True, ):
    # Create the process and wait for the exit
    process, executable = __execute_shell_command_async(command, env, cwd, executable, shell)
    (stdout, stderr) = process.communicate()
    exitcode = process.returncode

    # The stderr and stdout are byte objects... lets change them to strings
    stdout = stdout.decode()
    stderr = stderr.decode()

    # Sanitize the variables and remove trailing newline characters
    stdout = stdout.rstrip("\n")
    stderr = stderr.rstrip("\n")

    return exitcode, stdout, stderr, executable


def __execute_shell_command_async(command, env, cwd, executable=None, shell=True, ):

    if type(command) == list:
        args = command
    elif type(command) == str:  
        args = [command]
    else:
        raise Exception(f"Specifying a command of type {type(command)} is not supported.")
    kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "shell": shell,
        "close_fds": 'posix',
    }
    if executable:
        logger.debug(f"Executable set to: {executable}")
        kwargs["executable"] = executable
    if env:
        logger.debug(f"Environment set to: " + os.linesep + json.dumps(env, indent = 4))
        kwargs["env"] = env
    if cwd:
        logger.debug(f"CWD set to: {cwd}")
        kwargs["cwd"] = cwd

    # Define a monkey patch so we can determien the executable being invoked
    # 
    # Note: We have to do this patch because there is simply no other way.
    # Additionally, the different operating systems will behave differently
    # so the logic is pretty inconsistent. Basically, if Shell=True, then
    # a shell is invoked and does the magic of resolving paths in the event
    # we use a shothand name rather than full path. If Shell is not specified,
    # the low level OS dependent wrapper written in C takes over. Windows will 
    # do some of its own magic and Linux will not do any resolving. I.e. Windows
    # will infer the executable from the args using the PATH and linux will blow
    # up if a full path is not specified
    determined_executable = None
    original_method = None
    patch_method = None 
    system_name = platform.system()
    patch_called = False
    original_method = sys.audit
    def patch_method(*args, **kwargs):
        nonlocal executable
        nonlocal determined_executable
        # The python subprocess module does a lot of black magic behind the scenes... 
        # If no executable was passed explicitly, its possible the executable was 
        # set in the args and we can parse it out
        if not executable:
            for arg in args:
                if arg and type(arg) == str and arg != "subprocess.Popen":
                    determined_executable = arg.split(" ")[0]
                    break
        else:
            determined_executable = executable
        
        # Additionally OS may do some magic to determine the full path
        # to the executable being invoked. Essentially, the platform will lookup
        # the executable in the $PATH variable or equivalent. As such, we will need
        # to do some additional magic to figure out where this is.
        # We will need to do this call on the original function so our patch is not 
        # applied. As such we will set a flag and wait until later to do this.
        #
        # But the OS may also blow up and complain that the exe could not be found
        # This will trigger an error and we will never get here.
        nonlocal patch_called
        patch_called = True
        return original_method(*args, **kwargs)

    # Create the process using the patch
    process = None
    with patch("sys.audit", side_effect=patch_method, autospec=True) as mock_bar:
        process = subprocess.Popen(*args, **kwargs)    
    
    logger.debug("Process opened.")
    if determined_executable == None:
        logger.warning("Unable to determine the executable used by the process.")
    else:
        # It's possible the executable path was determined right away           
        # if not, we can do some hacky black magic to identify the path to the executable
        if os.path.exists(determined_executable):
            logger.debug(f"Executable determined to be: {determined_executable}")
            executable = determined_executable
        else:
            if system_name == "Windows":
                search_tool = "where"
            else:
                search_tool = "/usr/bin/which"
            try:
                executable_path = subprocess.Popen([search_tool, determined_executable], stdout=subprocess.PIPE,).communicate()[0].strip().decode()
                if executable_path:
                    determined_executable = executable_path
                    logger.debug(f"Executable determined to be: {determined_executable}")
                    executable = determined_executable
                else:
                    logger.warning(f"Search tool '{search_tool}' was unable to determine the executable given the name '{determined_executable}'.")
            except:
                logger.warning("An error occurred while looking up executable path. Likely the search tool was incorrect.")
                
    return process, executable


def execute_shell_command(command, max_retries=1, retry_delay=1, env=None, cwd=None, blocking=True, executable=None, shell=True, async_buffer_funcs={}):

    try:

        if cwd and not os.path.isdir(cwd):
            raise Exception("The working directory '{0}' does not exist.".format(cwd))

        logger.debug("Running shell command:")
        logger.debug(command)

        for i in range(0, max_retries):

            # Run the shell command
            if blocking:
                exitcode, stdout_string, stderr_string, executable = __execute_shell_command(command, env, cwd, executable, shell)
            else:
                process, executable = __execute_shell_command_async(command, env, cwd, executable, shell)
                return AsynchronousShellCommandResults(command, executable, process, async_buffer_funcs)

            # If successful, return the results
            if exitcode == 0:
                logger.debug("Command STDOUT:")
                for line in stdout_string.split("\n"):
                    if line:
                        logger.debug(line)
                logger.debug("Command STDERR:")
                for line in stderr_string.split("\n"):
                    if line:
                        logger.error(line)
                return ShellCommandResults(command, executable, stdout_string, stderr_string, exitcode)

            # If an error occurred we need to determine if this is the last retry attempt
            last_retry = i == max_retries - 1

            # If it is not the last retry we must determine whether or not we can ignore the error
            # To do this we must see if our retry conditions have been satisfied
            if not last_retry:
                logger.debug("Retrying...(%s)" % i)
                time.sleep(retry_delay)
                continue
            else:
                err_msg = "Maximum retries (%s) exceeded for shell command."
                err_msg += " An error will be generated."
                logger.error(err_msg % max_retries)
                logger.error("Stdout:")
                for line in stdout_string.split("\n"):
                    logger.error(line)
                logger.error("Stderr:")
                for line in stderr_string.split("\n"):
                    logger.error(line)
                logger.error("Exit code: {0}".format(exitcode))

                raise ShellCommandException(command, stdout_string, stderr_string, exitcode)

    except Exception as ex:
        raise Exception("An error occurred while executing the shell command.") from ex
