# This script build the database for each tool
DB_NAME=zymo_db
FASTA_FILES=/mnt/c/Users/zhenh/tax_data_split/*/train/*/*.fna
LOG_DIRECTORY=/mnt/c/Users/zhenh/tax_db/log
DB_DIRECTORY=/mnt/c/Users/zhenh/tax_db

# The directory containing the `taxonomy` directory from the NCBI taxonomy database
NCBI_TAXONOMY_DIR=/mnt/c/Users/zhenh/tax_db/


mkdir -p $LOG_DIRECTORY
mkdir -p $DB_DIRECTORY
cd $DB_DIRECTORY

BUILT_LIBRARY=false

# Build Kraken2 custom database
for k in 35 31 27 23 19 15 
do
    mkdir -p ${DB_NAME}_${k}

    # For the first time, insert the files into the library
    if [ "$BUILT_LIBRARY" = false ]; then
        for file in ${FASTA_FILES}
        do 
            echo "Adding file ${file}."
            kraken2-build --add-to-library "$file" --db ${DB_NAME}_${k}
            BUILT_LIBRARY=true
        done
    else
        # mode the library in previous database to the new database
        mv ${DB_NAME}_$((k+4))/library ${DB_NAME}_${k}/library
    fi
    # move the taxonomy file into the database for building
    mv ${NCBI_TAXONOMY_DIR}/taxonomy ${DB_NAME}_${k}/

    # Build the database
    /usr/bin/time -o "${LOG_DIRECTORY}/kraken2_build_${k}.time" -v kraken2-build --kmer-len ${k} --minimizer-len $((k-4)) --minimizer-spaces 0 --threads 20 --build --db ${DB_NAME}_${k}

    # move the taxonomy file back
    mv ${DB_NAME}_${k}/taxonomy ${NCBI_TAXONOMY_DIR}/
done


