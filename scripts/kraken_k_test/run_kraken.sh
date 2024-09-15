benchmark_dir=/mnt/c/Users/zhenh/kraken2_benchmark2

QUERY_FILES=(/mnt/c/Users/zhenh/tax_reads/train_reads.fastq
             /mnt/c/Users/zhenh/tax_reads/ood_species_reads.fastq
             /mnt/c/Users/zhenh/tax_reads/ood_strains_reads.fastq
             /home/zhenhao/htc/data/zymo_test_reads/negative.fastq
             /home/zhenhao/htc/data/human_reads.fastq)
KRAKEN_DB_DIR=/mnt/c/Users/zhenh/tax_db/
KRAKEN_DB_NAMES=(zymo_db_35 zymo_db_31 zymo_db_27 zymo_db_23 zymo_db_19 zymo_db_15)

mkdir -p ${benchmark_dir}
mkdir -p ${benchmark_dir}/log

for i in {0..5}
do
    db_name=${KRAKEN_DB_NAMES[$i]}
    for j in {0..4}
    do
        /usr/bin/time -o ${benchmark_dir}/log/db${i}_query${j}.time -v kraken2 --db ${KRAKEN_DB_DIR}/${db_name} ${QUERY_FILES[$j]} --threads 64 >> ${benchmark_dir}/db${i}_query${j}.output 2> ${benchmark_dir}/log/db${i}_query${j}.time.log
    done
done