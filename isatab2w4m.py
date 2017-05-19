#!/usr/bin/env python3.4
# vi: fdm=marker

import argparse
from isatools import isatab as ISATAB

# Information message
################################################################

# Convert to W4M {{{1
################################################################

def convert2w4m(input_dir, study_name = None):
    investigation_file = input_dir + 'i_Investigation.txt'
    f = open(investigation_file, 'r')
    investigation = ISATAB.load(f)
    
    if (len(investigation.studies) == 0)
        # No studies
        print('No studies found in investigation file ' + investigation_file)
        return
    
    elif (len(investigation.studies) > 1)
        # Too much studies
        print('Cannot handle more than one study in investigation file ' + investigation_file)
    else
        study = investigation.studies[0]
        print('Processing study ' + study.name + ' in ' + investigation_file
        
 
# Main {{{1
################################################################

if __name__ == '__main__':
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for extracting assays from ISATab data and outputing in W4M format.')
    parser.add_argument('-i', help = 'Input directory containing the ISA-Tab files.',   dest = 'input_dir',    required = True)
    parser.add_argument('-n', help = 'Name of the study to extract. If unset, the first study found will be used.',   dest = 'study_name',    required = False)
    args = parser.parse_args()
    args_dict = vars(args)
    
    print(convert2w4m(**args_dict))
