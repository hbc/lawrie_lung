#!/usr/bin/env python
"""Convert phenotype file into PED compatible file for upload to GEMINI.
"""
from __future__ import print_function
import csv
import os
import sys

def main(in_file):
    out_file = "%s.ped" % os.path.splitext(in_file)[0]
    with open(out_file, "w") as out_handle:
        writer = csv.writer(out_handle, dialect="excel-tab")
        with open(in_file) as in_handle:
            reader = csv.reader(in_handle)
            write_ped(reader, writer)

def write_ped(reader, writer):
    base_header = ["#Family_ID", "Individual_ID", "Paternal_ID", "Maternal_ID", "Sex", "Phenotype", "Ethnicity"]
    unset = set(["Paternal_ID", "Maternal_ID", "Phenotype"])
    defaults = {"#Family_ID": "ph_lung"}
    remaps = {"Individual_ID": "Biobank_ID",
              "Sex": "Gender",
              "Ethnicity": "Ethnic_origin"}
    remap_fns = {"Individual_ID": lambda x: x,
                 "Sex": prep_gender,
                 "Ethnicity": lambda x: x}
    final_header = base_header
    header = reader.next()
    final_header = base_header + [h for h in header if h not in remaps.values()]
    writer.writerow(final_header)
    for sample in reader:
        sample_vals = {k: v for k, v in zip(header, sample)}
        out = []
        print("---")
        for h in final_header:
            if h in remaps:
                val = remap_fns[h](sample_vals[remaps[h]])
            elif h in unset:
                val = "-9"
            elif h in defaults:
                val = defaults[h]
            else:
                val = sample_vals[h]
                if h.startswith(("Diag_DanaPoint", "RHC_", "pft_")):
                    print(h, val)
            out.append(val)
        writer.writerow(out)

def prep_gender(x):
    if x.lower() == "male":
        return 1
    elif x.lower() == "female":
        return 2
    else:
        return 0

if __name__ == "__main__":
    main(*sys.argv[1:])
