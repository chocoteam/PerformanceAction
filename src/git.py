import subprocess
import os

def get_repo_path():
    # Get absolute path to current Git repo
    try:
        repopath = str(subprocess.check_output(['git', 'rev-parse', '--show-toplevel']))
        # Clean output
        repopath = repopath.lstrip("b'").rstrip("n'").rstrip('\\')
        return repopath
    except subprocess.CalledProcessError as e:
        print(f'Could not determine the Git repo path. Error: {e.returncode}')

def get_filecontent(filepath: str, filehash: str):
    # Get rid of `\` on Windows
    filepath = filepath.replace('\\', '/')
    repopath = get_repo_path()
    relpath = os.path.relpath(filepath, repopath)
    # Get rid of `\` on Windows
    relpath = relpath.replace('\\', '/')

    # Get file content from relpath and filehash
    try:
        filecontent = str(subprocess.check_output(['git', 'show', f'{filehash}:{relpath}']))
        # Clean output
        filecontent = filecontent.lstrip("b'").rstrip("'").replace('\\n', '')
    except subprocess.CalledProcessError as e:
        print(f'Could not read {filepath} from {filehash}. Error: {e.returncode}')

    return filecontent

def get_changed_files(path: str, commit_hash: str):
    repopath = get_repo_path()
    # Get list of changed files in specific path for a specific commit
    try:
        files = str(subprocess.check_output(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash, path]))
        # Clean output
        files = files.lstrip("b'").rstrip("n'").rstrip('\\')
        files = files.split('\\n')
        for f in files:
            f = os.path.join(repopath, f)
        return files
    except subprocess.CalledProcessError as e:
        print(f'Could not search for modified files in {path} for commit {commit_hash}. Error: {e.returncode}')
