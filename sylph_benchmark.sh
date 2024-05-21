## Build database for GTDB
# Build genome list
for file in ./gtdb_genomes_reps_r214/database/*/*/*/*/*.fna.gz
do 
    echo ${file} >> genome_list.txt; 
done

# Insert human genome
cp genome_list.txt genome_list_human.txt
echo GCF_000001405.26_GRCh38_genomic.fna >> genome_list_human.txt

## Build sylph DB
/usr/bin/time -o "sylph-build.time" -v ./sylph sketch -l ./genome_list.txt -t 64 -o sylph_gtdb &> "sylph_gtdb_build.log"
/usr/bin/time -o "sylph-build-human.time" -v ./sylph sketch -l ./genome_list_human.txt -t 64 -o sylph_gtdb_human &> "sylph_gtdb_human_build.log"

# Do profiling
sylph sketch /mnt/c/Users/guzh/Downloads/01_Mock_100000-bacteria-l1000-q10.fastq/01_Mock_100000-bacteria-l1000-q10.fastq -d 01
/usr/bin/time -o "sylph-query.time" -v sylph profile sylph_gtdb.syldb 01/*.sylsp > profiling.tsv
/usr/bin/time -o "sylph-query-human.time" -v sylph profile sylph_gtdb_human.syldb 01/*.sylsp > profiling_human.tsv