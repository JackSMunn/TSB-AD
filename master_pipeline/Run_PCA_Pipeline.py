# -*- coding: utf-8 -*-
# PCA-Only Anomaly Detection Pipeline for TSB-AD-U
# Runs PCA on all datasets in TSB-AD-U directory

import pandas as pd
import numpy as np
import torch
import random
import time
import os
import glob
import logging
from TSB_AD.evaluation.metrics import get_metrics
from TSB_AD.utils.slidingWindows import find_length_rank
from TSB_AD.model_wrapper import run_Unsupervise_AD

# Seeding for reproducibility
seed = 2024
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
np.random.seed(seed)
random.seed(seed)
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

print("="*80)
print("PCA Pipeline for TSB-AD-U Dataset")
print("="*80)
print("CUDA available: ", torch.cuda.is_available())
print("cuDNN version: ", torch.backends.cudnn.version())

# Configuration
DATASET_DIR = '../Datasets/TSB-AD-U/'
SAVE_DIR = './eval/PCA_pipeline/'
SCORE_DIR = os.path.join(SAVE_DIR, 'scores')
METRICS_DIR = os.path.join(SAVE_DIR, 'metrics')

# Create directories
os.makedirs(SCORE_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=f'{SAVE_DIR}/PCA_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# PCA hyperparameters (can be adjusted)
PCA_PARAMS = {
    'n_components': None,  # None uses mle auto-selection
    'whiten': False
}

if __name__ == '__main__':
    
    Start_T = time.time()
    
    # Get all CSV files in the TSB-AD-U directory
    all_files = glob.glob(os.path.join(DATASET_DIR, '*.csv'))
    all_files = sorted(all_files)
    
    print(f"\nFound {len(all_files)} datasets in {DATASET_DIR}")
    print(f"Scores will be saved to: {SCORE_DIR}")
    print(f"Metrics will be saved to: {METRICS_DIR}")
    print("="*80)
    
    # Storage for results
    results_list = []
    failed_files = []
    
    # Process each file
    for idx, file_path in enumerate(all_files, 1):
        filename = os.path.basename(file_path)
        
        # Check if already processed
        score_file = os.path.join(SCORE_DIR, filename.replace('.csv', '.npy'))
        if os.path.exists(score_file):
            print(f"[{idx}/{len(all_files)}] Skipping {filename} (already processed)")
            continue
        
        print(f"\n[{idx}/{len(all_files)}] Processing: {filename}")
        logging.info(f"Processing: {filename}")
        
        try:
            # Load data
            df = pd.read_csv(file_path).dropna()
            data = df.iloc[:, 0:-1].values.astype(float)
            label = df['Label'].astype(int).to_numpy()
            
            print(f"  Data shape: {data.shape}, Labels: {label.sum()} anomalies ({100*label.sum()/len(label):.2f}%)")
            
            # Calculate sliding window for VUS metrics
            slidingWindow = find_length_rank(data[:, 0].reshape(-1, 1), rank=1)
            
            # Run PCA
            start_time = time.time()
            output = run_Unsupervise_AD('PCA', data, **PCA_PARAMS)
            end_time = time.time()
            run_time = end_time - start_time
            
            if not isinstance(output, np.ndarray):
                raise ValueError(f"PCA returned non-array output: {output}")
            
            # Save anomaly scores
            np.save(score_file, output)
            print(f"  ✓ Anomaly scores saved")
            
            # Compute evaluation metrics
            evaluation_result = get_metrics(output, label, slidingWindow=slidingWindow)
            
            # Add metadata
            result_dict = {
                'file': filename,
                'time': run_time,
                'data_length': len(data),
                'num_features': data.shape[1],
                'num_anomalies': int(label.sum()),
                'anomaly_ratio': float(label.sum() / len(label)),
                'sliding_window': slidingWindow
            }
            result_dict.update(evaluation_result)
            results_list.append(result_dict)
            
            # Print key metrics
            print(f"  Runtime: {run_time:.3f}s")
            print(f"  VUS-PR: {evaluation_result['VUS-PR']:.4f}")
            print(f"  VUS-ROC: {evaluation_result['VUS-ROC']:.4f}")
            print(f"  AUC-PR: {evaluation_result['Affiliation_Precision']:.4f}")
            print(f"  AUC-ROC: {evaluation_result['Affiliation_Recall']:.4f}")
            
            logging.info(f"Success: {filename} | Time: {run_time:.3f}s | VUS-PR: {evaluation_result['VUS-PR']:.4f}")
            
            # Save incremental results
            if len(results_list) % 10 == 0:
                temp_df = pd.DataFrame(results_list)
                temp_df.to_csv(f'{METRICS_DIR}/PCA_results_temp.csv', index=False)
                print(f"  → Checkpoint: Saved {len(results_list)} results")
        
        except Exception as e:
            error_msg = f"Failed: {filename} - {str(e)}"
            print(f"  ✗ {error_msg}")
            logging.error(error_msg)
            failed_files.append({'file': filename, 'error': str(e)})
            continue
    
    # Save final results
    print("\n" + "="*80)
    print("Pipeline Complete!")
    print("="*80)
    
    if results_list:
        results_df = pd.DataFrame(results_list)
        results_df.to_csv(f'{METRICS_DIR}/PCA_all_results.csv', index=False)
        print(f"✓ Successfully processed {len(results_list)} datasets")
        print(f"  Results saved to: {METRICS_DIR}/PCA_all_results.csv")
        
        # Print summary statistics
        print("\nSummary Statistics:")
        print(f"  Mean VUS-PR: {results_df['VUS-PR'].mean():.4f} ± {results_df['VUS-PR'].std():.4f}")
        print(f"  Mean VUS-ROC: {results_df['VUS-ROC'].mean():.4f} ± {results_df['VUS-ROC'].std():.4f}")
        print(f"  Mean Runtime: {results_df['time'].mean():.3f}s ± {results_df['time'].std():.3f}s")
        print(f"  Total Runtime: {time.time() - Start_T:.2f}s ({(time.time() - Start_T)/60:.2f} minutes)")
    
    if failed_files:
        failed_df = pd.DataFrame(failed_files)
        failed_df.to_csv(f'{METRICS_DIR}/PCA_failed_files.csv', index=False)
        print(f"\n✗ Failed to process {len(failed_files)} datasets")
        print(f"  Error log saved to: {METRICS_DIR}/PCA_failed_files.csv")
    
    print("\n" + "="*80)
    print("Next steps:")
    print("  1. Review results in:", METRICS_DIR)
    print("  2. Run statistical analysis: jupyter notebook PCA_Statistical_Analysis.ipynb")
    print("="*80)
