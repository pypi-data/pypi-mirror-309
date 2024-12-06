import unittest, os
import onkopus as op
import adagenes as ag


class TestCLIAnnotation(unittest.TestCase):

    def test_stream_based_annotation_revel(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + "/../test_files/somaticMutations.ln50.vcf"
        outfile = __location__ + "/../test_files/somaticMutations.ln50" + ".revel.vcf"

        client = op.ClinVarClient(genome_version="hg38")

        ag.process_file(infile, outfile, client, genome_version="hg19")

