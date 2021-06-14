import argparse
import os
import json

import comparator
from models import PageGenInputData, Metadata
import pagegen

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('ref_file_path', help='Path to JSON file to compare against (reference file)')
    parser.add_argument('comp_file_path', help='Path to JSON file to compare')
    parser.add_argument('output_path', help='Path of folder to output the generated page')
    parser.add_argument('repository_url', help='URL of the tested code repository (for commit hyperlinks)')
    parser.add_argument('similar_percent_limit', help='Maximum percentage signifying similarity. It must be positive, as it will be checked for both lower and higher values. If not set, it will default to `1%`', type=float, default=1)
    args = parser.parse_args()

    inner_main(args.ref_file_path, args.comp_file_path, args.output_path, args.repository_url)

def inner_main(ref_file_path: str, comp_file_path: str, output_path: str, repository_url: str):
    ref_file_path = os.path.abspath(ref_file_path)
    comp_file_path = os.path.abspath(comp_file_path)
    output_path = os.path.abspath(output_path)

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
    shared_main(comp_file_path, 'hashref', 'hashcomp', ref_content, comp_content, output_path, repository_url)

def shared_main(input_file_path: str, hashref: str, hashcomp: str, ref_content, comp_content, output_path: str, repository_url: str):
    # Comparison
    comp = comparator.Comparator(ref_content, comp_content)
    comp_results = comp.compare()

    # Result page generation
    metadata = Metadata(
        test_folder_path=comp_content["metadata"]["testFolderPath"],
        page_title=comp_content["metadata"]["pageTitle"],
        page_description=comp_content["metadata"]["pageDescription"],
        repository_url=repository_url,
    )
    page_gen_input_data = PageGenInputData(metadata, comp_results)
    pagegen.generate_page(os.path.basename(input_file_path), hashref, hashcomp, output_path, page_gen_input_data)

if __name__ == "__main__":
    main()