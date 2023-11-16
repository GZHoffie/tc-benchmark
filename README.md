# tc-benchmark
A pipeline for comparing taxonomy classification tools.


## Installation of Tools

In the following, we summarize ways of downloading and using the state-of-the-art taxonomy classification tools, including Kraken 2, CLARK, Centrifuge, Diamond, Ganon and Taxor.

```bash
mkdir tc-tools
cd tc-tools
```

### Kraken 2

Kraken 2 can be downloaded directly via conda or build from source.

```bash
# zlib.h library
sudo apt-get install libz-dev

# install kraken2 under tc-tools/kraken2
git clone https://github.com/DerrickWood/kraken2.git
./install_kraken2.sh ./

# Add the executable to PATH
echo "export PATH=$(pwd):\${PATH}" >> ~/.bashrc
source ~/.bashrc
```
### CLARK

CLARK can be acessed via [this page](http://clark.cs.ucr.edu/).

```bash
wget http://clark.cs.ucr.edu/Download/CLARKV1.2.6.1.tar.gz
tar -xvf CLARKV1.2.6.1.tar.gz
cd CLARKSCV1.2.6.1/
./install.sh
cd exe

# Add the executable to PATH
echo "export PATH=$(pwd):\${PATH}" >> ~/.bashrc
```

### Centrifuge

```bash
# Refer to README on https://github.com/DaehwanKimLab/centrifuge.
git clone https://github.com/DaehwanKimLab/centrifuge
cd centrifuge
make
sudo make install prefix=/usr/local
```

### Diamond

```bash
# Refer to WIKI at https://github.com/bbuchfink/diamond/wiki
wget http://github.com/bbuchfink/diamond/releases/download/v2.1.8/diamond-linux64.tar.gz
tar xzf diamond-linux64.tar.gz

# Add the executable into PATH
mkdir Diamond
mv diamond Diamond/
cd Diamond/
echo "export PATH=$(pwd):\${PATH}" >> ~/.bashrc

```

### Ganon

```bash
# Refer to WIKI at https://pirovc.github.io/ganon
git clone --recurse-submodules https://github.com/pirovc/ganon.git

# Install Python side
cd ganon
python3 setup.py install

# Compile and install C++ side
mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DVERBOSE_CONFIG=ON -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCONDA=OFF -DLONGREADS=OFF ..
make -j 4
sudo make install prefix=/usr/local
```

The above process failed on my computer. We may also install with conda,

```bash
conda install -c bioconda -c conda-forge ganon
```

### Taxor

```bash
mkdir KMCP
cd KMCP
wget https://github.com/shenwei356/kmcp/releases/download/v0.9.4/kmcp_linux_amd64.tar.gz

echo "export PATH=$(pwd):\${PATH}" >> ~/.bashrc
```