import subprocess
import os

def get_repo_path():
    # Get absolute path to current Git repo
    try:
        repo_path = str(subprocess.check_output(['git', 'rev-parse', '--show-toplevel']))
        # Clean output
        repo_path = repo_path.lstrip("b'").rstrip("n'").rstrip('\\')
        return os.path.abspath(repo_path)
    except subprocess.CalledProcessError as e:
        print(f'Could not determine the Git repo path. Error: {e.returncode}')

def get_file_content(file_path: str, file_hash: str):
    repo_path = get_repo_path()
    relpath = os.path.relpath(file_path, repo_path)
    # Get rid of `\` on Windows
    relpath = relpath.replace('\\', '/')

    # Get file content from a relative path and a file hash
    try:
        filecontent = str(subprocess.check_output(['git', 'show', f'{file_hash}:{relpath}']))
        # Clean output
        filecontent = filecontent.lstrip("b'").rstrip("'").replace('\\n', '')
    except subprocess.CalledProcessError as e:
        print(f'Could not read {file_path} from {file_hash}. Error: {e.returncode}')

    return filecontent

def get_changed_files(path: str, commit_hash: str):
    repo_path = get_repo_path()
    # Get list of changed files in specific path for a specific commit
    try:
        output = str(subprocess.check_output(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash, path]))
        # Clean output
        output = output.lstrip("b'").rstrip("n'").rstrip('\\')
        changed_files = make_file_list(output)
        existing_files = get_existing_files(path, commit_hash)
        # Eliminate removed files that are detected as modified by Git (changed_files /\ existing_files)
        files = list(set(changed_files) & set(existing_files))
        return files
    except subprocess.CalledProcessError as e:
        print(f'Could not search for modified files in {path} for commit {commit_hash}. Error: {e.returncode}')

def get_existing_files(path: str, commit_hash: str):
    # Get list of existing files in specific path for a specific commit
    try:
        output = str(subprocess.check_output(['git', 'ls-tree', '--name-only', '-r', commit_hash, path]))
        # Clean output
        output = output.lstrip("b'").rstrip("n'").rstrip('\\')
        return make_file_list(output)
    except subprocess.CalledProcessError as e:
        print(f'Could not search for existing files in {path} for commit {commit_hash}. Error: {e.returncode}')

def make_file_list(git_output: str):
    repo_path = get_repo_path()
    files = []
    for file in git_output.split('\\n'):
        files.append(os.path.abspath(os.path.join(repo_path, file)))
    return files
