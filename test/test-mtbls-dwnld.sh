#!/bin/bash
# vi: fdm=marker

# Constants {{{1
################################################################

SCRIPT_PATH=$(dirname $BASH_SOURCE)
MTBLSDWNLD=$SCRIPT_PATH/../mtbls-dwnld
ASPERA_PUBLIC_TOKEN=Xz68YfDe
[[ -z $(which ascp) ]] || ASCP=ascp
WGET=wget

# Test wget whole study {{{1
################################################################

test_wget_whole_study() {

	local study=MTBLS164

	# Remove previously downloaded directory
	rm -rf $study

	# Download
	$MTBLSDWNLD -g $study

	# Test
	expect_folder "$study" || return 1
	expect_file "$study/i_Investigation.txt" || return 1
	expect_files_in_folder "$study" '^._.*\.t.*$' || return 1
	expect_other_files_in_folder "$study" '^._.*\.t.*$' || return 1
}

# Test wget zipped study {{{1
################################################################

test_wget_zipped_study() {

	local study=MTBLS164

	# Remove previously downloaded zip
	rm $study.zip

	# Download
	$MTBLSDWNLD -gMc $study

	# Test
	expect_non_empty_file "$study.zip" || return 1
}

# Test wget metadata only {{{1
################################################################

test_wget_metadata_only() {

	local study=MTBLS164

	# Remove previously downloaded directory
	rm -rf $study

	# Download
	$MTBLSDWNLD -gM $study

	# Test
	expect_folder "$study" || return 1
	expect_file "$study/i_Investigation.txt" || return 1
	expect_no_other_files_in_folder "$study" '^._.*\.t.*$' || return 1
}

# Get private study path {{{1
################################################################

get_private_study_path() {

	local method=$1
	local study=$2

	# Get path
	path=TEST_MTBLS_DWNLD_${method}_${study}_PRIVATE_PATH
	path=$(echo $path | tr '[:lower:]' '[:upper:]')
	expect_str_not_null "${!path}" "No path to test private download of $study with method $method. Please set environment variable $path." >/dev/null

	echo "${!path}"
}

# Get private study token {{{1
################################################################

get_private_study_token() {

	local method=$1
	local study=$2

	# Get token
	token=TEST_MTBLS_DWNLD_${method}_${study}_PRIVATE_TOKEN
	token=$(echo $token | tr '[:lower:]' '[:upper:]')
	expect_str_not_null "${!token}" "No token to test private download of $study with method $method. Please set environment variable $token." >/dev/null

	echo "${!token}"
}

# Test wget private study {{{1
################################################################

test_wget_private_study() {

	local study=MTBLS353

	# Remove previously downloaded directory
	rm -rf $study

	# Download
	$MTBLSDWNLD -gpM -t $(get_private_study_token wget $study) $(get_private_study_path wget $study)

	# Test
	expect_folder "$study" || return 1
	expect_file "$study/i_Investigation.txt" || return 1
}

# Test ascp whole study {{{1
################################################################

test_ascp_whole_study() {

	local study=MTBLS164

	# Remove previously downloaded directory
	rm -rf $study

	# Download
	$MTBLSDWNLD -agq -t "$ASPERA_PUBLIC_TOKEN" $study

	# Test
	expect_folder "$study" || return 1
	expect_file "$study/i_Investigation.txt" || return 1
	expect_files_in_folder "$study" '^._.*\.t.*$' || return 1
	expect_other_files_in_folder "$study" '^._.*\.t.*$' || return 1
}

# Test ascp default key {{{1
################################################################

test_ascp_default_key() {

	local study=MTBLS164

	# Remove previously downloaded directory
	rm -rf $study

	# Download
	$MTBLSDWNLD -agq $study

	# Test
	expect_folder "$study" || return 1
	expect_file "$study/i_Investigation.txt" || return 1
	expect_files_in_folder "$study" '^._.*\.t.*$' || return 1
	expect_other_files_in_folder "$study" '^._.*\.t.*$' || return 1
}

# Test ascp metadata only {{{1
################################################################

test_ascp_metadata_only() {

	local study=MTBLS164

	# Remove previously downloaded directory
	rm -rf $study

	# Download
	$MTBLSDWNLD -agMq $study

	# Test
	expect_folder "$study" || return 1
	expect_file "$study/i_Investigation.txt" || return 1
	expect_no_other_files_in_tree "$study" '^._.*\.t.*$' || return 1
}

# Test ascp private study {{{1
################################################################

test_ascp_private_study() {

	local study=MTBLS1

	# Remove previously downloaded directory
	rm -rf $study

	# Download
	$MTBLSDWNLD -agpMq -t $(get_private_study_token ascp $study) $(get_private_study_path ascp $study)

	# Test
	expect_folder "$study" || return 1
	expect_file "$study/i_Investigation.txt" || return 1
}

# Test wget factor slicing {{{1
################################################################

test_wget_factor_slicing() {

	local study=MTBLS1

	# Remove previously downloaded directory
	rm -rf ${study}

	# Check sliced study
	expect_success $MTBLSDWNLD -g -f Gender=Female $study
	expect_folder "$study" || return 1
	expect_file "$study/i_Investigation.txt" || return 1
	expect_files_in_folder "$study" '^._.*\.t.*$' || return 1
	expect_other_files_in_tree "$study" '^._.*\.t.*$' || return 1
	nb_files=$(find $study -type f | wc -l)
	nb_files_expected=113
	expect_num_eq $nb_files $nb_files_expected "The sliced study should contain $nb_files_expected files. Found $nb_files_sliced_study."
}

# Main {{{1
################################################################

# Small studies to test:        Data files
# MTBLS164    2.30MB            one .xlsx and one .json
# MTBLS174    3.51MB            .zip files and one .json
# MTBLS116    5.72MB            .zip files and one .json
# MTBLS77     6.70MB            .zip files, one .docx and one .xlsx
# MTBLS342    8.09MB            .fid files, one .json
# MTBLS361    23.32MB           .zip files, one .xlsx and one .json
# MTBLS566    34.10MB           2 .mzML files.
# MTBLS1      148.82MB          .zip files and .nmrML files
# MTBLS321    492.24MB          mzXML
# MTBLS213    384.47MB          mzXML
# MTBLS433    204.41MB          mzML
# MTBLS381    776.72MB          mzData
# MTBLS10     180.49MB          CDF

# wget tests
test_context "Testing mtbls-dwnld with wget"
test_that "Download of whole study with wget works correctly." test_wget_whole_study
test_that "Download of study as a zip works correctly." test_wget_zipped_study
test_that "Download of metadata only with wget works correctly." test_wget_metadata_only
test_that "Download of private study with wget works correctly." test_wget_private_study
test_that "Factor slicing works." test_wget_factor_slicing

# aspera test
if [[ -n $ASCP ]] ; then
	test_context "Testing mtbls-dwnld with Aspera ascp"
	test_that "Download of whole study with ascp works correctly." test_ascp_whole_study
	test_that "Download of study using default key with ascp works correctly." test_ascp_default_key
	test_that "Download of metadata only with ascp works correctly." test_ascp_metadata_only

	# XXX ASCP PRIVATE DOWNLOAD FAILING
	#    pierrick@schroeder:mtbls-dwnld$ ascp --policy=fair -T -l 1g mtblight@ah01.ebi.ac.uk:/prod/mtbls1-4ZWHUHHlKR .
	#    ascp: Failed to open TCP connection for SSH, exiting.
	#    Session Stop  (Error: Failed to open TCP connection for SSH)
#	test_that "Download of private study with ascp works correctly." test_ascp_private_study
fi

# Report
test_report
