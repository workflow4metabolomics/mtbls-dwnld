#!/usr/bin/env python3
# vi: fdm=marker

import argparse
import subprocess
import os

# MtblsDwnld {{{1
################################################################

class MtblsDwnld:
    
    quiet = False
    
    # Set quiet {{{2
    ############################################################
    
    def setQuiet(self, quiet):
        self.quiet = quiet

# WgetMtblsDwnld {{{1
################################################################

class WgetMtblsDwnld(MtblsDwnld):
    
    # Download {{{2
    ############################################################
        
    def download(self, study, metadata_only = True, token = None):
        
        # Set output file
        output_file = '.'.join([study, 'zip'])
        
        # Set file to download
        file_to_download = os.path.basename(study)
        if metadata_only:
            file_to_download = 'metadata'
        
        # Set arguments
        args = ['wget', '-O', output_file]
        if self.quiet:
            args.append('-q')
            
        # Set URL
        url = '/'.join(['http://www.ebi.ac.uk/metabolights', os.path.basename(study), 'files', file_to_download])
        if token is not None:
            url = '?'.join(url, '='.join('token', token))
        args.append(url)
            
        # Run download command
        subprocess.run(args)
    
# Read arguments {{{1
################################################################

def read_args():
    
    parser = argparse.ArgumentParser(description='Script for extracting assays from ISATab data and outputing in W4M format.')
    parser.add_argument('study', help = 'The study to retrieve. Use the name for a public study (e.g.: MTBLS30) and the full path for a private sudy (e.g.: /mesa/mystudy-ffffffffffffffffffff-ffff-ffff-ffff-ffffffffffff).')
    parser.add_argument('-M', '--metadata-only', help = 'Download only the metadata (ISA-Tab files i_*, m_*, s_* and a_*) files. This option has no effet if aspera is selected (option -a).', dest = 'metadata_only', action = 'store_true')
    parser.add_argument('-o', '--output', help = 'Set output directory.', dest = "output_dir", default = '.')
    parser.add_argument('-q', '--quiet', help = 'Quiet.', dest = 'quiet', action = 'store_true')
    parser.add_argument('-t', '--token', help = 'Set the token or password to use.', dest = 'token')
    args = parser.parse_args()
 
    return args

# Main {{{1
################################################################

if __name__ == '__main__':
    
    # Parse command line arguments
    args = read_args()
    
    # Create downloader
    downloader = WgetMtblsDwnld()
    downloader.setQuiet(quiet = args.quiet)
    
    # Download
    downloader.download(args.study, metadata_only = args.metadata_only, token = args.token)
