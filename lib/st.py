#!/usr/bin/env python
import sys
import pysam
import math
import numpy as np
import os

#pysam implementation for bam file parse 
#jje 03022021

class Bam():
    def __init__(self, bamfile, bedfile=None):
        self.bamfile = bamfile
        self.bedfile = bedfile
        self.bam = pysam.AlignmentFile(bamfile, 'rb')

        self.id = self.get_rg_sample() if self.get_rg_sample() is not None else os.path.basename(self.bamfile)
        
    def get_rg_sample(self):
        #get read group id if exists or use bam filename for output bed name for sample
        if "RG" in self.bam.header.to_dict() and "SM" in self.bam.header.to_dict()["RG"][0]:
            return self.bam.header.to_dict()["RG"][0]["SM"]

        return

    def stat_phred(self, scores):
        #from a list of integer phred scores, transforms and returns 
        #min, median, mean value
        if len(scores) == 0:
            return
        
        vals = np.array(scores)
    
        minval = vals.min()
        medianval = np.median(vals)
        meanval = self.mean_phred(vals)
   
        return minval, medianval, meanval

    def mean_phred(self, scores):
        #from a list of integer phred scores, return mean value
        if len(scores) == 0:
            return
        
        vals = np.array(scores)
    
        return int(-10*math.log10(sum([ math.pow(10, (-1*s)/10) for s in vals])/len(vals)))

    def region_stats(self, bedfile=None):
        #get stats of mapping quality, coverage, flags from a set of bed regions
        
        if bedfile is None:
            if self.bedfile is None:
                message = "ERROR: st.region_stats() requires a bed file of regions provided in method or constructor\n"
                raise Exception(message)
            else:
                bedfile = self.bedfile

        with open(bedfile) as handle:
            bed = handle.readlines()

        outrows = list()
    
        for region in bed:
            col = region.rstrip().split("\t")
            chr = col[0]
            start = int(col[1])
            stop = int(col[2])
    
            #get top strand coords (so stop > start)
            coords = sorted([start,stop])
            sortstart = coords[0]
            sortstop = coords[1]

            pos = dict()
            for pile in self.bam.pileup(chr, sortstart, sortstop, stepper="nofilter"):

                pilepos = pile.reference_pos
        
                if pilepos < start or pilepos >= stop:
                    continue

                numseq = pile.nsegments
                #unused but use later to count/filter overlapping read pairs
                qrynms = pile.get_query_names()

                #get mapping quality and align stats
                mqs = list()
                qlens = list()
                cov = 0

                flagged = {"duplicate": 0, "paired": 0, "proper": 0, "qcfail": 0, "secondary": 0, "mq0": 0, "supplementary": 0, "indel":0 , "deletion": 0, "refskip": 0}
        
                for pileread in pile.pileups:

                    if pileread.indel > 0:
                        flagged["indel"] += 1
                    if pileread.is_del:
                        flagged["deletion"] += 1
                    if pileread.is_refskip:
                        flagged["refskip"] += 1

                    aln = pileread.alignment
            
                    if aln.is_duplicate:
                        flagged["duplicate"] += 1
                    if aln.is_secondary:
                        flagged["secondary"] += 1
                    if aln.is_supplementary:
                        flagged["supplementary"] += 1
                    if aln.is_qcfail:
                        flagged["qcfail"] += 1

                    if aln.is_paired:
                        flagged["paired"] += 1
                    if aln.is_proper_pair:
                        flagged["proper"] += 1
            
                    if aln.mapping_quality == 0:
                        flagged["mq0"] += 1

                    else:#count all flag 3840 with MQ>0
                        if not aln.is_duplicate and not aln.is_secondary and not aln.is_supplementary and not aln.is_qcfail:
                            mqs.append(aln.mapping_quality)
                            qlens.append(aln.infer_query_length())
                            cov += 1

                if len(mqs) == 0:
                    minval = 0
                    medianval = 0
                    meanval = 0
                else:
                    minval, medianval, meanval = self.stat_phred(mqs)

                pos[str(pilepos)] = (cov, minval, medianval, meanval, flagged)

            do_header = True
            colnames = ["chr", "start", "stop", "id", "offset", "coverage", "mq_min", "mq_median", "mq_mean"]

            for loc in sorted(pos.keys()):
                cov, minval, medianval, meanval, flags = pos[loc]
                outrow = [chr, str(start), str(stop), self.id, str(int(loc)-sortstart), str(cov), str(minval), str(medianval), str(meanval)]
    
                for key in sorted(flags):
                    if do_header: 
                        colnames.append(key)

                    outrow.append(str(flags[key]))

                do_header = False
                outrows.append(outrow)

        return colnames, outrows
