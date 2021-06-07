import argparse
import os

import filemanager
import comparator

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='Path of JSON output file to parse')
    parser.add_argument('hashref', help='Hash value of commit to compare against (reference commit)')
    parser.add_argument('hashcomp', help='Hash value of commit to compare')
    args = parser.parse_args()

    filepath = os.path.abspath(args.filepath)
    hashref = args.hashref
    hashcomp = args.hashcomp

    print(f'Your filepath: {filepath}')
    print(f'Your reference commit hash: {hashref}')
    print(f'Your commit hash to compare: {hashcomp}')
    print('-----------------------------------------------')

    # File parsing
    ref_file = filemanager.FileManager(filepath, hashref)
    comp_file = filemanager.FileManager(filepath, hashcomp)
    comp = comparator.Comparator(ref_file, comp_file)
    page_gen_input_data = comp.compare()

if __name__ == "__main__":
    main()
