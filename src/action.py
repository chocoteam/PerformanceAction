import argparse
import os

from main import shared_main
from filemanager import FileManager

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='Path of JSON output file to parse')
    parser.add_argument('hashref', help='Hash value of commit to compare against (reference commit)')
    parser.add_argument('hashcomp', help='Hash value of commit to compare')
    parser.add_argument('output_path', help='Path of folder to output the generated page')
    args = parser.parse_args()

    filepath = os.path.abspath(args.filepath)
    hashref = args.hashref
    hashcomp = args.hashcomp
    output_path = os.path.abspath(args.output_path)

    print(f'Your filepath: {filepath}')
    print(f'Your reference commit hash: {hashref}')
    print(f'Your commit hash to compare: {hashcomp}')
    print('-----------------------------------------------')

    # File parsing
    ref_file = FileManager(filepath, hashref)
    comp_file = FileManager(filepath, hashcomp)
    ref_content = ref_file.parse()
    comp_content = comp_file.parse()

    # Rest of the program
    shared_main(filepath, hashref, hashcomp, ref_content, comp_content, output_path)

if __name__ == "__main__":
    main()
