""" Pipeline to run IRB approach on a given portfolio """
import luigi


class FileExists(luigi.Task):
    """
        Check that file given as input is present in the file system
    """
    # The location and file name of the dataset is passed as a parameter
    # to the pipeline
    input_file = luigi.Parameter()

    def output(self):
        """Saves the dataset locally"""
        return luigi.LocalTarget(str(self.input_file))

    def run(self):
        """ Open the file passed as parameter; if the file doesnt exist this
            will fail the FileExists luigi task. """
        open(str(self.input_file))


class ComputeRiskCapitalPerObligor(luigi.Task):
    """
        XXX
    """
