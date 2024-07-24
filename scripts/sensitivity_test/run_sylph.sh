#!/bin/bash

test_files_directory=/home/zhenhao/tc-benchmark/data/sensitivity_test
output_file_directory=/home/zhenhao/tc-benchmark/output/sylph_sensitivity_output
SYLPH_DATABASE=/home/zhenhao/tc-benchmark/sylph_gtdb.syldb
SYLPH_EXECUTIVE=/home/zhenhao/tc-benchmark/sylph

mkdir -p $output_file_directory

for coverage in 0.008 0.015 0.101 0.0284 0.0535 0.1902 0.3585 0.6757
do
    # run sylph profile and query
    ${SYLPH_EXECUTIVE} profile $SYLPH_DATABASE ${test_files_directory}/s_aureus_coverage_${coverage}.fastq > ${output_file_directory}/profile_s_aureus_${coverage}.tsv
    #sylph query $SYLPH_DATABASE ${test_files_directory}/s_aureus_coverage_${coverage}.fastq -m 80 -k 21 > ${output_file_directory}/query_s_aureus_${coverage}.tsv

    #sylph query $SYLPH_DATABASE ${test_files_directory}/other_coverage_${coverage}.fastq -m 80 > ${output_file_directory}/query_other_${coverage}.tsv
    ${SYLPH_EXECUTIVE} profile $SYLPH_DATABASE ${test_files_directory}/merged_coverage_${coverage}.fastq > ${output_file_directory}/profile_merged_${coverage}.tsv
done


# Different estimators
for coverage in 0.008 0.015 0.101 0.0284 0.0535 0.1902 0.3585 0.6757
do
    ${SYLPH_EXECUTIVE} profile $SYLPH_DATABASE ${test_files_directory}/s_aureus_coverage_${coverage}.fastq --mme > ${output_file_directory}/profile_s_aureus_mme_${coverage}.tsv
    ${SYLPH_EXECUTIVE} profile $SYLPH_DATABASE ${test_files_directory}/merged_coverage_${coverage}.fastq --mme > ${output_file_directory}/profile_merged_mme_${coverage}.tsv

    ${SYLPH_EXECUTIVE} profile $SYLPH_DATABASE ${test_files_directory}/s_aureus_coverage_${coverage}.fastq --nb > ${output_file_directory}/profile_s_aureus_nb_${coverage}.tsv
    ${SYLPH_EXECUTIVE} profile $SYLPH_DATABASE ${test_files_directory}/merged_coverage_${coverage}.fastq --nb > ${output_file_directory}/profile_merged_nb_${coverage}.tsv

    ${SYLPH_EXECUTIVE} profile $SYLPH_DATABASE ${test_files_directory}/s_aureus_coverage_${coverage}.fastq --mle > ${output_file_directory}/profile_s_aureus_mle_${coverage}.tsv
    ${SYLPH_EXECUTIVE} profile $SYLPH_DATABASE ${test_files_directory}/merged_coverage_${coverage}.fastq --mle > ${output_file_directory}/profile_merged_mle_${coverage}.tsv
done