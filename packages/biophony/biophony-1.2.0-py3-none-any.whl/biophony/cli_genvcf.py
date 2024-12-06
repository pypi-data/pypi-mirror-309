# pylint: disable=missing-module-docstring
import argparse
import logging

from .cli_script import CliScript
from .mutsim import MutSim

logger = logging.getLogger("biophony")


class VcfGenScript(CliScript):
    """VCF Generator Script class."""

    def __init__(self) -> None:
        super().__init__(desc="Generates VCF files.")

    def declare_args(self, p: argparse.ArgumentParser) -> None:
        """Declares command line arguments."""

        # Input file
        p.add_argument("-f", "--fasta-file", dest="fasta_file", default="-",
                       help=("A FASTA file to use for generating the VCF file."
                             + "Set to \"-\" to use stdin."))

        # Output file
        p.add_argument("-o", "--output-vcf", dest="vcf_file", default="-",
                       help=("Path to the VCF file to generate."
                             + "Set to \"-\" to use stdout."))

        # Generation parameters
        p.add_argument("-m", "--snp-rate", dest="snp_rate", type=float,
                       default=0.0,
                       help="The probability of mutation of one base.")
        p.add_argument("-i", "--ins-rate", dest="ins_rate", type=float,
                       default=0.0,
                       help="The probability of insertion at one base.")
        p.add_argument("-d", "--del-rate", dest="del_rate", type=float,
                       default=0.0,
                       help="The probability of deletion of one base.")

    def do_run(self, args: argparse.Namespace) -> None:
        """Runs VCF Generator code."""

        mutsim = MutSim(fasta_file=args.fasta_file,
                        vcf_file=args.vcf_file,
                        snp_rate=args.snp_rate,
                        del_rate=args.del_rate,
                        ins_rate=args.ins_rate)
        mutsim.run()


def vcfgen_cli() -> None:
    """VCF generation CLI.
    """

    VcfGenScript().run()
