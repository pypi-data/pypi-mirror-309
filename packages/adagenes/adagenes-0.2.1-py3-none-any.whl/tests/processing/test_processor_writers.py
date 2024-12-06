import unittest, os
import adagenes as ag


class AVFProcessorTestCase(unittest.TestCase):

    def test_processor_avf_writer(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + "/../test_files/somaticMutations.l100.vcf"
        outfile = infile + ".anno.avf"

        ag.process_file(infile, outfile, ag.LiftoverClient(genome_version="hg19", target_genome="hg38"), writer=ag.AVFWriter(genome_version="hg19"))
        bframe = ag.read_file(outfile)

        self.assertEqual(bframe.data["chr7:21744592insG"]["variant_data"]["POS_hg19"], 21784210, "")
        self.assertEqual(bframe.data["chr7:21744592insG"]["variant_data"]["POS_hg38"], 21744592, "")

    def test_processor_vcf_writer(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + "/../test_files/somaticMutations.l100.vcf"
        outfile = infile + ".anno.vcf"

        ag.process_file(infile, outfile, ag.LiftoverClient(genome_version="hg19", target_genome="hg38"))
        bframe = ag.read_file(outfile)
        #print(bframe.data)
        print(bframe.data["chr7:21744592insG"])
        print(bframe.data["chr7:21744592insG"].keys())

        self.assertEqual(bframe.data["chr7:21744592insG"]["info_features"]["POS_hg19"], '21784210', "")
        self.assertEqual(bframe.data["chr7:21744592insG"]["info_features"]["POS_hg38"], '21744592', "")

