from pathlib import Path
import subprocess
import os
import glob
from tqdm import tqdm
import pandas as pd
import pickle
from multiprocessing import Process, Queue, Pool
import random



class ReferenceGenomeDownloader:
    """
    A utility class enabling us to download reference genomes from NCBI RefSeq database.
    """
    def __init__(self) -> None:
        pass
    
    def _download_reference(self, accession, directory):
        """
        Download the reference using the given accession number, and store it in
        ${directory}/${name}.fna. If the file already exists, we append to the file.
        """
        if not os.path.isabs(directory):
            print("[WARNING]\tThe path is not an absolute path.")

        # mkdir if the directory doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)

        # Change to this directory
        os.chdir(directory)

        # Download using NCBI datasets
        subprocess.run(["datasets", "download", "genome", "accession",
                         accession, "--filename", accession + ".zip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(accession + ".zip"):
            subprocess.run(["unzip", accession + ".zip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Store the results in ${directory}/${taxid}.fna
        files_name = glob.glob("ncbi_dataset/data/*/*.fna")
        with open(accession + ".fna", "wb") as f:
            subprocess.run(["cat"] + files_name, stdout=f)
        subprocess.run(["rm", "-r", "ncbi_dataset", accession + ".zip", "README.md"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _remove_directory(self, directory):
        """
        Delete the directory and all the content inside.
        """
        subprocess.run(["rm", "-r", directory], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    def download_reference_from_acession_list(self, accession_list, directory):
        """
        Given a list of accession, Download the corresponding reference under directory.
        """
        for i, accession in tqdm(enumerate(accession_list)):
            self._download_reference(accession, directory)
            
    
    def download_all_references(self, metadata_df, directory, num_samples=None, level="genus"):
        """
        Given a metadata_df with columns "species_taxid", "genus_taxid", "ncbi_genbank_assembly_accession"
        download the references for all species/genera/families.

        For each species/genera/families (specified by `level`), only take `num_samples` references to speed things up.
        """
        if level not in ["species", "genus", "family"]:
            print("[ERROR]\t\tThe level parameter must be one of `species`, `genus` or `family`.")
            return
        
        key = level + "_name"

        # The set of all species/genera/families
        all_set = set(metadata_df.dropna(subset=[key])[key])
        argument_list = []
        for i, item in enumerate(all_set):
            print("Processing item", i+1, "/", len(all_set))

            # get the corresponding part of the metadata
            part_df = metadata_df[metadata_df[key] == item]#.groupby("species_name").sample(1)

            # if there are more than `num_samples` species, sample only `num_samples` of them
            if num_samples is not None and len(part_df) > num_samples:
                part_df = part_df.sample(num_samples)
            
            # Download the references
            argument_list.append((part_df["ncbi_genbank_assembly_accession"], directory + str(item)))


        # Use multiprocessing
        print("Using", os.cpu_count(), "CPUs.")
        pool = Pool(os.cpu_count())
        res = pool.starmap(self.download_reference_from_acession_list, argument_list)
        
        return res


if __name__ == "__main__":
    d = ReferenceGenomeDownloader()
    
    # Read metadata
    metadata_df = pd.read_csv("/home/zhenhao/TDT/gtdb_utils/metadata_with_taxid.csv")

    # Download 10 genomes in the genus escherichia
    #family_samples = set(metadata_df["family_name"].sample(20))
    #metadata_df = metadata_df[metadata_df["family_name"].isin(family_samples)]
    #d.download_all_references(metadata_df, "/home/zhenhao/ETFMH/data_temp/", num_samples=20, level="family")

    #metadata_df = metadata_df[metadata_df["genus_name"] == "Escherichia"]
    #d.download_all_references(metadata_df, "/home/zhenhao/ETFMH/Escherichia_data/", num_samples=10, level="species")

    # Download things not in Escherichia
    #import random
    #metadata_df = metadata_df[metadata_df["genus_name"] != "Escherichia"]
    #genus_samples = random.sample(set(metadata_df["genus_name"]), 10)
    #metadata_df = metadata_df[metadata_df["genus_name"].isin(genus_samples)]
    #d.download_all_references(metadata_df, "/home/zhenhao/ETFMH/Other_data/", num_samples=10, level="genus")

    # Download at most 20 genomes per family
    # For each species, keep at most one genome
    #metadata_df = metadata_df.groupby("species_name").sample(1)
    #d.download_all_references(metadata_df, "/mnt/c/Users/guzh/tax_data/", num_samples=20, level="family")


    #metadata_df = metadata_df[metadata_df["family_name"] == "Staphylococcaceae"]
    #d.download_all_references(metadata_df, "/home/zhenhao/ETFMH/Staphylococcaceae_data/", num_samples=20, level="genus")

    #metadata_df = metadata_df[metadata_df["family_name"] != "Staphylococcaceae"]
    #family_samples = random.sample(list(metadata_df["family_name"]), 20)
    #metadata_df = metadata_df[metadata_df["family_name"].isin(family_samples)]
    #d.download_all_references(metadata_df, "/home/zhenhao/ETFMH/Other_data/", num_samples=10, level="family")

    # Randomly sample 100 species
    metadata_df = metadata_df.dropna()
    species_samples = random.sample(list(metadata_df["species_name"]), 100)
    metadata_df = metadata_df[metadata_df["species_name"].isin(species_samples)]
    d.download_all_references(metadata_df, "/home/zhenhao/tc-benchmark/data/sensitivity_test_genomes/", num_samples=1, level="species")