import datetime
import os
from io import TextIOWrapper

import models

def generate_page(tests_output_file_name: str, commit1: str, commit2: str, output_file_folder: str, input_data: PageGenInputData):
    """Generates a [Hugo](https://gohugo.io/) page displaying variation between test results.

    Args:
        tests_output_file_name (str): Name of the file generated when running tests
        commit1 (str): Hash value of reference commit for test results variation
        commit2 (str): Hash value of compared commit (actual one)
        output_file_folder (str): Path of the folder where the page should be written
        input_data (PageGenInputData): Data used for page generation
    """

    # Process data for later usage
    processed_data = __process_input_data(input_data)

    # Create new file
    file = __open_page_file(tests_output_file_name, output_file_folder)

    # Write Hugo Front Matter
    __write_front_matter(file, commit1)

    # Create file content
    for key, value in processed_data.items():
        __write_content(file, key, 2, value)

    # Write trailing new line
    file.write('\n')

    # Close file
    file.close()

def __process_input_data(input_data: PageGenInputData):
    """Processes input data to put it in a more useful shape for page generation.

    Args:
        input_data (PageGenInputData): Data used for page generation

    Returns:
        dict: The processed data as a nested dictionary with path components as keys and test results as values.
    """

    # Create empty dictionary
    processed_data = {}

    # Get file path prefix to remove when generating the dictionary structure
    prefix = input_data.metadata.test_folder_path

    # Populate the dictionary
    for test_result in input_data.results:
        # Remove file path prefix
        file_path: str = test_result.file_path.removeprefix(prefix)

        # Split file path in components
        # Note: Tests are run on Linux, so it's ok to split on `/`
        components = file_path.split('/')

        # Create folder structure
        nested = processed_data
        for component in components[:-1]:
            # Add component if it doesn't exist
            if component not in nested:
                nested[component] = {}
            # Go one level deeper
            nested = nested[component]

        # Store test result in last folder
        nested[components[-1]] = test_result

    return processed_data

def __open_page_file(tests_output_file_name: str, output_file_folder: str):
    """Opens a file for writing the page (overwrites existing file).

    Args:
        tests_output_file_name (str): Name of the file generated when running tests
        output_file_folder (str): Path of the folder where the page should be written

    Returns:
        TextIOWrapper: The page file
    """

    output_file_name = os.path.splitext(tests_output_file_name)[0]+'.md'
    output_file_path = os.path.join(output_file_folder, output_file_name)
    return open(output_file_path, "w")

def __write_front_matter(file: TextIOWrapper, reference_commit: str):
    """Writes [Hugo Front Matter](heading) in a file.

    Args:
        file (TextIOWrapper): A file
        reference_commit (str): Hash value of reference commit for test results variation
    """

    file.write(f'''---
title: "Optimization benchmarks"
date: {datetime.datetime.now().astimezone().isoformat()}
weight: 1
description: >
  Benchmarks of tests ran in optimization scheme.

  Results are compared with [`{reference_commit[0:7]}`](https://github.com/chocoteam/choco-solver/commit/{reference_commit}).
---''')

def __write_variation(file: TextIOWrapper, diff: Diff):
    """Writes variation in a readable way.

    Args:
        file (TextIOWrapper): A file
        diff (Diff): A diff object describing the variation
    """

    def span(color: str, content: str):
        return f'<span style="color: {color}">{content}</span>'

    if diff.diff == 0:
        file.write(span('#005C94', '='))
    else:
        sign = '+' if diff.diff > 0 else ''
        # FIXME: Unhardcode limit
        if diff.variation < -1:
            icon = '↘︎'
            color = 'green'
        elif diff.variation > 1:
            icon = '↗︎'
            color = 'red'
        else:
            icon = '≈'
            color = '#005C94'
        file.write(span(color, f'{icon} `{sign}{diff.diff}` (`{sign}{diff.variation}%`)'))

def __write_test_result(file: TextIOWrapper, result: TestResult):
    """Writes test results to the file.

    Args:
        file (TextIOWrapper): A file
        result (TestResult): The tests results to write
    """

    diff = result.exit_diff

    # Write value
    file.write(f'\n\n**{diff.label}:** `{diff.value}` ')
    # Write variation
    __write_variation(file, diff)

    # Write diff table
    file.write(f'''\n\nEvolution of last results:

| Measure | Reference | Value | Variation |
| ------- | --------- | ----- | --------- |''')

    for diff in result.diffs:
        file.write(f'\n| `{diff.label}` | `{diff.reference}` | `{diff.value}` | ')
        __write_variation(file, diff)
        file.write(' |')

def __write_content(file: TextIOWrapper, heading: str, level: int, content: dict):
    """Writes headings to the file.

    Args:
        file (TextIOWrapper): A file
        heading (str): The heading of this content section
        level (int): The heading level of this content section
        content (dict): A nested dictionary containing path components as keys and TestResult as values
    """

    file.write(f'\n\n{"#" * level} {heading}')
    if isinstance(content, TestResult):
        __write_test_result(file, content)
    else:
        for key, value in content.items():
            __write_content(file, key, level + 1, value)
