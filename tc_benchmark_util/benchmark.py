from tc_benchmark_util import taxid_util
import pandas as pd

class read_level_benchmark:
    def __init__(self, metadata_df):
        self.metadata_df = metadata_df
    
    def _benchmark_in_domain(self, ground_truth, predictions, rank='species'):
        """
        Given a list of ground truth and predictions, return a dataframe
        containing the ground truth, predictions, and whether the sensitivity
        and precision of the predictions at the given taxonomy rank.
        """
        assert len(ground_truth) == len(predictions), f"The length of ground truth ({len(ground_truth)}) and predictions ({len(predictions)}) must be the same."
        result_df = pd.DataFrame({'ground_truth': ground_truth, 'predictions': predictions})

        # Convert all taxids to the specified rank
        if rank == 'strain':
            result_df['ground_truth_' + rank] = result_df['ground_truth']
            result_df['predictions_' + rank] = result_df['predictions']
        else:
            result_df['ground_truth_' + rank] = result_df['ground_truth'].apply(lambda x: taxid_util.get_level(x, rank))
            result_df['predictions_' + rank] = result_df['predictions'].apply(lambda x: taxid_util.get_level(x, rank))

        # Remove all rows where ground truth is NaN
        result_df = result_df.dropna(subset=['ground_truth_' + rank])

        # Check if the predictions are correct
        result_df['true_positive'] = result_df.apply(lambda x: taxid_util.check_equivalence(x['ground_truth'], x['predictions'], rank), axis=1)
        if rank == 'strain':
            result_df['mapped'] = result_df['predictions'].apply(lambda x: x != 0)
        else:
            result_df['mapped'] = result_df['predictions'].apply(lambda x: taxid_util.get_level(x, rank) is not None)

        # Group reads of the same ground truth together, and calculate the sensitivity and precision for each group
        # Return a dataframe containing the read count, sensitivity and precision for each group
        grouped = result_df.groupby('ground_truth_' + rank)
        sensitivity = []
        precision = []
        f1 = []
        count = []
        taxid = []
        for name, group in grouped:
            true_positive = group['true_positive'].sum()
            mapped = group['mapped'].sum()
            sensitivity.append(true_positive / len(group))
            precision.append(true_positive / mapped if mapped != 0 else 0)
            f1.append(2 * sensitivity[-1] * precision[-1] / (sensitivity[-1] + precision[-1]) if sensitivity[-1] + precision[-1] != 0 else 0)
            count.append(len(group))
            taxid.append(name)
        
        res = pd.DataFrame({'count': count, 'sensitivity': sensitivity, 'precision': precision, 'f1': f1}, index=taxid) 
        
        return res
    
    def _benchmark_out_of_domain(self, ground_truth, predictions, absent_rank='species', present_rank='genus'):
        """
        Perform benchmarking when the ground truth is out of the domain at rank `rank`.
        We find the specificity at the `absent_rank` level, and the sensitivity and precision at the `present_rank` level.
        """
        assert len(ground_truth) == len(predictions), f"The length of ground truth ({len(ground_truth)}) and predictions ({len(predictions)}) must be the same."
        result_df = pd.DataFrame({'ground_truth': ground_truth, 'predictions': predictions})

        # Convert all taxids to the specified rank
        if present_rank == 'strain':
            result_df['ground_truth_' + present_rank] = result_df['ground_truth']
            result_df['predictions_' + present_rank] = result_df['predictions']
        else:
            result_df['ground_truth_' + present_rank] = result_df['ground_truth'].apply(lambda x: taxid_util.get_level(x, rank))
            result_df['predictions_' + present_rank] = result_df['predictions'].apply(lambda x: taxid_util.get_level(x, rank))

        # Remove all rows where ground truth is NaN
        result_df = result_df.dropna(subset=['ground_truth_' + present_rank])

        # the true negative is the number of reads that are not mapped, or mapped to a higher level
        result_df['true_negative'] = result_df['predictions'].apply(lambda x: taxid_util.get_level(x, absent_rank) is None)

        # the false positives is the number of reads that are mapped to the absent rank
        result_df['false_positive'] = result_df['predictions'].apply(lambda x: taxid_util.get_level(x, absent_rank) is not None)

        # Check TP and FN at the present rank
        result_df['true_positive'] = result_df.apply(lambda x: taxid_util.check_equivalence(x['ground_truth'], x['predictions'], present_rank), axis=1)
        result_df['mapped'] = result_df['predictions'].apply(lambda x: taxid_util.get_level(x, present_rank) is not None)


        # At absent rank, we calculate the specificity
        grouped = result_df.groupby('ground_truth')
        specificity = []
        count = []
        taxid = []
        for name, group in grouped:
            specificity.append(group['true_positive'].sum() / (group['true_positive'].sum() + group['false_positive'].sum()))
            count.append(len(group))
            taxid.append(name)
        res_absent = pd.DataFrame({'count': count, 'specificity': specificity}, index=taxid)
        

        # Group reads of the same ground truth together, and calculate the sensitivity and precision for each group
        # Return a dataframe containing the read count, sensitivity and precision for each group
        grouped = result_df.groupby('ground_truth_' + present_rank)
        sensitivity = []
        precision = []
        count = []
        taxid = []
        for name, group in grouped:
            true_positive = group['true_positive'].sum()
            mapped = group['mapped'].sum()
            sensitivity.append(true_positive / len(group))
            precision.append(true_positive / mapped if mapped != 0 else 0)
            count.append(len(group))
            taxid.append(name)
        
        res_present = pd.DataFrame({'count': count, 'sensitivity': sensitivity, 'precision': precision}, index=taxid) 
        
        return res_absent, res_present

    def parse_ground_truth(self, ground_truth_file):
        """
        Parse the ground truth file and return a dataframe containing the
        ground truth and the taxid of the ground truth.
        """
        with open(ground_truth_file, 'r') as f:
            res = [int(line.strip()) for line in f.readlines()]
        
        return res
    
    def parse_predictions(self, predictions_file):
        """
        Parse the predictions file and return a dataframe containing the
        predictions and the taxid of the predictions.
        """
        pass
    
    
    def parse_in_domain(self, ground_truth_file, predictions_file, ranks=['species']):
        """
        Parse the ground truth and predictions files, and return a dataframe
        containing the ground truth, predictions, and whether the sensitivity
        and precision of the predictions at the given taxonomy rank.
        """
        ground_truth = self.parse_ground_truth(ground_truth_file)
        predictions = self.parse_predictions(predictions_file)
        res = []
        for rank in ranks:
            res.append(self._benchmark_in_domain(ground_truth, predictions, rank=rank))
        return res

    def parse_out_of_domain(self, ground_truth_file, predictions_file, absent_rank='species', present_rank='genus'):
        """
        Parse the ground truth and predictions files, and return a dataframe
        containing the ground truth, predictions, and the specificity at the
        absent rank, and the sensitivity and precision at the present rank.
        """
        ground_truth = self.parse_ground_truth(ground_truth_file)
        predictions = self.parse_predictions(predictions_file)
        return self._benchmark_out_of_domain(ground_truth, predictions, absent_rank=absent_rank, present_rank=present_rank)

class kraken2_read_level_benchmark(read_level_benchmark):
    def __init__(self, metadata_df):
        super().__init__(metadata_df)
    
    def parse_predictions(self, predictions_file):
        """
        Parse the predictions file and return a dataframe containing the
        predictions and the taxid of the predictions.
        """
        with open(predictions_file, 'r') as f:
            res = [int(line.strip().split('\t')[2]) for line in f.readlines()]
        
        return res


class mapper_read_level_benchmark(read_level_benchmark):
    def __init__(self, metadata_df):
        super().__init__(metadata_df)
    
    def parse_predictions(self, predictions_file):
        """
        The predictions_file is a SAM file containing the mapping results.
        """
        classifications = []
        last_read_id = None
        read_map_result = {}
        with open(predictions_file) as f:
            for line in f.readlines():
                if line[0] == "@":
                    continue

                # parse the line
                map_result = line.split("\t")
                read_id = map_result[0]
                if read_id != last_read_id:
                    # record the classification of the last read
                    if last_read_id is not None:
                        if len(read_map_result) == 0:
                            classifications.append(0)
                        else:
                            # find the taxid with the highest map quality
                            best_taxid = max(read_map_result, key=read_map_result.get)
                            classifications.append(int(best_taxid))
                    
                    # reset the read_map_result
                    read_map_result = {}
                
                # update the read_map_result
                read_flag = int(map_result[1])

                #print(read_flag, read_flag & 4 != 0 and read_flag & 256 != 0)
                if read_flag & 4 == 0 and read_flag & 256 == 0:
                    #print(read_flag, taxid)
                    taxid = map_result[2].split("|")[-1]
                    map_quality = int(map_result[4])
                    read_map_result[taxid] = map_quality
                
                # update the last_read_id
                last_read_id = read_id
            
            # record the classification of the last read
            if len(read_map_result) == 0:
                classifications.append(0)
            else:
                # find the taxid with the highest map quality
                best_taxid = max(read_map_result, key=read_map_result.get)
                classifications.append(int(best_taxid))
                
        return classifications
    




if __name__ == "__main__":
    metadata_df = pd.read_csv("/home/zhenhao/metadata_with_taxid.csv", index_col=0)
    benchmark = kraken2_read_level_benchmark(metadata_df)
    rank = 'species'
    res = benchmark.parse_in_domain("/mnt/c/Users/zhenh/tax_reads/train_reads.label", "/mnt/c/Users/zhenh/kraken2_benchmark1/db2_query0.output", ranks=[rank])
    print(res)
    print(res[0]['sensitivity'].median(), res[0]['precision'].median())
    res = benchmark.parse_out_of_domain("/mnt/c/Users/zhenh/tax_reads/ood_strains_reads.label", "/mnt/c/Users/zhenh/kraken2_benchmark1/db2_query2.output", absent_rank='strain', present_rank='species')
    print(res)
    #print(res[0]['sensitivity'].median(), res[0]['precision'].median())



