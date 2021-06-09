import models

class Comparator():
    def __init__(self, dataref: str, datacomp: str):
        self.dataref = dataref
        self.datacomp = datacomp

    def compare(self):
        comp_results = []
        for result_ref in self.dataref["results"]:
            try:
                result_comp = self.pair(result_ref)
            except Exception as e:
                print(f'Could not pair results for {result_ref["name"]}. Skipping')

            data_ref = models.RawData(result_ref["name"], result_ref["stats"], models.ExitValue(result_ref["exit"]["time"], result_ref["exit"]["status"]))
            data_comp = models.RawData(result_comp["name"], result_comp["stats"], models.ExitValue(result_comp["exit"]["time"], result_comp["exit"]["status"]))

            comp_results.append(models.TestResult(data_ref.path, Comparator.make_exit_diff(data_ref, data_comp), Comparator.make_diffs(data_ref, data_comp)))

        return comp_results

    def pair(self, ref):
        for result in self.datacomp["results"]:
            if (result["name"] == ref["name"]):
                return result
        raise Exception

    @staticmethod
    def make_diffs(data_ref, data_comp):
        diffs = []
        for (key, value_ref), (key2, value_comp) in zip(data_ref.stats[-1].items(), data_comp.stats[-1].items()):
            diffs.append(Comparator.make_diff(key, value_ref, value_comp))
        return diffs

    @staticmethod
    def make_exit_diff(data_ref, data_comp):
        return Comparator.make_diff("Exit value", data_ref.exit.time, data_comp.exit.time)

    @staticmethod
    def make_diff(label: str, reference: float, value: float):
        diff = reference - value
        variation = Comparator.compute_variation(reference, value, diff)
        return models.Diff(label, reference, value, diff, variation)

    @staticmethod
    def compute_variation(reference, value, diff):
        if (reference == 0):
            if (value == 0):
                return 0
            else:
                return 100
        else:
            variation = (diff / value) * 100

        return variation
