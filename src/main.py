import argparse
import os

import filemanager

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path to json to parse")
    parser.add_argument("hashref", help="commit hash to reference json")
    parser.add_argument("hashcomp", help="commit hash to compare with")
    args = parser.parse_args()

    filepath = os.path.abspath(args.filepath)
    hashref = args.hashref
    hashcomp = args.hashcomp

    print("Your filepath : " + filepath)
    print("Your reference commit hash : " + hashref)
    print("Your commit hash to compare with : " + hashcomp)
    print("-----------------------------------------------")

    # File parsing
    ref_file = filemanager.FileManager(filepath,hashref)
    comp_file = filemanager.FileManager(filepath,hashcomp)

    ref_file.parse()
    print("Content of " + ref_file.filepath + " " + ref_file.filehash)
    print(ref_file.content)

    comp_file.parse()
    print("Content of " + comp_file.filepath + " " + comp_file.filehash)
    print(comp_file.content)

if __name__ == "__main__":
    main()