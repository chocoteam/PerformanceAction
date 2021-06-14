import argparse
import os

from main import shared_main
from git import get_changed_jsons
from filemanager import FileManager

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('jsondir', help='Path of JSON directory to parse files from')
    parser.add_argument('hashref', help='Hash value of commit to compare against (reference commit)')
    parser.add_argument('hashcomp', help='Hash value of commit to compare')
    parser.add_argument('output_path', help='Path of folder to output the generated page')
    parser.add_argument('repository_url', help='URL of the tested code repository (for commit hyperlinks)')
    parser.add_argument('similar_percent_limit', help='Maximum percentage signifying similarity. It must be positive, as it will be checked for both lower and higher values. If not set, it will default to `1%`', type=float, default=1)
    args = parser.parse_args()

    jsondir = os.path.abspath(args.jsondir)
    hashref = args.hashref
    hashcomp = args.hashcomp
    output_path = os.path.abspath(args.output_path)

    print(f'Your JSON directory: {jsondir}')
    print(f'Your reference commit hash: {hashref}')
    print(f'Your commit hash to compare: {hashcomp}')
    print('-----------------------------------------------')

    changed_jsons = get_changed_jsons(jsondir, hashcomp)
    for changed_json in changed_jsons:
        # File parsing
        ref_file = FileManager(changed_json, hashref)
        comp_file = FileManager(changed_json, hashcomp)
        ref_content = ref_file.parse()
        comp_content = comp_file.parse()

        # Rest of the program
        shared_main(changed_json, ref_content, comp_content, output_path, args.repository_url, args.similar_percent_limit)

if __name__ == "__main__":
    main()
