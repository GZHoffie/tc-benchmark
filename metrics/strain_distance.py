from pymummer import coords_file, alignment, nucmer

def mummer_strain(reference_file, query_file):
    """
    Use Mummer to find similarity between strains.
    """
    results_file = "./temp_mummer_result.txt"

    runner = nucmer.Runner(reference_file, query_file, results_file) 
    runner.run()
    file_reader = coords_file.reader(results_file)
    alignments = [coord for coord in file_reader if not coord.is_self_hit()] #Remove self hits
    print(alignments)


if __name__ == "__main__":
    mummer_strain("~/tc-benchmark/Escherichia coli/")