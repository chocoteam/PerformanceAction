import subprocess
import os

def get_filecontent(filepath: str, filehash: str):
    filepath = filepath.replace('\\', '/') # Get rid of `\` on Windows

    # Get absolute path to current Git repo
    try:
        repopath = str(subprocess.check_output('git rev-parse --show-toplevel'))
            .lstrip("b'").rstrip("n'").rstrip('\\') # Clean output
    except subprocess.CalledProcessError as e:
        print(f'Could not determine the Git repo path. Error : ${e.returncode}')

    relpath = os.path.relpath(filepath, repopath)
        .replace('\\', '/') # Get rid of `\` on Windows

    # Get file content from relpath and filehash
    try:
        filecontent = str(subprocess.check_output('git show ${filehash}:${relpath}'))
            .lstrip("b'").rstrip("'").replace('\\n', '') # Clean output
    except subprocess.CalledProcessError as e:
        print(f'Could not read ${filepath} from ${filehash}. Error : ${e.returncode}')

    return filecontent
