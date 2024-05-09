import subprocess
import concurrent.futures

# Define a function to run the script with the given arguments
def run_script_with_args(args):
    script_path = 'detection_v8_api_args.py'
    subprocess.run(['python', script_path, args[0], args[1], args[2]])

# Read the arguments from the file and create a list of argument sets
args_list = []
with open('cameras.txt', 'r') as file:
    for line in file:
        args = line.split()
        if len(args) == 3:  # Ensure each line contains exactly three arguments
            args_list.append(args)
        else:
            print(f"Ignoring line '{line.strip()}' as it does not contain exactly three arguments.")

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(run_script_with_args, args_list)
