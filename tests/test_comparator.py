import pytest
import json
from typing import List

from comparator import Comparator
from models import TestResult, Diff

def test_1():
    ref_file_path = './tests/data/input/optimization1.out.json'
    comp_file_path = './tests/data/input/optimization2.out.json'
    ref_file = open(ref_file_path, 'r')
    comp_file = open(comp_file_path, 'r')
    ref_content = json.loads(ref_file.read())
    comp_content = json.loads(comp_file.read())
    ref_file.close()
    comp_file.close()

    comp = Comparator(ref_content, comp_content)
    comp_results = comp.compare()

    assert isinstance(comp_results, List)
    assert len(comp_results) == 3

    # First result
    res = comp_results[0]
    assert isinstance(res, TestResult)
    assert res.file_path == '/home/evaluation/evaluation/pub/bench/lorem/ipsum/1'
    exit_diff = res.exit_diff
    assert isinstance(exit_diff, Diff)
    assert exit_diff.label == 'Exit value'
    assert exit_diff.reference == 4
    assert exit_diff.value == 2
    assert exit_diff.diff == 2
    assert exit_diff.variation == 100
    diffs = res.diffs
    assert isinstance(diffs, List)
    assert len(diffs) == 2
    diff_bound = diffs[0]
    assert diff_bound.label == "bound"
    assert diff_bound.reference == 12
    assert diff_bound.value == 12
    assert diff_bound.diff == 0
    assert diff_bound.variation == 0
    diff_time = diffs[1]
    assert diff_time.label == "time"
    assert diff_time.reference == 2
    assert diff_time.value == 1
    assert diff_time.diff == 1
    assert diff_time.variation == 100