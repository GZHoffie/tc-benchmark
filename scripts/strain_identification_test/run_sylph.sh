#!/bin/bash

test_files_directory=/home/zhenhao/tc-benchmark/strain_identification_test
output_file_directory=/home/zhenhao/tc-benchmark/output/sylph_strain_id_output
SYLPH_DATABASE=/home/zhenhao/tc-benchmark/database.syldb

mkdir -p $output_file_directory

ls ${test_files_directory}/*.fastq

for file in ${test_files_directory}/*.fastq
do
    # run sylph profile and query
    filename=$(basename "$file")
    stem="${filename%.*}"

    sylph query $SYLPH_DATABASE ${file} > ${output_file_directory}/query_${stem}.tsv
    sylph profile $SYLPH_DATABASE ${file} > ${output_file_directory}/profile_${stem}.tsv
    #sylph profile $SYLPH_DATABASE ${test_files_directory}/merged_coverage_${coverage}.fastq > ${output_file_directory}/profile_merged_${coverage}.tsv
done