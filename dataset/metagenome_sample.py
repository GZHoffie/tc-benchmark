import pandas as pd
import numpy as np
import subprocess
import os
import random
import glob
from pathlib import Path

class MetagenomicSampleGenerator:
    def __init__(self) -> None:
        pass

    def generate_sample(self, references, output_directory, output_file_name, total_read_num=None, average_coverage=None, distribution="log_normal"):
        """
        Generate a metagenomic sample.

        Install badread with
        ```bash
        pip3 install git+https://github.com/rrwick/Badread.git
        ```
        before running this function.

        Args:
            - read_num (int): number of reads in the generated sample.
            - references (List[str]): list of file names containing the references in the metagenomic sample.
            - output_directory (str): path to store the output file.
            - output_file_name (str): name of the output files.
            - distribution (either "uniform" or "log_normal"): the distribution of abundance.
        """
        # mkdir if the directory doesn't exist
        Path(output_directory).mkdir(parents=True, exist_ok=True)

        # decide abundance of the sample
        total_species_num = len(references)
        if distribution == "log_normal":
            species_abundance = np.random.lognormal(0, 1, total_species_num)
            species_abundance = species_abundance / np.sum(species_abundance)
            species_abundance = np.sort(species_abundance)
        else:
            species_abundance = np.ones(total_species_num) / len(total_species_num)


        # Assign pathogens the lowest abundance
        species_index = 0
        reads = ""
        all_species = []
        abundance_ground_truth = {}

        # Open file for writing
        f = open(os.path.join(output_directory, output_file_name + ".fastq"), 'w')
        f.close()

        # Simulate reads from pathogen genome
        #print(references)
        for file in references:
            print("Simulating reads from file", file)
            # determine number of reads of this species
            if total_read_num is not None:
                num_reads = str(int(species_abundance[species_index] * total_read_num * 4000))
            elif average_coverage is not None:
                num_reads = str(average_coverage) + "x"


            # Simulate reads
            simulated_read = subprocess.run(["badread", "simulate", "--reference", file, "--quantity", num_reads, "--length", "4000,2000", "--identity", "100,100,0",
                                             "--glitches", "0,0,0", "--junk_reads", "0", "--random_reads", "0", "--chimeras", "0"], capture_output=True)
            
            # Store the reads in `reads` list
            #read_list = simulated_read.stdout.decode("utf-8").split('\n')
            #read_list = [r for i, r in enumerate(read_list) if i % 4 == 1]
            with open(os.path.join(output_directory, output_file_name + ".fastq"), 'ab') as f:
                f.write(simulated_read.stdout)
            #reads += simulated_read.stdout.decode("utf-8")

            # Accession = file.stem()
            accession = Path(file).stem

            # store ground truth
            abundance_ground_truth[accession] = species_abundance[species_index]

            # move on to next species
            species_index += 1

        # Output raw reads
        #read_index = np.arange(len(reads))
        #random.shuffle(read_index)


        # Output ground truth abundance
        with open(os.path.join(output_directory, output_file_name + "_abundance.csv"), 'w') as f:
            f.write("accession,abundance\n")
            for file in abundance_ground_truth:
                f.write(file + "," + str(abundance_ground_truth[file]) + "\n")


if __name__ == "__main__":
    import glob

    g = MetagenomicSampleGenerator()
    #print(glob.glob("./data_temp/*/*.fna"))
    #g.generate_sample(glob.glob("./single_species/*/*.fna"), 100000, "./", "EColi")
    
    coverages = [0.008, 0.015, 0.0284, 0.0535, 0.101, 0.1902, 0.3585, 0.6757]
    for coverage in coverages:
        g.generate_sample(glob.glob("./data/sensitivity_test_genomes/Staphylococcus aureus/*.fna"), "./data/sensitivity_test", "s_aureus_coverage_" + str(coverage), average_coverage=coverage)