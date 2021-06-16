import argparse
import os

from main import shared_main
from git import get_changed_files, get_existing_files
from filemanager import FileManager

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('trackeddir', help='Path to tracked directory to check for changes')
    parser.add_argument('hashref', help='Hash value of commit to compare against (reference commit)')
    parser.add_argument('hashcomp', help='Hash value of commit to compare')
    parser.add_argument('output_path', help='Path of folder to output the generated page')
    parser.add_argument('repository_url', help='URL of the tested code repository (for commit hyperlinks)')
    parser.add_argument('similar_percent_limit', help='Maximum percentage signifying similarity. It must be positive, as it will be checked for both lower and higher values. If not set, it will default to `1%`', type=float, default=1)
    args = parser.parse_args()

    trackeddir = os.path.abspath(args.trackeddir)
    hashref = args.hashref
    hashcomp = args.hashcomp
    output_path = os.path.abspath(args.output_path)

    print(f'Your tracked directory: {trackeddir}')
    print(f'Your reference commit hash: {hashref}')
    print(f'Your commit hash to compare: {hashcomp}')
    print('-----------------------------------------------')

    # Establish which files to compare
    changed_files = get_changed_files(trackeddir, hashcomp) # list of changed files in commit hashcomp
    existing_files = get_existing_files(trackeddir, hashref) # list of existing files in commit hashref
    common_files = list(set(changed_files) - (set(changed_files) - set(existing_files))) # changed_files /\ existing_files

    if common_files:
        print(f'Comparing {len(common_files)} file(s):')
        for filepath in common_files:
            print(f'- {filepath}')

            # File parsing
            ref_file = FileManager(filepath, hashref)
            comp_file = FileManager(filepath, hashcomp)
            ref_content = ref_file.parse()
            comp_content = comp_file.parse()

            # Rest of the program
            shared_main(filepath, ref_content, comp_content, output_path, args.repository_url, args.similar_percent_limit)

        print('-----------------------------------------------')
        print(f'Results have been written in {output_path}')
    else:
        print('No file to compare')

if __name__ == "__main__":
    main()
