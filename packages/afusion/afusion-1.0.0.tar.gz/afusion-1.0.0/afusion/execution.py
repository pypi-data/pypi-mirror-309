import subprocess

def run_alphafold(command):
    """
    Runs the AlphaFold Docker command and captures output.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    output_lines = []
    for line in iter(process.stdout.readline, ''):
        if line:
            output_lines.append(line)
    process.stdout.close()
    process.wait()
    return ''.join(output_lines)
