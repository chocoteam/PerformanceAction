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
    def __init__(self, test_folder_path: str, page_title: str, page_description: str, repository_url: str, similar_percent_limit: float = 1):
        """Some metadata used to generate the test results page.

        Args:
            test_folder_path (str): Path of folder where test input files are located. Used to remove the path prefix from absolute file paths
            page_title (str): Title of the generated Hugo page
            page_description (str): Description of the generated Hugo page
            repository_url (str): URL of the tested code repository (for commit hyperlinks)
            similar_percent_limit (float): Maximum percentage signifying similarity.
        """
        self.test_folder_path = test_folder_path
        self.page_title = page_title
        self.page_description = page_description
        self.repository_url = repository_url
        self.similar_percent_limit = similar_percent_limit
class PageGenInputData:
    def __init__(self, metadata: Metadata, results: List[TestResult]):
        self.metadata = metadata
        self.results = results