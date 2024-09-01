# MyShell - Custom Unix-like Shell in Python

## Features and Functionality

### 1. Command Execution
MyShell supports executing built-in commands (`cd`, `pwd`, `var`, `exit`, `which`) and external commands found in the system's `PATH`. The `executeOtherCommands` function (in the module other_commands) is responsible for executing external commands using `os.fork()` and `os.execvp()` to create child processes and replace them with the desired command.

### 2. How does your shell translate a line of input that a user enters into a command which is executed in the command line?
The parseCommand module handles command parsing in my shell. It first checks if a command requires piping using the needPiping function from the piping module, which returns true if the command contains a "|" not enclosed in quotes. If piping is needed, I will let the handlePiping function from the piping module handles the command, the command is split using the split_by_pipe_op function, which I modified to only split on "|" outside of quotes, treating those within quotes as literal strings.

The parsed input is then passed to the processInnput function, which deals with backslashes. This function handles two cases: if a backslash is followed by ${}, it invokes the variableSubstitution logic (covered in the next section). For escaping quotes, it iterates through the input, ignores backslashes, and collects characters within quotes, then wraps the result in double quotes. This ensures that the input, when processed by shlex.split, does not raise errors, maintaining robust and error-free command parsing.

### 3. What is the logic that your shell performs to find and substitute environment variables in user input? Howdoes it handle the user escaping shell variables with a backslash (\) so that they are interpreted as literal strings?
The main logic for handling variable substitution is in the variable_substitute module, specifically in the variableSubstitution function. This function first checks if the command contains a variable to substitute using neededToSubStitute, which returns true if ${<variable_name>} is found. If substitution is needed, the function processes each element of the already split command. If an element contains a space, it is enclosed in double quotes to preserve the original structure after substitution. This is also done for elements containing variables to be substituted, ensuring the integrity of the command.

From lines 24 to 40, the function loops through the input, omitting backslashes before ${} and substituting variables using os.environ[<variable_name>]. Afterwards, it checks for mismatched quotes (lines 67-78). If an odd number of single or double quotes is detected, it adjusts them by replacing mismatched quotes, preserving the original quoting in the command and preventing parsing errors with shlex.split.

### 4. How does your shell handle pipelines as part of its execution? What logic in your program allows one command to read another command's stdout output as stdin ?

This logic is implemented in the piping module. First, I split the command using split_by_pipe_op, resulting in a list of commands to execute. I then iterate through this list, using shlex.split to parse each command. For all commands except the last one, I create a pipe with os.pipe(). Next, I duplicate the process with os.fork(). In the child process, I replace the current process with the command using os.execvp. I use os.dup2 to redirect the input from the read end of the previous pipe and the output to the write end of the current pipe. After each redirection, I close the pipe ends properly to prevent broken pipes or errors. In the parent process, os.wait() is used to wait for the child process to complete. This logic is implemented from lines 44 to 72 of the piping module.


## Testing Strategy
I implemented end-to-end tests to cover around 90% of the assignment requirements. Each built-in command is tested for basic and complex successful cases, as well as various error scenarios. Test cases are clearly named in the tests folder to indicate their purpose. A test_folder with files, subdirectories, and a students.csv file is included for testing.

The run_tests.sh script automates testing by iterating through .in files in the io_files folder, running them against the program, and redirecting outputs to .actual files. It then uses the diff command to compare these outputs with expected .out files, printing "Pass" or "Failed" accordingly.




