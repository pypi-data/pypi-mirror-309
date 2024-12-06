import subprocess

# Start a Python subprocess with pipes for stdin, stdout, and stderr
proc = subprocess.Popen(
    ['python', '-i'],  # '-i' opens Python in interactive mode
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

def execute_in_subprocess(code_chunk):
    # Write the code chunk to the stdin of the subprocess
    proc.stdin.write(code_chunk + '\n')
    proc.stdin.flush()
    
    # Capture the output from stdout
    output = []
    while True:
        line = proc.stdout.readline()
        if line == '':  # Break if output ends
            break
        output.append(line)
    return ''.join(output)

# Example usage:
print(execute_in_subprocess('a = 5'))
print(execute_in_subprocess('print(a)'))  # Should output 5
