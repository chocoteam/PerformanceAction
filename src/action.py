import argparse
import os

from main import shared_main
from git import get_changed_files, get_existing_files
from filemanager import FileManager

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('hash_ref', help='Hash value of commit to compare against (reference commit)')
    parser.add_argument('hash_comp', help='Hash value of commit to compare')
    parser.add_argument(
        '-d',
        '--directory',
        metavar='TRACKED_DIR',
        dest='tracked_dir',
        help='Path to directory to check for changes',
        required=True,
    )
    parser.add_argument(
        '-o',
        '--output',
        dest='output_path',
        metavar='OUTPUT_PATH',
        help='Path of folder to output the generated page',
        required=True,
    )
    parser.add_argument(
        '--code-repo',
        metavar='REPOSITORY_URL',
        dest='repository_url',
        help='URL of the tested code repository (for commit hyperlinks)',
        required=True,
    )
    parser.add_argument(
        '--limit', 
        metavar='SIMILAR_PERCENT_LIMIT',
        dest='similar_percent_limit',
        help='Maximum percentage signifying similarity. It must be positive, as it will be checked for both lower and higher values. If not set, it will default to 1%%',
        type=float,
        default=1,
    )
    args = parser.parse_args()
    # python src/action.py 57287e71 39f252ba -d ./data/ -o ./.out --code-repo https://github.com/chocoteam/choco-solver

    tracked_dir = os.path.abspath(args.tracked_dir)
    hash_ref = args.hash_ref
    hash_comp = args.hash_comp
    output_path = os.path.abspath(args.output_path)

    print(f'Your tracked directory: {tracked_dir}')
    print(f'Your reference commit hash: {hash_ref}')
    print(f'Your commit hash to compare: {hash_comp}')
    print(f'Your output path: {output_path}')
    print('-' * 48)

    # Establish which files to compare
    changed_files = get_changed_files(tracked_dir, hash_comp) # list of changed files in commit hash_comp
    existing_files = get_existing_files(tracked_dir, hash_ref) # list of existing files in commit hash_ref
    common_files = list(set(changed_files) & set(existing_files)) # changed_files /\ existing_files

    if common_files:
        print(f'Comparing {len(common_files)} file(s)…')
        for file_path in common_files:
            print(f'- {file_path}')

            # File parsing
            ref_file = FileManager(file_path, hash_ref)
            comp_file = FileManager(file_path, hash_comp)
            ref_content = ref_file.parse()
            comp_content = comp_file.parse()

            # Rest of the program
            shared_main(file_path, ref_content, comp_content, output_path, args.repository_url, args.similar_percent_limit)

        print('-' * 48)
        print(f'Results have been written in {output_path}')
    else:
        print('No file to compare')

if __name__ == "__main__":
    main()
