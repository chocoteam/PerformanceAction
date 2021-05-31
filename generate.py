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
  def __init__(self, exit_diff: Diff, diffs: List[Diff]):
    self.exit_diff = exit_diff
    self.diffs = diffs

# Variables
commit = '13a4c1dca0dd58d62acc741866fb945f3fe81592'
raw_data = [
  RawData(
    "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-03-4-rom_c18",
    [{"bound":9,"time":0},{"bound":12,"time":0}],
    ExitValue(0, "terminated"),
  ),
  RawData(
    "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-04-4-rom_c18",
    [{"bound":24,"time":0}],
    ExitValue(1, "terminated"),
  ),
  RawData(
    "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-07-4-rom_c18",
    [],
    ExitValue(-1, "failed"),
  ),
]
input_data = [
  
]

# Process input data
# TODO: Process data
processed_data = {
  "XCSP18": {
    "CrosswordDesign": {
      "CrosswordDesign-03-4-rom_c18": TestResult(
        Diff("Exit value", 0, 0, 0, 0),
        []
      ),
      "CrosswordDesign-04-4-rom_c18": TestResult(
        Diff("Exit value", 1, 1, 0, 0),
        []
      ),
      "CrosswordDesign-07-4-rom_c18": TestResult(
        Diff("Exit value", -1, -1, 0, 0),
        []
      ),
    },
    "NurseRostering": {
      "NurseRostering-17_c18": {

      },
      "NurseRostering-20_c18": {

      },
    },
    "Rlfap": {
      "Rlfap-opt": {
        "Rlfap-scen-03-opt_c18": {

        },
        "Rlfap-scen-06-opt_c18": {

        },
      },
    },
  },
  "XCSP3": {
    "Filters-ar_1_2.xml": {

    },
  },
}

# Open file
file = open("optimization.md", "w")

# Write Front Matter
file.write(f'''---
title: "Optimization benchmarks"
date: {datetime.datetime.now().astimezone().isoformat()}
weight: 1
description: >
  Benchmarks of tests ran in optimization scheme.

  Results are compared with [`{commit[0:7]}`](https://github.com/chocoteam/choco-solver/commit/{commit}).
---''')

# Writes test results to the file
def write_test_result(result: TestResult):
  diff = result.exit_diff

  # Write value
  file.write(f'\n\n**{diff.label}:** {diff.value}')
  # Write variation
  if diff.diff == 0:
    file.write(f' [=]')
  else:
    sign = '-' if diff.diff < 0 else '+'
    file.write(f' ({sign}{diff.diff} / {sign}{diff.variation}%)')

  file.write(f'\n\n<!-- TODO: Write test results diff -->')
  # TODO: Write test results diff

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
