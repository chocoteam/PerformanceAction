import datetime

# Classes
class ExitValue:
  def __init__(self, time: int, status: str):
    self.time = time
    self.status = status
class InputData:
  def __init__(self, path: str, stats, exit: ExitValue):
    self.path = path
    self.stats = stats
    self.exit = exit

# Variables
commit = '13a4c1dca0dd58d62acc741866fb945f3fe81592'
rawData = [
  InputData(
    "filepath",
    [
      {
        "bound":9,
        "time":0
      },
      {
        "bound":12,
        "time":2
      },
    ],
    ExitValue(3, "terminated"),
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

# Write data
for key, value in processedData.items():
  file.write(f'\n\n## {key}')

# Write trailing new line
file.write('\n')

# Close file
file.close()
