from typing import List

class ExitValue:
    def __init__(self, time: int, status: str):
        self.time = time
        self.status = status
class RawData:
    def __init__(self, path: str, stats, exit: ExitValue):
        self.path = path
        self.stats = stats
        self.exit = exit
class Diff:
    def __init__(self, label: str, reference: float, value: float, diff: float, variation: float):
        self.label = label
        self.reference = reference
        self.value = value
        self.diff = diff
        self.variation = variation
class TestResult:
    __test__ = False
    def __init__(self, file_path: str, exit_diff: Diff, diffs: List[Diff]):
        self.file_path = file_path
        self.exit_diff = exit_diff
        self.diffs = diffs
class Metadata:
    def __init__(self, test_folder_path: str):
        self.test_folder_path = test_folder_path
class PageGenInputData:
    def __init__(self, metadata: Metadata, results: List[TestResult]):
        self.metadata = metadata
        self.results = results