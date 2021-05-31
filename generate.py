import datetime

# Variables
commit = '13a4c1dca0dd58d62acc741866fb945f3fe81592'

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

# Close file
file.close()
