import argparse
import os
import json

import comparator
import models
import pagegen

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('ref_file_path', help='Path to JSON file to compare against (reference file)')
    parser.add_argument('comp_file_path', help='Path to JSON file to compare')
    parser.add_argument('output_path', help='Path of folder to output the generated page')
    args = parser.parse_args()

    ref_file_path = os.path.abspath(args.ref_file_path)
    comp_file_path = os.path.abspath(args.comp_file_path)
    output_path = os.path.abspath(args.output_path)

    print(f'Your reference file: {ref_file_path}')
    print(f'Your file to compare: {comp_file_path}')
    print('-----------------------------------------------')

    # File parsing
    ref_file = open(ref_file_path, 'r')
    comp_file = open(comp_file_path, 'r')
    ref_content = json.loads(ref_file.read())
    comp_content = json.loads(comp_file.read())
    ref_file.close()
    comp_file.close()

    # Rest of the program
    shared_main(ref_file_path, 'hashref', 'hashcomp', ref_content, comp_content, output_path)

def shared_main(input_file_path, hashref, hashcomp, ref_content, comp_content, output_path):
    # Comparison
    comp = comparator.Comparator(ref_content, comp_content)
    comp_results = comp.compare()

    # Result page generation
    page_gen_input_data = models.PageGenInputData(models.Metadata(ref_content["metadata"]["testFolderPath"]), comp_results)
    pagegen.generate_page(os.path.basename(input_file_path), hashref, hashcomp, output_path, page_gen_input_data)

if __name__ == "__main__":
    main()