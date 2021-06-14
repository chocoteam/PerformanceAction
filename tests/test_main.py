import pytest
import os
from main import inner_main

def test_the_program_runs():
    inner_main(
        ref_file_path='./tests/data/input/optimization1.out.json',
        comp_file_path='./tests/data/input/optimization2.out.json',
        output_path='./tests/.out/',
        repository_url='https://github.com/chocoteam/choco-solver',
    )

    assert os.path.exists('./tests/.out/optimization2.out.md')

def test_second_file_metadata_used_for_page_generation():
    inner_main(
        ref_file_path='./tests/data/input/legacy_optimization.out.json',
        comp_file_path='./tests/data/input/new_optimization.out.json',
        output_path='./tests/.out/',
        repository_url='https://github.com/chocoteam/choco-solver',
    )

    f = open('./tests/.out/new_optimization.out.md', 'r')
    file_content = f.read()
    assert 'A new title' in file_content
    assert 'A new description.' in file_content
