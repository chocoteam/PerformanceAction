# GitHub Action to generate test results summary page

![Python version](https://img.shields.io/badge/python-3.8-informational)

This repository is a drop-off location for test results of [choco-solver](https://github.com/chocoteam/choco-solver). When files are committed in [`data/`](./data/), they are compared with older versions (when appropriate) and an overview page is generated on [Choco's website](https://choco-solver.org/docs/Benchmarks/). This allows quick overview of regressions or problems in the code.

---

## Table Of Contents

- [Table Of Contents](#table-of-contents)
- [Usage](#usage)
  - [From a GitHub action](#from-a-github-action)
  - [On your computer](#on-your-computer)
- [Input file format](#input-file-format)
- [Generated page](#generated-page)
- [Contribute](#contribute)
  - [Run tests](#run-tests)
- [Maintainance notice](#maintainance-notice)

---

## Usage

The program can be used in different ways: from a GitHub Action or on a local machine.

### From a GitHub action

1. Commit a test results file ([see format](#input-file-format))
2. Update the test results file
3. Run `python action.py`

   <details>
     <summary>Tip: Run <code>python action.py -h</code> for help about required arguments.</summary>

     ```text
     usage: action.py [-h] -d TRACKED_DIR -o OUTPUT_PATH [--limit SIMILAR_PERCENT_LIMIT] hash_ref hash_comp

     positional arguments:
       hash_ref              Hash value of commit to compare against (reference commit)
       hash_comp             Hash value of commit to compare

     optional arguments:
       -h, --help            show this help message and exit
       -d TRACKED_DIR, --directory TRACKED_DIR
                             Path to directory to check for changes
       -o OUTPUT_PATH, --output OUTPUT_PATH
                             Path of folder to output the generated page
       --limit SIMILAR_PERCENT_LIMIT
                             Maximum percentage signifying similarity. It must be positive, as it will be checked for both lower and higher values. If not set, it
                             will default to 1%
     ```

   </details>

### On your computer

1. Create two test results files ([see format](#input-file-format))
2. Run `python main.py`

   <details>
     <summary>Tip: Run <code>python main.py -h</code> for help about required arguments.</summary>

     ```text
     usage: main.py [-h] -o OUTPUT_PATH [--limit SIMILAR_PERCENT_LIMIT] ref_file_path comp_file_path

     positional arguments:
       ref_file_path         Path to JSON file to compare against (reference file)
       comp_file_path        Path to JSON file to compare

     optional arguments:
       -h, --help            show this help message and exit
       -o OUTPUT_PATH, --output OUTPUT_PATH
                             Path of folder to output the generated page
       --limit SIMILAR_PERCENT_LIMIT
                             Maximum percentage signifying similarity. It must be positive, as it will be checked for both lower and higher values. If not set, it
                             will default to 1%
     ```

   </details>

## Input file format

The test results files must be formatted in JSON. They have a simple structure:

- A `"metadata"` key corresponding to metadata used for generating the page. Its structure is:
  - `"testFolderPath"`: Path of folder where test input files are located. Used to remove the path prefix from absolute file paths
  - `"pageTitle"`: Title of the generated Hugo page
  - `"pageDescription"`: Description of the generated Hugo page
  - `"codeRepo"`: URL of the tested code repository (for commit hyperlinks)
  - `"codeCommit"`: Hash of the commit used to run tests (in the main repository, where the code change originated)
- A `"results"` key corresponding to an array of test results

What we call a "test result" is the result of a test run with an input file.
The path to this input file must be unique as it determines the way the test result will be displayed on the website.

<details>
<summary>Here is an example test result file.</summary>

```json
{
    "metadata": {
        "testFolderPath": "/home/evaluation/evaluation/pub/bench/",
        "pageTitle": "Optimization benchmarks",
        "pageDescription": "Benchmarks of tests ran in optimization scheme.",
        "codeCommit": "13a4c1dca0dd58d62acc741866fb945f3fe81592"
    },
    "results": [
        {
            "name": "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-03-4-rom_c18",
            "stats": [{"bound":9,"time":0},{"bound":12,"time":0}],
            "exit": {"time": 0, "status": "terminated"}
        },
        {
            "name": "/home/evaluation/evaluation/pub/bench/XCSP18/CrosswordDesign/CrosswordDesign-06-4-rom_c18",
            "stats": [{"bound":30,"time":9},{"bound":36,"time":9},{"bound":38,"time":9},{"bound":40,"time":10},{"bound":44,"time":10},{"bound":48,"time":148},{"bound":52,"time":221}],
            "exit": {"time": -1, "status": "stop"}
        },
        {
            "name": "/home/evaluation/evaluation/pub/bench/XCSP18/NurseRostering/NurseRostering-17_c18",
            "stats": [],
            "exit": {"time": -1, "status": "failed"}
        },
        {
            "name": "/home/evaluation/evaluation/pub/bench/XCSP18/NurseRostering/NurseRostering-20_c18",
            "stats": [],
            "exit": {"time": -1, "status": "failed"}
        },
        {
            "name": "/home/evaluation/evaluation/pub/bench/XCSP18/Rlfap/Rlfap-opt/Rlfap-scen-03-opt_c18",
            "stats": [{"bound":32,"time":36},{"bound":30,"time":68},{"bound":28,"time":93},{"bound":26,"time":139},{"bound":24,"time":157},{"bound":22,"time":180},{"bound":20,"time":221},{"bound":18,"time":260}],
            "exit": {"time": -1, "status": "stop"}
        },
        {
            "name": "/home/evaluation/evaluation/pub/bench/XCSP18/Rlfap/Rlfap-opt/Rlfap-scen-05-opt_c18",
            "stats": [{"bound":792,"time":5}],
            "exit": {"time": 5, "status": "terminated"}
        }
    ]
}
```

</details>

More examples can be found under [`tests/data/input/`](./tests/data/input/).

As you can see in the above example, test results consist of a JSON object containing the path to the input file, the results found and the exit data.

Results found are JSON objects with arbitrary structure. As of now, results look like `{"bound":792,"time":5}`, but the keys are not interpreted by this action. This means the shape of this object can change over time, and the generated page will always stay as relevant.

## Generated page

The generated page is meant to be used in [Choco's website](https://choco-solver.org). The website, maintained under [chocoteam/website](https://github.com/chocoteam/website), uses [Hugo](https://gohugo.io) as a static site generator. The generated page is therefore a [Markdown](https://en.wikipedia.org/wiki/Markdown) file with YAML [Front Matter](https://gohugo.io/content-management/front-matter/).

It lists all input files used by a test suite, nesting them depending on their file path.

<!-- TODO: Insert example screenshot -->

---

## Contribute

### Run tests

1. Install [`pytest`](https://docs.pytest.org/en/6.2.x/getting-started.html#install-pytest)
2. Run `pytest` or `python -m pytest` in project folder

---

## Maintainance notice

This repository is the result of a school project at IMT Atlantique Nantes. It was designed to stop after 6 weeks, and will not be maintained by its original creators in the future. For more information, please contact [@cprudhom](https://github.com/cprudhom).
