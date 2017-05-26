#!/usr/bin/env python3
# vi: fdm=marker

import argparse
import sys
import os.path
import re
import glob
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
    
    # Look for data files in assay
    for df in assay.data_files:
        m = re.match('^m_.*\.(tsv|txt)$', df.filename)
        if m is not None:
            if data_filename is not None:
                error('Found two data files ("', data_filename, '" and "', df.filename, '") in assay "', assay.filename, '".')
            info('Found data file "' + df.filename + '".')
            data_filename = df.filename
            
    # No data file
    if data_filename is None:
        error('Found no data file in assay "', assayfilename, '".')
        
    return(data_filename)
    
# Get data array {{{1
################################################################

def get_data_array(input_dir, assay):
    data_filename = get_data_file(assay)
    array = ISATAB.read_tfile(os.path.join(input_dir, data_filename))
    return(array)

# Make variable names {{{1
################################################################

def make_variable_names(data_array):

    var_names = [None] * data_array.axes[0].size
 
    # Make variable names from data values
    for col in ['mass_to_charge', 'retention_time']:
        try:
            c = data_array[col]
            var_names = [ s + t for s, t in zip(var_names, c)]
        except:
            pass

    # Create missing variable names
    
    # Remove unwanted characters
    
    print(var_names)
    return(var_names)

# Get investigation file {{{1
################################################################

def get_investigation_file(input_dir):

    # Search for file
    investigation_files = glob.glob(os.path.join(input_dir, 'i_*.txt'))
    
    # No file
    if len(investigation_files) == 0:
        error('No investigation file found.')
        
    # More than one file
    if len(investigation_files) > 1:
        error('Found more than one investigation file.')
        
    # File found
    investigation_file = investigation_files[0]
    info('Found investigation file "' + investigation_file + '".')
    
    return(investigation_file)
    
# Load investigation {{{1
################################################################

def load_investigation(input_dir):
    investigation_file = get_investigation_file(input_dir)
    f = open(investigation_file, 'r')
    investigation = ISATAB.load(f)
    return(investigaion)
    
# Convert to W4M {{{1
################################################################

def convert2w4m(input_dir, study_filename = None, assay_filename = None):
    investigation = load_investigation(input_dir)

    # Select study
    study = select_study(investigation, study_filename)
    if study is None:
        info('No studies found in investigation file.')
        return
    info('Processing study "' + study.filename + '".')
    
    # Select assays
    assays = select_assays(study, assay_filename)
    
    # Loop on all assays
    for assay in assays:
        info('Processing assay "' + assay.filename + '".')
        data_array = get_data_array(input_dir, assay)
        print(type(data_array))
        print(data_array.axes[1].values)
        var_names = make_variable_names(data_array)
 
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
