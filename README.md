Metabolights Downloader
=======================

[![Build Status](https://travis-ci.org/workflow4metabolomics/mtbls-dwnld.svg?branch=master)](https://travis-ci.org/workflow4metabolomics/mtbls-dwnld)

A [Metabolights](http://www.ebi.ac.uk/metabolights/) study downloader for [Galaxy](https://galaxyproject.org/), part of the [Workflow4Metabolomics](http://workflow4metabolomics.org/) project, and developed during the [PhenoMeNal](http://phenomenal-h2020.eu/home/) project.

For more information, see the galaxy tool page, help section, available inside `mtbls-dwnld_config.xml`.

## Requirements

 * R version 3.2, and the following R packages:
   - CRAN package `R.utils`.
   - CRAN package `getopt`.
   - Bioconductor package `Risa`.
 * `unzip` program.
 * `wget` program.
 * `ascp` (Aspera secure copy) program, which you can download [here](http://downloads.asperasoft.com/en/downloads/50).
 
## Updates

### 2.0.4

 * Test presence of downloader program.
 * Correct running of `wget`.

### 2.0.3

 * Allow to choose the downloading method (`wget` or `aspera`).
 * Ask to specify is the study to download is public or private.
 * Allow to download all assays at once and convert them to W4M format.
 * Allow to download *mzMl* and *mzData* files as collections. 

### 1.3.0

 * Allow to choose the assay to extract and convert to W4M format.
