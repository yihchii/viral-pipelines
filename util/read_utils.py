#!/usr/bin/env python
"""
Utilities for working with sequence reads, such as format conversions and
fixing mate pairs.
"""

__author__ = "irwin@broadinstitute.org"
__version__ = "PLACEHOLDER"
__date__ = "PLACEHOLDER"
__commands__ = []

import argparse, logging, os
import util.cmd, util.file
from util.file import mkstempfname

log = logging.getLogger(__name__)


# =======================
# ***  purge_unmated  ***
# =======================

def purge_unmated(inFastq1, inFastq2, outFastq1, outFastq2) :
    """Use mergeShuffledFastqSeqs to purge unmated reads, and put corresponding
       reads in the same order."""
    tempOutput = mkstempfname()
    mergeShuffledFastqSeqsPath = os.path.join(util.file.get_scripts_path(),
                                              'mergeShuffledFastqSeqs.pl')
    # The regular expression that follow says that the sequence identifiers
    # of corresponding sequences must be of the form SEQID/1 and SEQID/2
    cmdline = "{mergeShuffledFastqSeqsPath} -t -r '^@(\S+)/[1|2]$' " \
              "-f1 {inFastq1} -f2 {inFastq2} -o {tempOutput}".format(**locals())
    log.debug(cmdline)
    assert not os.system(cmdline)
    os.rename(tempOutput + '.1.fastq', outFastq1)
    os.rename(tempOutput + '.2.fastq', outFastq2)

def parser_purge_unmated() :
    parser = argparse.ArgumentParser(
        description='''Use mergeShuffledFastqSeqs to purge unmated reads, and
                       put corresponding reads in the same order.
                       Corresponding sequences must have sequence identifiers
                       of the form SEQID/1 and SEQID/2.
                    ''')
    parser.add_argument('inFastq1',
        help='Input fastq file; 1st end of paired-end reads.')
    parser.add_argument('inFastq2',
        help='Input fastq file; 2nd end of paired-end reads.')
    parser.add_argument('outFastq1',
        help='Output fastq file; 1st end of paired-end reads.')
    parser.add_argument('outFastq2',
        help='Output fastq file; 2nd end of paired-end reads.')
    return parser

def main_purge_unmated(args) :
    inFastq1 = args.inFastq1
    inFastq2 = args.inFastq2
    outFastq1 = args.outFastq1
    outFastq2 = args.outFastq2
    purge_unmated(inFastq1, inFastq2, outFastq1, outFastq2)
    return 0

__commands__.append(('purge_unmated', main_purge_unmated,
                     parser_purge_unmated))

# =======================
# ***  fastq_to_bam   ***
# =======================
# TBD...

# =======================
# ***  bam_to_fastq   ***
# =======================
# TBD...


# =========================
# ***  fastq_to_fasta   ***
# =========================
# TBD...


# =======================

if __name__ == '__main__':
    util.cmd.main_argparse(__commands__, __doc__)
