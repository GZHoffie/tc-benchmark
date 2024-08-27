benchmark_dir=/mnt/c/Users/zhenh/kraken2_benchmark

QUERY_FILES=(/home/zhenhao/htc/data/zymo_test_reads/train_reads.fastq
             /home/zhenhao/htc/data/zymo_test_reads/ood_species_reads.fastq
             /home/zhenhao/htc/data/zymo_test_reads/negative.fastq
             /home/zhenhao/htc/data/human_reads.fastq)
KRAKEN_DB_DIR=/mnt/c/Users/zhenh/tax_db/
KRAKEN_DB_NAMES=(test_35_db test_31_db test_27_db test_23_db test_19_db test_15_db)

mkdir -p ${benchmark_dir}
mkdir -p ${benchmark_dir}/log

for i in {0..5}
do
    db_name=${KRAKEN_DB_NAMES[$i]}
    for j in {0..3}
    do
        /usr/bin/time -o ${benchmark_dir}/log/db${i}_query${j}.time -v kraken2 --db ${KRAKEN_DB_DIR}/${db_name} ${QUERY_FILES[$j]} --threads 64 >> ${benchmark_dir}/db${i}_query${j}.output 2> ${benchmark_dir}/log/db${i}_query${j}.time.log
    done
done