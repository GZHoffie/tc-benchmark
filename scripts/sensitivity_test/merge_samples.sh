#!/bin/bash

DATA_DIRECTORY=/home/zhenhao/tc-benchmark/data/sensitivity_test

for coverage in 0.008 0.015 0.101 0.0284 0.0535 0.1902 0.3585 0.6757
do
    # run sylph profile and query
    #sylph profile $SYLPH_DATABASE ${test_files_directory}/s_aureus_coverage_${coverage}.fastq -m 80 -k 21 > ${output_file_directory}/profile_s_aureus_${coverage}.tsv
    #sylph query $SYLPH_DATABASE ${test_files_directory}/s_aureus_coverage_${coverage}.fastq -m 80 -k 21 > ${output_file_directory}/query_s_aureus_${coverage}.tsv

    cat ${DATA_DIRECTORY}/e_coli_coverage_${coverage}.fastq >> ${DATA_DIRECTORY}/merged_coverage_${coverage}.fastq
    cat ${DATA_DIRECTORY}/other_coverage_${coverage}.fastq >> ${DATA_DIRECTORY}/merged_coverage_${coverage}.fastq
done