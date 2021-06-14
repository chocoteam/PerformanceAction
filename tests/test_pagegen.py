import pytest
from models import PageGenInputData, Metadata, TestResult, Diff
from pagegen import generate_page

def test_with_data():
    tests_output_file_name: str = 'test_with_data.out'
    commit1: str = '13a4c1dca0dd58d62acc741866fb945f3fe81592'
    commit2: str = '614c0134750071ffe08dc376e9cc8caf210974bf'
    output_file_folder: str = './tests/.out/'
    input_data = PageGenInputData(
        Metadata(
            '/home/evaluation/evaluation/pub/bench/',
        ),
        [
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-03-4-rom_c18",
                Diff("Exit value", 0, 0, 0, 0),
                [Diff("bound", 13, 12, -1, -7.6923), Diff("time", 0, 0, 0, 0)]
            ),
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-04-4-rom_c18",
                Diff("Exit value", 1, 1, 0, 0),
                []
            ),
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-07-4-rom_c18",
                Diff("Exit value", -1, -1, 0, 0),
                []
            ),
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP18/NurseRostering/NurseRostering-17_c18",
                Diff("Exit value", -1, -1, 0, 0),
                []
            ),
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP18/NurseRostering/NurseRostering-20_c18",
                Diff("Exit value", -1, -1, 0, 0),
                []
            ),
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP18/Rlfap/Rlfap-opt/Rlfap-scen-03-opt_c18",
                Diff("Exit value", -1, -1, 0, 0),
                []
            ),
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP18/Rlfap/Rlfap-opt/Rlfap-scen-06-opt_c18",
                Diff("Exit value", -1, -1, 0, 0),
                []
            ),
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP3/Filters-ar_1_2.xml",
                Diff("Exit value", -1, -1, 0, 0),
                []
            ),
        ],
    )

    generate_page(tests_output_file_name, commit1, commit2, output_file_folder, input_data)

def test_failure_color():
    tests_output_file_name: str = 'test_failure_color.out'
    commit1: str = '13a4c1dca0dd58d62acc741866fb945f3fe81592'
    commit2: str = '614c0134750071ffe08dc376e9cc8caf210974bf'
    output_file_folder: str = './tests/.out/'
    input_data = PageGenInputData(
        Metadata(
            '/home/evaluation/evaluation/pub/bench/',
        ),
        [
            TestResult(
                '/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-03-4-rom_c18',
                Diff('Exit value 1', -1, -1, 0, 0),
                []
            ),
            TestResult(
                '/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-04-4-rom_c18',
                Diff('Exit value 2', 2, -1, -3, -150),
                []
            ),
            TestResult(
                '/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-07-4-rom_c18',
                Diff('Exit value 3', 0, -1, -1, 0),
                []
            ),
        ],
    )

    generate_page(tests_output_file_name, commit1, commit2, output_file_folder, input_data)

    f = open('./tests/.out/test_failure_color.md', 'r')
    file_content = f.read()
    assert '**Exit value 1:** `-1` <span style="color: red">⨯ (was `-1`)</span>' in file_content
    assert '**Exit value 2:** `-1` <span style="color: red">⨯ (was `2`)</span>' in file_content
    assert '**Exit value 3:** `-1` <span style="color: red">⨯ (was `0`)</span>' in file_content

def test_rounded_percentages():
    tests_output_file_name: str = 'test_rounded_percentages.out'
    commit1: str = '13a4c1dca0dd58d62acc741866fb945f3fe81592'
    commit2: str = '614c0134750071ffe08dc376e9cc8caf210974bf'
    output_file_folder: str = './tests/.out/'
    input_data = PageGenInputData(
        Metadata(
            '/home/evaluation/evaluation/pub/bench/',
        ),
        [
            TestResult(
                "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-03-4-rom_c18",
                Diff("Exit value", 0, 0, 0, 0),
                [Diff("bound", 13, 12, -1, -7.6923), Diff("time", 0, 0, 0, 0)]
            ),
        ],
    )

    generate_page(tests_output_file_name, commit1, commit2, output_file_folder, input_data)

    f = open("./tests/.out/test_rounded_percentages.md", "r")
    file_content = f.read()
    assert "7.692" not in file_content
    assert "7.69" in file_content

def test_table_hidden_if_no_result():
    tests_output_file_name: str = 'test_table_hidden_if_no_result.out'
    commit1: str = '13a4c1dca0dd58d62acc741866fb945f3fe81592'
    commit2: str = '614c0134750071ffe08dc376e9cc8caf210974bf'
    output_file_folder: str = './tests/.out/'
    input_data = PageGenInputData(
        Metadata(
            '/home/evaluation/evaluation/pub/bench/',
        ),
        [
            TestResult(
                '/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-03-4-rom_c18',
                Diff('Exit value 1', 0, 0, 0, 0),
                []
            ),
        ],
    )

    generate_page(tests_output_file_name, commit1, commit2, output_file_folder, input_data)
    f = open('./tests/.out/test_table_hidden_if_no_result.md', 'r')
    file_content = f.read()
    assert '| Measure' not in file_content
    assert '*The test generated no result.*' in file_content

def test_show_both_commits_in_description():
    tests_output_file_name: str = 'test_show_both_commits_in_description.out'
    commit1: str = '13a4c1dca0dd58d62acc741866fb945f3fe81592'
    commit2: str = '614c0134750071ffe08dc376e9cc8caf210974bf'
    output_file_folder: str = './tests/.out/'
    input_data = PageGenInputData(
        Metadata(
            '/home/evaluation/evaluation/pub/bench/',
        ),
        [],
    )

    generate_page(tests_output_file_name, commit1, commit2, output_file_folder, input_data)
    f = open('./tests/.out/test_show_both_commits_in_description.md', 'r')
    file_content = f.read()
    assert 'Results of [`614c013`](https://github.com/chocoteam/choco-solver/commit/614c0134750071ffe08dc376e9cc8caf210974bf) are compared with [`13a4c1d`](https://github.com/chocoteam/choco-solver/commit/13a4c1dca0dd58d62acc741866fb945f3fe81592).' in file_content
