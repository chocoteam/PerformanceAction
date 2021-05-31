import datetime
from typing import List

# Classes
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
  def __init__(self, file_path: str, exit_diff: Diff, diffs: List[Diff]):
    self.file_path = file_path
    self.exit_diff = exit_diff
    self.diffs = diffs
class Metadata:
  def __init__(self, test_folder_path: str, output_file_name: str, commit1: str, commit2: str):
    self.test_folder_path = test_folder_path
    self.output_file_name = output_file_name
    self.commit1 = commit1
    self.commit2 = commit2
class InputData:
  def __init__(self, metadata: Metadata, results: List[TestResult]):
    self.metadata = metadata
    self.results = results

# Parameters
input_data = InputData(
  Metadata(
    '/home/evaluation/evaluation/pub/bench/',
    'optimization.out',
    '13a4c1dca0dd58d62acc741866fb945f3fe81592',
    '614c0134750071ffe08dc376e9cc8caf210974bf',
  ),
  [
    TestResult(
      "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-03-4-rom_c18",
      Diff("Exit value", 0, 0, 0, 0),
      [Diff("bound", 12, 13, -1, -7.6923), Diff("time", 0, 0, 0, 0)]
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

# Process input data
processed_data = {}
prefix = input_data.metadata.test_folder_path
for test_result in input_data.results:
  # Remove file path prefix
  file_path: str = test_result.file_path.removeprefix(prefix)

  # Split file path in components
  # Tests are run on Linux, so it's ok to split on `/`
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

# Open file
# FIXME: Unhardcode value
file = open("optimization.md", "w")

# Write Front Matter
commit = input_data.metadata.commit2
file.write(f'''---
title: "Optimization benchmarks"
date: {datetime.datetime.now().astimezone().isoformat()}
weight: 1
description: >
  Benchmarks of tests ran in optimization scheme.

  Results are compared with [`{commit[0:7]}`](https://github.com/chocoteam/choco-solver/commit/{commit}).
---''')

# Writes variation in a readable way
def write_variation(diff: Diff):
  if diff.diff == 0:
    file.write(f'[=]')
  else:
    sign = '+' if diff.diff > 0 else ''
    file.write(f'(`{sign}{diff.diff}` / `{sign}{diff.variation}%`)')

# Writes test results to the file
def write_test_result(result: TestResult):
  diff = result.exit_diff

  # Write value
  file.write(f'\n\n**{diff.label}:** `{diff.value}` ')
  # Write variation
  write_variation(diff)

  # Write diff table
  file.write(f'''\n\nEvolution of last results:

| Measure | Reference | Value | Variation |
| ------- | --------- | ----- | --------- |''')

  for diff in result.diffs:
    file.write(f'\n| `{diff.label}` | `{diff.reference}` | `{diff.value}` | ')
    write_variation(diff)
    file.write(' |')

# Writes headings to the file
def write_content(path_component: str, level: int, content):
  file.write(f'\n\n{"#" * level} {path_component}')
  if isinstance(content, TestResult):
    write_test_result(content)
  else:
    for key, value in content.items():
      write_content(key, level + 1, value)

# Create file content
for key, value in processed_data.items():
  write_content(key, 2, value)

# Write trailing new line
file.write('\n')

# Close file
file.close()
