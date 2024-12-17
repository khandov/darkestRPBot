import subprocess
import statsdb.dbscript as db
import registerCommands
def run_script(script_name):
    subprocess.run(['python', script_name])
db.initiate()
if __name__ == "__main__":
    scripts = ['registerCommands.py']
    for script in scripts:
        run_script(script)