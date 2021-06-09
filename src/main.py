import argparse
import os

import filemanager
import comparator
import models
import pagegen

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
    ref_content = ref_file.parse()
    comp_content = comp_file.parse()

    # Comparison
    comp = comparator.Comparator(ref_content, comp_content)
    comp_results = comp.compare()

    # Result page generation
    page_gen_input_data = models.PageGenInputData(models.Metadata(ref_content["metadata"]["testFolderPath"]), comp_results)
    pagegen.generate_page(os.path.basename(filepath), hashref, hashcomp, ".out", page_gen_input_data)

if __name__ == "__main__":
    main()
