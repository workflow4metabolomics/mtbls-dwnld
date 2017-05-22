#!/usr/bin/env python3
# vi: fdm=marker

import argparse
import sys
import os.path
from isatools import isatab as ISATAB

# Check Python version
if sys.hexversion < 0x03040000:
    sys.exit("Python 3.4 or newer is required to run this program.")

# Error message
################################################################

def error(msg):
    print('ERROR: ' + msg, file = sys.stderr)
    sys.exit(1)
    
# Information message
################################################################

def info(msg):
    print('INFO: ' + msg)

# Select study {{{1
################################################################

def select_study(investigation, study_name = None):
    
    study = None
    
    # More than one study and no study specified
    if len(investigation.studies) > 1 and study_name is None :
        error('The investigation file "' + investigation_file + '" contains more than one study. You need to select one of them.')
 
    # Search for specified study
    if study_name is not None:
        
        # Loop on all studies
        for s in investigation.studies:
            if s.filename == study_name:
                study = s
                break

        # Specified study not found
        if study is None :
            error('Study "' + study_name + '" not found in investigation file "' + investigation_file + '".')
        
    # Take first one
    if study is None and len(investigation.studies) > 0 :
        study = investigation.studies[0]
        
    return(study)
    
# Convert to W4M {{{1
################################################################

def convert2w4m(input_dir, study_name = None):
    investigation_file = os.path.join(input_dir, 'i_Investigation.txt')
    f = open(investigation_file, 'r')
    investigation = ISATAB.load(f)
    
    # Select study
    study = select_study(investigation, study_name)
    if study is None:
        info('No studies found in investigation file ' + investigation_file)
        return
    info('Processing study "' + study.filename + '" in "' + investigation_file + '".')
 
# Main {{{1
################################################################

if __name__ == '__main__':
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for extracting assays from ISATab data and outputing in W4M format.')
    parser.add_argument('-i', help = 'Input directory containing the ISA-Tab files.',   dest = 'input_dir',    required = True)
    parser.add_argument('-n', help = 'Filename of the study to extract. If unset, the first study found will be used.',   dest = 'study_name',    required = False)
    args = parser.parse_args()
    args_dict = vars(args)
    
    print(convert2w4m(**args_dict))
