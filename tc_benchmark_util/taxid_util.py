
from collections import Counter
from ete3 import NCBITaxa
from functools import lru_cache


@lru_cache(maxsize=10000)
def get_level(ID, rank='genus'):
    """
    Find the genus of a given species ID, returns None if the taxid is not found,
    or the taxid is at a lower rank than the specified rank.
    :param ID: The species ID.
    :param rank: The rank of the taxonomy to return.
    """

    ncbi = NCBITaxa()

    if ID is None:
        return None
        
    # Get the lineage of the species
    try:
        lineage = ncbi.get_lineage(int(ID))
        ranks = ncbi.get_rank(lineage)
    except:
        return None

    #print(ranks)
    for i in ranks:
        if ranks[i] == rank:
            return i
        
    return None


@lru_cache(maxsize=10000)
def accession_to_taxid(metadata_df, accession):
    """
    Get the taxid of a given accession.
    :param metadata_df: The GTDB metadata dataframe.
    """
    sub_accession = accession[4:]
    try:
        return metadata_df[metadata_df["ncbi_accession"] == sub_accession]["ncbi_taxid"][0]
    except:
        return None
    
def check_equivalence(taxid1, taxid2, rank='species'):
    if get_level(taxid1, rank) is None or get_level(taxid2, rank) is None:
        return False
    return get_level(taxid1, rank) == get_level(taxid2, rank)
