from models import RawData, RawDataKeys, ExitValue, Diff, TestResult

class Comparator():
    def __init__(self, dataref, datacomp):
        self.dataref = dataref
        self.datacomp = datacomp

    def compare(self):
        comp_results = []
        for result_ref in self.dataref[RawDataKeys().results_key]:
            try:
                result_comp = self.pair(result_ref)
            except Exception as e:
                print(f'Could not pair results for {result_ref[RawDataKeys().result_input_file_path_key]}. Skipping')

            data_ref = RawData.from_result(result_ref)
            data_comp = RawData.from_result(result_comp)

            result = TestResult(
                data_ref.path,
                Comparator.make_exit_diff(data_ref, data_comp),
                Comparator.make_diffs(data_ref, data_comp),
            )
            comp_results.append(result)

        return comp_results

    def pair(self, ref):
        for result in self.datacomp[RawDataKeys().results_key]:
            if (result[RawDataKeys().result_input_file_path_key] == ref[RawDataKeys().result_input_file_path_key]):
                return result
        raise Exception

    @staticmethod
    def make_diffs(data_ref, data_comp):
        diffs = []

        # Abort if one list is empty
        if not (data_ref.stats and data_comp.stats):
            return []

        ref_stat = data_ref.stats[-1]
        comp_stat = data_comp.stats[-1]

        # List common keys
        ref_keys = set(ref_stat.keys())
        comp_keys = set(comp_stat.keys())
        common_keys = sorted(ref_keys & comp_keys) # ref_keys /\ comp_keys sorted alphabtically

        for key in common_keys:
            diffs.append(Comparator.make_diff(key, ref_stat[key], comp_stat[key]))

        return diffs

    @staticmethod
    def make_exit_diff(data_ref, data_comp):
        return Comparator.make_diff('Exit value', data_ref.exit.time, data_comp.exit.time)

    @staticmethod
    def make_diff(label: str, reference: float, value: float):
        diff = value - reference
        variation = Comparator.compute_variation(reference, value, diff)
        return Diff(label, reference, value, diff, variation)

    @staticmethod
    def compute_variation(reference, value, diff):
        if (reference == 0):
            if (value == 0):
                return 0
            else:
                return 100
        else:
            variation = (diff / reference) * 100

        return variation
