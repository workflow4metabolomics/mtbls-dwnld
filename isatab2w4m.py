#!/usr/bin/env python3
# vi: fdm=marker

import argparse
import sys
import os.path
import re
import glob
import collections
from isatools import isatab as ISATAB

# Check Python version
if sys.hexversion < 0x03040000:
    sys.exit("Python 3.4 or newer is required to run this program.")

# Error message {{{1
################################################################

def error(msg):
    print('ERROR: ' + msg, file = sys.stderr)
    sys.exit(1)
    
# Information message {{{1
################################################################

def info(msg):
    print('INFO: ' + msg)

# Read arguments {{{1
################################################################

def read_args():
    
    s1 = 'You can use it as a template, where %%s will be replaced by the study name and %%a by the assay filename.'
	
    # Default values
    dft_output_dir = '.'
    dft_sample_file = '%s-%a-sample-metadata.tsv'
    dft_variable_file = '%s-%a-variable-metadata.tsv'
    dft_matrix_file = '%s-%a-sample-variable-matrix.tsv'
    
    parser = argparse.ArgumentParser(description='Script for extracting assays from ISATab data and outputing in W4M format.')
    parser.add_argument('-i', help = 'Input directory containing the ISA-Tab files.', dest = 'input_dir', required = True)
    parser.add_argument('-f', help = 'Filename of the assay to extract. If unset, the first assay of the chosen study will be used.',   dest = 'assay_filename', required = False)
    parser.add_argument('-n', help = 'Filename of the study to extract. If unset, the first study found will be used.', dest = 'study_filename', required = False)
    parser.add_argument('-d', help = 'Set output directory. Default is "' + dft_output_dir + '".', dest = "output_dir", required = False, default = dft_output_dir)
    parser.add_argument('-s', help = 'Output file for sample metadata. ' + s1 + ' Default is "' + dft_sample_file.replace('%', '%%') + '".', dest = "sample_output", required = False, default = dft_sample_file)
    parser.add_argument('-v', help = 'Output file for variable metadata. ' + s1 + ' Default is "' + dft_variable_file.replace('%', '%%') + '".', dest = 'variable_output', required = False, default = dft_variable_file)
    parser.add_argument('-m', help = 'Output file for sample x variable matrix. ' + s1 + ' Default is "' + dft_matrix_file.replace('%', '%%') + '".', dest = 'matrix_output', required = False, default = dft_matrix_file)
    parser.add_argument('-S', help = 'Filter out NA values in the specified sample metadata columns. The value is comma separated list of column names.',   dest = 'samp_na_filering', required = False)
    parser.add_argument('-V', help = 'Filter out NA values in the specified variable metadata columns. The value is comma separated list of column names.', dest = 'var_na_filering',  required = False)
    args = parser.parse_args()
    return vars(args)
    
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
        
    return study
    
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

    return assays
    
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
        
    return data_filename
    
# Get assay data frame {{{1
################################################################

def get_assay_df(input_dir, assay):
    return ISATAB.read_tfile(os.path.join(input_dir, assay.filename))
    
# Get measures data frame {{{1
################################################################

def get_measures_df(input_dir, assay):
    data_filename = get_data_file(assay)
    array = ISATAB.read_tfile(os.path.join(input_dir, data_filename))
    return array

# Get study data frame {{{1
################################################################

def get_study_df(input_dir, study):
    return ISATAB.read_tfile(os.path.join(input_dir, study.filename))

# Make names {{{1
################################################################

def make_names(v, uniq = False):
 
    j = 0
    for i in range(len(v)):
        
        # Create missing names
        if v[i] == '':
            v[i] = 'X' + ('' if j == 0 else ('.' + str(j)))
            j += 1
            
        # Remove unvanted characters
        else:
            v[i] = re.sub(r'[^A-Za-z0-9_.]', '.', v[i])
            
    # Make sure all elements are unique  
    if uniq:
        # List all indices of items
        item_indices = collections.defaultdict(list)
        for i, x in enumerate(v):
            item_indices[x].append(i)
            
        # Look for duplicates
        for x in item_indices.keys():
            
            # Is this item duplicated?
            if len(item_indices[x]) > 1:
                
                # Rename all duplicates
                j = 1
                for i in item_indices[x][1:]:
                    while True:
                        new_name = v[i] + "." + str(j)
                        if new_name not in item_indices:
                            break
                        j += 1
                    v[i] = new_name
        
    return v
    
# Make variable names {{{1
################################################################

def make_variable_names(assay_df):

    var_names = None
 
    # Make variable names from data values
    for col in ['mass_to_charge', 'retention_time']:
        try:
            if var_names is None:
                var_names = assay_df[col].values
            else:
                var_names = [ s + ('' if str(t) == '' else ('_' + str(t))) for s, t in zip(var_names, assay_df[col].values)]
        except:
            pass
    
    # Normlize names
    var_names = make_names(var_names)

    return var_names

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
    
    return investigation_file
    
# Load investigation {{{1
################################################################

def load_investigation(input_dir):
    investigation_file = get_investigation_file(input_dir)
    f = open(investigation_file, 'r')
    investigation = ISATAB.load(f)
    return investigation
    
# Get sample names {{{1
################################################################

def get_sample_names(assay):
    return [sample.name for sample in assay.materials['samples']]

# Make sample metadata {{{1
################################################################

def make_sample_metadata(study_df, assay_df, sample_names, normalize = True):
    
    # Normalize column names
    study_df.set_axis(1, make_names(study_df.axes[1].tolist()))
    assay_df.set_axis(1, make_names(assay_df.axes[1].tolist()))
    
    # Merge data frames
    sample_metadata = assay_df.merge(study_df, on = 'Sample.Name', sort = False)

    # Normalize
    if (normalize):
        sample_names = make_names(sample_names, uniq = True)
        sample_metadata.insert(0, 'sample.name', sample_names)
        sample_metadata.set_axis(1, make_names(sample_metadata.axes[1].tolist(), uniq = True))

    return(sample_metadata)

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
        measures_df = get_measures_df(input_dir, assay)
        variable_names = make_variable_names(measures_df)
        sample_names = get_sample_names(assay)
        study_df = get_study_df(input_dir, study)
        assay_df = get_assay_df(input_dir, assay)
        sample_metadata = make_sample_metadata(study_df = study_df, assay_df = assay_df, sample_names = sample_names, normalize = True)
 
# Main {{{1
################################################################

if __name__ == '__main__':
    
    # Parse command line arguments
    args_dict = read_args()
    
    convert2w4m(input_dir = args_dict['input_dir'], study_filename = args_dict['study_filename'], assay_filename = args_dict['assay_filename'])
