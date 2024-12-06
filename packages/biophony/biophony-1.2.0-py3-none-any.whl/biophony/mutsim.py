"""Uses Mutation Simulator package to generate VCF."""

import os
import shutil
import subprocess
import sys
import tempfile


# pylint: disable=too-few-public-methods
class MutSim:
    """Class for calling Mutation Simulator.

    :param fasta_file: Input FASTA file to use. Set to "-" to use stdin.
    :param vcf_file: Path to VCF file to generate. Set to "-" to use stdout.
    :param snp_rate: The probability of mutation of one base.
    :param del_rate: The probability of deletion of one base.
    :param ins_rate: The probability of insertion at one base.
    """
    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self, fasta_file: str, vcf_file: str,
                 snp_rate: float, del_rate: float, ins_rate: float) -> None:

        self._vcf_file = vcf_file
        self._snp_rate = snp_rate
        self._del_rate = del_rate
        self._ins_rate = ins_rate

        # Create temporary working directory
        self._tmp_dir = tempfile.mkdtemp()

        # Write FASTA data if received from stdin
        if fasta_file == '-':
            fasta_file = os.path.join(self._tmp_dir, 'seq.fasta')
            with open(fasta_file, 'w', encoding="utf-8") as f:
                for line in sys.stdin:
                    f.write(line)

        # Get absolute path
        self._fasta_file = os.path.abspath(fasta_file)

    def run(self) -> None:
        """Generate VCF file."""

        # Store current working directory
        old_dir = os.getcwd()

        try:

            # Enter temp folder
            os.chdir(self._tmp_dir)

            # Call mutation-simulator script
            cmd = ["mutation-simulator", "-q", "-o", "variant", self._fasta_file,
                   "args", "-sn", str(self._snp_rate), "-de",
                   str(self._del_rate), "-in", str(self._ins_rate)]
            with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
                exit_code = proc.wait()
                assert exit_code == 0

            # Get generated VCF file
            generated_vcf = os.path.join(self._tmp_dir, "variant_ms.vcf")
            if self._vcf_file == "-":
                with open(generated_vcf, "r", encoding="utf-8") as f:
                    for line in f:
                        sys.stdout.write(line)
            else:
                os.rename(generated_vcf, self._vcf_file)

        finally:

            # Go back to former folder
            os.chdir(old_dir)

            # Delete temp folder
            shutil.rmtree(self._tmp_dir)
