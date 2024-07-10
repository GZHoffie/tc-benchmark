benchmark_dir=isolates_data


/usr/bin/time -o ${benchmark_dir}/kraken2.time -v kraken2 --db gtdb_kraken2_cpu isolates_data/sampled_reads.fastq --threads 64 >> ${benchmark_dir}/kraken2.output 2> ${benchmark_dir}/kraken2.log