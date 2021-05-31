import subprocess
import os

def get_filecontent(filepath,filehash):
    filepath = filepath.replace("\\","/") # to get rid of \ on Windows

    # Get absolute path to current Git repo
    try:
        repopath = str(subprocess.check_output("git rev-parse --show-toplevel")).lstrip("b'").rstrip("n'").rstrip("\\")
    except subprocess.CalledProcessError as e:
        print("Could not determine the Git repo path. Error : " + str(e.returncode))

    relpath = os.path.relpath(filepath,repopath).replace("\\","/") # to get rid of \ on Windows

    # Get file content from relpath and filehash
    try:
        filecontent = str(subprocess.check_output("git show " + filehash + ":" + relpath)).lstrip("b'").rstrip("'").replace("\\n","")
    except subprocess.CalledProcessError as e:
        print("Could not read " + filepath + " from " + filehash + ". Error : " + str(e.returncode))

    return filecontent