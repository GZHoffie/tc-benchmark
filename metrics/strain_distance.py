from pymummer import coords_file, alignment, nucmer
import subprocess
import pandas as pd
import re
import numpy as np
from unionfind import unionfind
import random
import glob


def compare_fastANI(reference_file, query_file):
    """
    Use Mummer to find similarity between strains.
    """
    results_file = "temp.txt"

    subprocess.run(["fastANI", "-r", reference_file, "-q", query_file, "-o", results_file], 
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    with open(results_file, "r") as f:
        fastANI_res = f.readline()
        res = float(fastANI_res.split('\t')[2])
    
    subprocess.run(["rm", results_file])
    return res / 100
    
    #alignments = [coord for coord in file_reader if not coord.is_self_hit()] #Remove self hits
    #print(alignments)

def _calculate_pairwise_distance(genome_list):
    """
    Calculate the pairwise distance using Jaccard index, and store it in a 
    distance matrix.
    """
    distance_matrix = np.zeros((len(genome_list), len(genome_list)))
    for i in range(len(genome_list)):
        for j in range(i+1, len(genome_list)):
            distance = min(
                1-compare_fastANI(genome_list[i], genome_list[j]),
                1-compare_fastANI(genome_list[j], genome_list[i])
            )
            print(i, j, distance)
            distance_matrix[i][j] = distance_matrix[j][i] = distance
    
    return distance_matrix
    
def hierarchical_clustering(genome_list, threshold):
    distance_matrix = _calculate_pairwise_distance(genome_list)
    u = unionfind(len(genome_list))
    for i in range(len(genome_list)):
        for j in range(i+1, len(genome_list)):
            if distance_matrix[i][j] <= threshold:
                u.unite(i, j)
    
    return u.groups()

def sample(genome_list, threshold):
    groups = hierarchical_clustering(genome_list, threshold)
    res = []
    for i in groups:
        res.append(genome_list[random.sample(i, 1)[0]])

    return res

if __name__ == "__main__":
    print(sample(glob.glob("data/Staphylococcus_aureus/*.fna"), 0.01))
    #print(compare_fastANI("data/Staphylococcus_aureus/GCA_000360265.1.fna", "data/Staphylococcus_aureus/GCA_000548005.1.fna"))
