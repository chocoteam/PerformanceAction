import pytest
from src.pagegen import generate_page, PageGenInputData, Metadata, TestResult, Diff

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
