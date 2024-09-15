#!/bin/bash

# Directory that contains names.dmp and nodes.dmp
KRAKEN2_TAXONOMY_DIR=/mnt/c/Users/zhenh/tax_db/taxonomy

# GTDB taxonomy directory
# Download using `wget https://data.ace.uq.edu.au/public/gtdb/data/releases/latest/bac120_taxonomy.tsv`
GTDB_TAXONOMY_DIR=/home/zhenhao/tc-benchmark/bac120_taxonomy.tsv

# GTDB taxonomy converter
# Download using `git clone https://github.com/rrwick/Metagenomics-Index-Correction.git`
GTDB_CONVERTER_DIR=/home/zhenhao/Metagenomics-Index-Correction

# Run taxonomy conversion
${GTDB_CONVERTER_DIR}/tax_from_gtdb.py --gtdb ${GTDB_TAXONOMY_DIR} --nodes ${KRAKEN2_TAXONOMY_DIR}/nodes.dmp --names ${KRAKEN2_TAXONOMY_DIR}/names.dmp