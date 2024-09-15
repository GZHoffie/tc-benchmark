#!/bin/bash

REFERENCE_DIRECTORY=/mnt/c/Users/zhenh/tax_data_split/train_all.fna
QUERY_FILES=(/mnt/c/Users/zhenh/tax_reads/train_reads.fastq
             /mnt/c/Users/zhenh/tax_reads/ood_species_reads.fastq
             /mnt/c/Users/zhenh/tax_reads/ood_strains_reads.fastq
             /home/zhenhao/htc/data/zymo_test_reads/negative.fastq
             /home/zhenhao/htc/data/human_reads.fastq)

mkdir -p /mnt/c/Users/zhenh/minimap2_benchmark
mkdir -p /mnt/c/Users/zhenh/minimap2_benchmark/log

cd /mnt/c/Users/zhenh/minimap2_benchmark

for i in {0..4}
do
    /usr/bin/time -o log/query${i}.time -v minimap2 -a ${REFERENCE_DIRECTORY} ${QUERY_FILES[$i]} >> query${i}.output 2> log/query${i}.log
done