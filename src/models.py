from typing import List

class RawDataKeys:
    def __init__(self):
        self.results_key = 'results'
        self.result_input_file_path_key = 'name'
        self.result_stats_key = 'stats'
        self.exit_key = 'exit'
        self.exit_value_key = 'time'
        self.exit_status_key = 'status'

class ExitValue:
    def __init__(self, time: int, status: str):
        self.time = time
        self.status = status
class RawData:
    def __init__(self, path: str, stats, exit: ExitValue):
        self.path = path
        self.stats = stats
        self.exit = exit

    @staticmethod
    def from_result(result):
        keys = RawDataKeys()
        return RawData(
            path=result[keys.result_input_file_path_key],
            stats=result[keys.result_stats_key],
            exit=ExitValue(
                result[keys.exit_key][keys.exit_value_key],
                result[keys.exit_key][keys.exit_status_key],
            ),
        )

    @staticmethod
    def keys():
        return RawDataKeys()
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
class TestOutputMetadata:
    __test__ = False
    def __init__(self, test_folder_path: str, page_title: str, page_description: str, code_commit: str):
        """Some metadata used to generate the test results page.

        Args:
            test_folder_path (str): Path of folder where test input files are located. Used to remove the path prefix from absolute file paths
            page_title (str): Title of the generated Hugo page
            page_description (str): Description of the generated Hugo page
            code_commit (str): Hash of the commit used to run tests (in the main repository, where the code change originated)
        """
        self.test_folder_path = test_folder_path
        self.page_title = page_title
        self.page_description = page_description
        self.code_commit = code_commit
class PageGenSettings:
    def __init__(self, test_output_metadata: TestOutputMetadata, ref_code_commit: str, repository_url: str, similar_percent_limit: float = 1):
        """All metadata used to generate the test results page.

        Args:
            test_output_metadata (TestOutputMetadata): Metadata from test output file
            ref_code_commit (str): Hash of the commit used to run tests (in the main repository, where the code change originated)
            repository_url (str): URL of the tested code repository (for commit hyperlinks)
            similar_percent_limit (float): Maximum percentage signifying similarity.
        """
        self.test_output_metadata = test_output_metadata
        self.ref_code_commit = ref_code_commit
        self.repository_url = repository_url
        self.similar_percent_limit = similar_percent_limit
class PageGenInputData:
    def __init__(self, settings: PageGenSettings, results: List[TestResult]):
        self.settings = settings
        self.results = results