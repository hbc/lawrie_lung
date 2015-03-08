#!/usr/bin/env python
"""Prepare template CSV file mapping reads to descriptions.
"""
import csv
import os
import sys

def main(ped_file, region_file, *fastq_files):
    ped_file = os.path.abspath(ped_file)
    region_file = os.path.abspath(region_file)
    samples = set([])
    with open(ped_file) as in_handle:
        for line in in_handle:
            if not line.startswith("#"):
                parts = line.split("\t")
                samples.add(parts[1])
    ext = "_R1.fastq.gz"
    sample_files = []
    for fq in fastq_files:
        if fq.endswith(ext):
            fname = os.path.basename(fq).replace(ext, "")
            sample_name = fname.split("-")[-1].split("_")[0]
            if sample_name not in samples:
                print "Missing", sample_name, fname
            else:
                samples.remove(sample_name)
                sample_files.append((sample_name, fname))
    assert len(samples) == 0, samples
    out_file = "%s-metadata.csv" % os.path.splitext(ped_file)[0]
    with open(out_file, "w") as out_handle:
        writer = csv.writer(out_handle)
        writer.writerow(["samplename", "description", "variant_regions", "ped"])
        for sample, fname in sample_files:
            writer.writerow([fname, sample, region_file, ped_file])

if __name__ == "__main__":
    main(*sys.argv[1:])
