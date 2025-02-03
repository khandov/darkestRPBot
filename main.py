import subprocess
import statsdb.dbscript as db
def run_script(script_name):
    subprocess.run(['python', script_name])

if __name__ == "__main__":
    #db.alterDatabase()
    scripts = ['api/commands.py']
    for script in scripts:
        run_script(script)