#!/bin/bash

# This script build the database for each tool
DB_NAME=test
FASTA_FILES=/home/zhenhao/tc-data/ncbi_dataset/data/*/*.fna
LOG_DIRECTORY=/home/zhenhao/tc-benchmark/log
DB_DIRECTORY=/mnt/c/Users/zhenh/db

mkdir -p $LOG_DIRECTORY
mkdir -p $DB_DIRECTORY
cd $DB_DIRECTORY

# Build Kraken2 custom database
kraken2-build --download-taxonomy --db ${DB_NAME}
for file in ${FASTA_FILES}; do kraken2-build --add-to-library $file --db test; done
/usr/bin/time -o "${LOG_DIRECTORY}/kraken2_build.time" -v kraken2-build --build --db test



#for file in gtdb_genomes_reps_r214/database/*/*/*/*/*.fna.gz
#do
#    zcat $file >> temp.fna
#    kraken2-build --add-to-library $file --db gtdb_kraken2
#    rm temp.fna
#done