import subprocess
import db.dbscript as db

def run_script(script_name):
    subprocess.run(['python', script_name])
db.initiate()
if __name__ == "__main__":
    scripts = ['api/commands.py']
    for script in scripts:
        run_script(script)