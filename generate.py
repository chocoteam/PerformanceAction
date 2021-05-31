import datetime

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

# Variables
commit = '13a4c1dca0dd58d62acc741866fb945f3fe81592'
rawData = [
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
inputData = [
  
]

# Process input data
# TODO: Process data
processedData = {
  "XCSP18": {
    "CrosswordDesign": {
      "CrosswordDesign-03-4-rom_c18": {

      },
      "CrosswordDesign-06-4-rom_c18": {

      },
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

# Write headings
def write_content(path_component: str, level: int, content):
  file.write(f'\n\n{"#" * level} {path_component}')
  for key, value in content.items():
    write_content(key, level + 1, value)

# Write data
for key, value in processedData.items():
  write_content(key, 2, value)

# Write trailing new line
file.write('\n')

# Close file
file.close()
