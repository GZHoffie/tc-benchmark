#!/bin/bash

# Store all source files under ./tc-tools
mkdir tc-tools
cd tc-tools

## Kraken 2
# zlib.h library
sudo apt-get install libz-dev

# install kraken2 under tc-tools/kraken2
git clone https://github.com/DerrickWood/kraken2.git
./install_kraken2.sh ./

# Add the executable to PATH
echo "export PATH=$(pwd):\${PATH}" >> ~/.bashrc

