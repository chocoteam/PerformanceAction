import argparse
import os
import json

import comparator
from models import PageGenInputData, TestOutputMetadata, PageGenSettings
import pagegen

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('ref_file_path', help='Path to JSON file to compare against (reference file)')
    parser.add_argument('comp_file_path', help='Path to JSON file to compare')
    parser.add_argument(
        '-o',
        '--output',
        dest='output_path',
        metavar='OUTPUT_PATH',
        help='Path of folder to output the generated page',
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

    inner_main(args.ref_file_path, args.comp_file_path, args.output_path, args.similar_percent_limit)

def inner_main(ref_file_path: str, comp_file_path: str, output_path: str, similar_percent_limit: float=1):
    ref_file_path = os.path.abspath(ref_file_path)
    comp_file_path = os.path.abspath(comp_file_path)
    output_path = os.path.abspath(output_path)

    print(f'Your reference file: {ref_file_path}')
    print(f'Your file to compare: {comp_file_path}')
    print(f'Your output path: {output_path}')
    print('-' * 48)

    # File parsing
    ref_file = open(ref_file_path, 'r')
    comp_file = open(comp_file_path, 'r')
    ref_content = json.loads(ref_file.read())
    comp_content = json.loads(comp_file.read())
    ref_file.close()
    comp_file.close()

    # Rest of the program
    shared_main(comp_file_path, ref_content, comp_content, output_path, similar_percent_limit)
    print(f'Results have been written in {output_path}')

def shared_main(input_file_path: str, ref_content, comp_content, output_path: str, similar_percent_limit: float=1):
    # Comparison
    comp = comparator.Comparator(ref_content, comp_content)
    comp_results = comp.compare()

    # Result page generation
    ref_metadata = TestOutputMetadata(
        test_folder_path=ref_content["metadata"]["testFolderPath"],
        page_title=ref_content["metadata"]["pageTitle"],
        page_description=ref_content["metadata"]["pageDescription"],
        repository_url=ref_content["metadata"]["codeRepo"],
        code_commit=ref_content["metadata"]["codeCommit"],
    )
    comp_metadata = TestOutputMetadata(
        test_folder_path=comp_content["metadata"]["testFolderPath"],
        page_title=comp_content["metadata"]["pageTitle"],
        page_description=comp_content["metadata"]["pageDescription"],
        repository_url=comp_content["metadata"]["codeRepo"],
        code_commit=comp_content["metadata"]["codeCommit"],
    )
    settings = PageGenSettings(
        ref_test_metadata=ref_metadata,
        comp_test_metadata=comp_metadata,
        similar_percent_limit=similar_percent_limit,
    )
    page_gen_input_data = PageGenInputData(settings, comp_results)
    pagegen.generate_page(os.path.basename(input_file_path), output_path, page_gen_input_data)

if __name__ == "__main__":
    main()