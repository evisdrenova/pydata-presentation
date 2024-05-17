import subprocess

# Prepare the Benthos subprocess
process = subprocess.Popen(
    ['benthos', '-c', 'config.yaml'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

# Function to send data to Benthos and receive the processed output
def process_data(data):
    process.stdin.write(data + '\n')
    process.stdin.flush()  # Ensure Benthos receives the data
    return process.stdout.readline().strip()  # Read the processed output

# Example usage
output = process_data("hello world")
print(output)  # Should print "HELLO WORLD" if using the example Benthos config

# Don't forget to close the process when done
process.stdin.close()
process.wait()
