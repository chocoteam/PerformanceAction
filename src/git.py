import subprocess
import os

def get_filecontent(filepath: str, filehash: str):
    # Get rid of `\` on Windows
    filepath = filepath.replace('\\', '/')

    # Get absolute path to current Git repo
    try:
        repopath = str(subprocess.check_output('git rev-parse --show-toplevel'))
        # Clean output
        repopath = repopath.lstrip("b'").rstrip("n'").rstrip('\\')
    except subprocess.CalledProcessError as e:
        print(f'Could not determine the Git repo path. Error: {e.returncode}')

    relpath = os.path.relpath(filepath, repopath)
    # Get rid of `\` on Windows
    relpath = relpath.replace('\\', '/')

    # Get file content from relpath and filehash
    try:
        filecontent = str(subprocess.check_output(f'git show {filehash}:{relpath}'))
        # Clean output
        filecontent = filecontent.lstrip("b'").rstrip("'").replace('\\n', '')
    except subprocess.CalledProcessError as e:
        print(f'Could not read {filepath} from {filehash}. Error: {e.returncode}')

    return filecontent
