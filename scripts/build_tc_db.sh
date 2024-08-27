#!/bin/bash

# This script build the database for each tool
DB_NAME=test_db
FASTA_FILES=/home/zhenhao/htc/data/zymo_data/*/train/*/*.fna
LOG_DIRECTORY=/home/zhenhao/tc-benchmark/log
DB_DIRECTORY=/mnt/c/Users/zhenh/tax_db

mkdir -p $LOG_DIRECTORY
mkdir -p $DB_DIRECTORY
cd $DB_DIRECTORY

# Build Kraken2 custom database
#kraken2-build --download-taxonomy --db ${DB_NAME}
for file in ${FASTA_FILES}
do 
    echo "Adding file ${file}."
    kraken2-build --add-to-library "$file" --db ${DB_NAME}
done
/usr/bin/time -o "${LOG_DIRECTORY}/kraken2_build.time" -v kraken2-build --build --db ${DB_NAME}



#for file in gtdb_genomes_reps_r214/database/*/*/*/*/*.fna.gz
#do
#    zcat $file >> temp.fna
#    kraken2-build --add-to-library $file --db gtdb_kraken2
#    rm temp.fna
#done