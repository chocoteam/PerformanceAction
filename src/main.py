import argparse
import os

import filemanager

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

    print(f'Your filepath: ${filepath}')
    print(f'Your reference commit hash: ${hashref}')
    print(f'Your commit hash to compare: ${hashcomp}')
    print('-----------------------------------------------')

    # File parsing
    ref_file = filemanager.FileManager(filepath, hashref)
    comp_file = filemanager.FileManager(filepath, hashcomp)

    ref_file.parse()
    print(f'Content of ${ref_file.filepath} ${ref_file.filehash}:')
    print(ref_file.content)

    comp_file.parse()
    print(f'Content of ${comp_file.filepath} ${comp_file.filehash}:')
    print(comp_file.content)

if __name__ == "__main__":
    main()
