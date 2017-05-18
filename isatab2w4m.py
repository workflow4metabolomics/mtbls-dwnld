#!/usr/bin/env python3.4
# vi: fdm=marker

import argparse
from isatools import isatab as ISATAB

# Convert to W4M {{{1
################################################################

def convert2w4m(input_dir):
    f = open(input_dir, 'r')
    investigation = ISATAB.load(f)
    
    if (len(investigation.studies) == 0)
        # No studies
    else
        
 
# Main {{{1
################################################################

if __name__ == '__main__':
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for extracting assays from ISATab data and outputing in W4M format.')
    parser.add_argument('-i', help = 'Input directory containing the ISA-Tab files.',   dest = 'input_dir',    required = True)
    args = parser.parse_args()
    args_dict = vars(args)
    
    print(convert2w4m(**args_dict))
