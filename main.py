import subprocess

def run_script(script_name):
    subprocess.run(['python', script_name])

if __name__ == "__main__":
    scripts = ['dbscript.py', 'commands.py']
    for script in scripts:
        run_script(script)