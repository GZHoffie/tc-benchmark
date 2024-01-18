#!/bin/bash

## Install kraken2
# Store all source files under ./tc-tools
mkdir -p tc-tools
cd tc-tools

## Kraken 2
# zlib.h library
sudo apt-get install libz-dev

# install kraken2 under tc-tools/kraken2
git clone https://github.com/DerrickWood/kraken2.git
cd kraken2
./install_kraken2.sh ./

# Add the executable to PATH
echo "export PATH=\${PATH}:$(pwd)" >> ~/.bashrc
source ~/.bashrc

cd ..

## Download dataset from NCBI
# Download `datasets` API (if haven't already)
mkdir tools
cd tools

wget https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets
chmod +x ./datasets
echo "export PATH=\${PATH}:$(pwd)" >> ~/.bashrc

# Download sratoolkits
wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.10/sratoolkit.3.0.10-ubuntu64.tar.gz
tar -xvf sratoolkit.3.0.10-ubuntu64.tar.gz


# enable search in PATH
cd ..
source ~/.bashrc

# Download sample data from NCBI database
sudo apt-get install -y unzip

mkdir -p tc-data
cd tc-data
datasets download genome taxon 286 --reference --filename pseudomonas_dataset.zip
unzip pseudomonas_dataset.zip
rm README.md pseudomonas_dataset.zip

# Build Kraken2 custom database
kraken2-build --download-taxonomy --db test
for file in ncbi_dataset/data/*/*.fna; do kraken2-build --add-to-library $file --db test; done
kraken2-build --build --db test

# Download some isolates ONT reads
