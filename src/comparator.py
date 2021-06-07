import filemanager
import models

class Comparator():
    def __init__(self, fileref: filemanager.FileManager, filecomp: filemanager.FileManager):
        self.fileref = fileref
        self.filecomp = filecomp

    def compare(self):
        self.fileref.parse()
        self.filecomp.parse()
        page_gen_input_data = models.PageGenInputData(models.Metadata("metadata"),[])
        for result_ref in self.fileref.content:
            try:
                result_comp = self.pair(result_ref)
            except Exception as e:
                print(f'Could not pair results for {result_ref["name"]}. Skipping')

            data_ref = models.RawData(result_ref["name"], result_ref["stats"], models.ExitValue(result_ref["exit"]["time"], result_ref["exit"]["status"]))
            data_comp = models.RawData(result_comp["name"], result_comp["stats"], models.ExitValue(result_comp["exit"]["time"], result_comp["exit"]["status"]))

            page_gen_input_data.results.append(models.TestResult(data_ref.path, self.make_exit_diff(data_ref, data_comp), self.make_diffs(data_ref, data_comp)))

        return page_gen_input_data

    def pair(self, ref):
        for result in self.filecomp.content:
            if (result["name"] == ref["name"]):
                return result
        raise Exception

    def make_diffs(self, data_ref, data_comp):
        diffs = []
        for index, (stat_ref, stat_comp) in enumerate(zip(data_ref.stats, data_comp.stats)):
            label = index
            reference = stat_ref["time"]
            value = stat_comp["time"]
            diff = value - reference
            variation = self.compute_variation(reference, value)
            diffs.append(models.Diff(label, reference, value, diff, variation))
        return diffs

    def make_exit_diff(self, data_ref, data_comp):
        label = "exit"
        reference = data_ref.exit.time
        value = data_comp.exit.time
        diff = value - reference
        variation = self.compute_variation(reference, value)
        return models.Diff(label, reference, value, diff, variation)

    def compute_variation(self, reference, value):
        if(reference == 0):
            variation = 1
            if(value == 0):
                variation = 0
        else:
            variation = value / reference
        return variation