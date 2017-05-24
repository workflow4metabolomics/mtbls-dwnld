#!/usr/bin/env python3
# vi: fdm=marker

import argparse
import sys
import os.path
import re
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

def select_study(investigation, study_filename = None):
    
    study = None
    
    # More than one study and no study specified
    if len(investigation.studies) > 1 and study_filename is None :
        error('The investigation file "' + investigation_file + '" contains more than one study. You need to select one of them.')
 
    # Search for specified study
    if study_filename is not None:
        
        # Loop on all studies
        for s in investigation.studies:
            if s.filename == study_filename:
                study = s
                break

        # Specified study not found
        if study is None :
            error('Study "' + study_filename + '" not found in investigation file "' + investigation_file + '".')
        
    # Take first one
    if study is None and len(investigation.studies) > 0 :
        study = investigation.studies[0]
        
    return(study)
    
# Select assays {{{1
################################################################

def select_assays(study, assay_filename = None):
    
    assays = []
    
    # Search for specified assay
    if assay_filename is not None:
        
        # Loop on all assays
        for a in study.assays:
            if a.filename == assay_filename:
                assays.append(a)
                break
            
        # Specified assay not found
        if len(assays) == 0 :
            error('Assay "' + assay_filename + '" not found.')
    
    # Take all assays
    if len(assays) == 0:
        assays = study.assays

    return(assays)
    
# Get data file {{{1
################################################################

def get_data_file(assay):
    data_filename = None
    for df in assay.data_files:
        m = re.match('^m_.*\.(tsv|txt)$', df.filename)
        if m is not None:
            if data_filename is not None:
                error('Found two data files ("', data_filename, '" and "', df.filename, '") in assay "', assay.filename, '".')
            info('Found data file "' + df.filename + '".')
            data_filename = df.filename
    if data_filename is None:
        error('Found no data file in assay "', assayfilename, '".')
    

# Convert to W4M {{{1
################################################################

def convert2w4m(input_dir, study_filename = None, assay_filename = None):
    investigation_file = os.path.join(input_dir, 'i_Investigation.txt')
    f = open(investigation_file, 'r')
    investigation = ISATAB.load(f)
    
    # Select study
    study = select_study(investigation, study_filename)
    if study is None:
        info('No studies found in investigation file ' + investigation_file)
        return
    info('Processing study "' + study.filename + '" in "' + investigation_file + '".')
    
    # Select assays
    assays = select_assays(study, assay_filename)
    
    # Loop on all assays
    for assay in assays:
        info('Processing assay "' + assay.filename + '".')
        data_filename = get_data_file(assay)
 
# Main {{{1
################################################################

if __name__ == '__main__':
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for extracting assays from ISATab data and outputing in W4M format.')
    parser.add_argument('-i', help = 'Input directory containing the ISA-Tab files.',   dest = 'input_dir',    required = True)
    parser.add_argument('-f', help = 'Filename of the assay to extract. If unset, the first assay of the chosen study will be used.',   dest = 'assay_filename',    required = False)
    parser.add_argument('-n', help = 'Filename of the study to extract. If unset, the first study found will be used.',   dest = 'study_filename',    required = False)
    args = parser.parse_args()
    args_dict = vars(args)
    
    convert2w4m(**args_dict)
