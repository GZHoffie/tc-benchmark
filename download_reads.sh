#!/bin/bash

## Download sra toolkit
mkdir -p tools
cd tools
wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.10/sratoolkit.3.0.10-ubuntu64.tar.gz
tar -xvf sratoolkit.3.0.10-ubuntu64.tar.gz
rm *.tar.gz
echo "export PATH=\${PATH}:$(pwd)/sratoolkit.3.0.10-ubuntu64/bin" >> ~/.bashrc
source ~/.bashrc

## Download reads using prefetch
cd /mnt/c/Users/guzh/ # Download outside WSL as the size of files is large

mkdir -p tax_data
cd tax_data

# Download the study that contains pseudomonas isolates
#prefetch -v SRP323385

# Download some isolates ONT reads
wget https://data.gtdb.ecogenomic.org/releases/latest/bac120_metadata.tsv.gz
zcat bac120_metadata.tsv.gz >> bac120_metadata.tsv
rm *.gz


# Convert all .sra files to .fastq files
for file in ./*/*.sra
do
    fasterq-dump ${file}
    rm ${file}
done

## Record ground truth and sample reads from the isolates
NUM_SAMPLES_PER_FILE=1000
mkdir -p sampled_reads

# Use NCBI esearch to get the tax ID of the read files
sudo apt install ncbi-entrez-direct

for file in *.fastq
do
    sra_id="${file%%.*}"
    tax_id=$(esearch -db sra -query $sra_id | efetch -format runinfo | awk -F "," '{print $28}' | sed -n 2p)
    head "./${sra_id}.fastq" -n $(( NUM_SAMPLES_PER_FILE * 4 )) >> "./sampled_reads/${tax_id}.fastq"
    echo "Sampled dataset ${sra_id} with Tax ID ${tax_id}."
done


# merge them all into one single fastq file
for file in ./sampled_reads/*.fastq
do
    cat $file >> sampled_reads.fastq
    base_name=$(basename $file)
    sra_id="${base_name%%.*}"

    line_count=$(wc -l < "$file")
    repetitions=$((line_count / 4))

    for ((i = 0; i < repetitions; i++)); do
        echo "$sra_id" >> sampled_reads.label
    done
done

