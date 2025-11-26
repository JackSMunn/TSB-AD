# PCA Pipeline for TSB-AD-U

A comprehensive pipeline for running PCA anomaly detection on all TSB-AD-U datasets with statistical analysis.

## Overview

This pipeline:
1. Runs PCA on **all 870 datasets** in the TSB-AD-U directory
2. Saves anomaly scores and evaluation metrics
3. Provides comprehensive statistical analysis

## Files

### 1. `Run_PCA_Pipeline.py`
Main execution script that:
- Processes all CSV files in `../Datasets/TSB-AD-U/`
- Runs PCA anomaly detection on each dataset
- Computes VUS-PR, VUS-ROC, and other metrics
- Saves results incrementally (checkpoints every 10 datasets)
- Logs all operations

### 2. `PCA_Statistical_Analysis.ipynb`
Jupyter notebook providing:
- Overall performance statistics
- Distribution analysis
- Box plots and violin plots
- Performance by dataset category
- Correlation analysis
- Top/bottom performers
- Statistical tests (normality, quartiles)
- Comprehensive visualizations

## Usage

### Step 1: Run the Pipeline

```bash
cd master_pipeline
python Run_PCA_Pipeline.py
```

This will:
- Process all 870 datasets in TSB-AD-U
- Save anomaly scores to `eval/PCA_pipeline/scores/`
- Save metrics to `eval/PCA_pipeline/metrics/PCA_all_results.csv`
- Create a log file: `eval/PCA_pipeline/PCA_pipeline.log`

**Expected runtime**: ~15-30 minutes (depends on your hardware)

### Step 2: Analyze Results

Open and run the Jupyter notebook:

```bash
jupyter notebook PCA_Statistical_Analysis.ipynb
```

The notebook will generate:
- Distribution plots
- Box plots
- Category-wise analysis
- Correlation matrices
- Scatter plots
- Q-Q plots
- Comprehensive dashboard
- Summary report

## Output Structure

```
eval/PCA_pipeline/
├── PCA_pipeline.log                    # Execution log
├── scores/                             # Anomaly scores (870 .npy files)
│   ├── 001_NAB_id_1_Facility_*.npy
│   ├── 002_NAB_id_2_WebService_*.npy
│   └── ...
└── metrics/
    ├── PCA_all_results.csv            # Main results file
    ├── PCA_summary_report.csv         # Summary statistics
    ├── distribution_analysis.png       # Distribution plots
    ├── boxplot_analysis.png           # Box plots
    ├── performance_by_category.png     # Category analysis
    ├── correlation_matrix.png          # Correlation heatmap
    ├── scatter_relationships.png       # Scatter plots
    ├── top_bottom_performers.png       # Best/worst datasets
    ├── qq_plots.png                   # Normality Q-Q plots
    └── comprehensive_dashboard.png     # Full dashboard
```

## Results File Format

`PCA_all_results.csv` contains:

| Column | Description |
|--------|-------------|
| `file` | Dataset filename |
| `time` | Runtime (seconds) |
| `data_length` | Number of data points |
| `num_features` | Number of features |
| `num_anomalies` | Number of anomaly points |
| `anomaly_ratio` | Ratio of anomalies |
| `sliding_window` | Window size used for VUS |
| `VUS-PR` | Volume Under Surface - Precision-Recall |
| `VUS-ROC` | Volume Under Surface - ROC |
| `Affiliation_Precision` | Affiliation precision score |
| `Affiliation_Recall` | Affiliation recall score |
| Other metrics... | Additional evaluation metrics |

## Key Metrics Explained

### VUS-PR (Volume Under Surface - Precision-Recall)
- **Most reliable metric** according to TSB-AD paper
- Evaluates performance across multiple sliding window sizes
- Accounts for temporal aspects of anomaly detection
- Range: [0, 1], higher is better
- Focuses on precision-recall trade-off

### VUS-ROC (Volume Under Surface - ROC)
- Similar to VUS-PR but uses ROC curves
- Evaluates true positive rate vs false positive rate
- Range: [0, 1], higher is better

### Affiliation Metrics
- Range-based metrics that consider temporal overlap
- More realistic for time series anomaly detection
- Account for detection delay and partial matches

## Customization

### Modify PCA Parameters

Edit `Run_PCA_Pipeline.py`:

```python
PCA_PARAMS = {
    'n_components': None,  # None = auto, or set integer
    'whiten': False        # Set to True to whiten components
}
```

### Change Dataset Directory

```python
DATASET_DIR = '../Datasets/TSB-AD-U/'  # Modify path here
```

### Adjust Checkpoint Frequency

```python
if len(results_list) % 10 == 0:  # Change 10 to desired frequency
    # Save checkpoint
```

## Statistical Analysis Features

The notebook provides:

1. **Descriptive Statistics**
   - Mean, median, std, min, max for all metrics
   - Performance quartiles

2. **Distribution Analysis**
   - Histograms with KDE overlays
   - Box plots
   - Q-Q plots for normality testing

3. **Category Analysis**
   - Performance breakdown by data source (NAB, WSD, MSL, etc.)
   - Identifies best/worst performing categories

4. **Correlation Analysis**
   - Heatmap of correlations
   - Scatter plots for key relationships
   - Identifies factors affecting performance

5. **Statistical Tests**
   - Shapiro-Wilk normality tests
   - Quartile analysis

6. **Visual Reports**
   - Top 10 and bottom 10 datasets
   - Comprehensive dashboard
   - Publication-ready figures

## Comparison with Other Methods

To compare PCA with other methods (IForest, LOF, KNN, etc.):

1. Run this PCA pipeline
2. Run other methods using `Run_Detector_U.py` from the benchmark_exp directory:
   ```bash
   cd ../benchmark_exp
   python Run_Detector_U.py --AD_Name IForest
   python Run_Detector_U.py --AD_Name LOF
   python Run_Detector_U.py --AD_Name KNN
   ```
3. Merge results and use the Friedman-Nemenyi tests from `analysis.ipynb`

## Troubleshooting

### Memory Issues
If you encounter memory errors with large datasets:
- Process datasets in batches
- Add memory cleanup: `gc.collect()` between datasets

### CUDA Errors
If CUDA is not available but you have a GPU:
- Check PyTorch installation
- Verify CUDA drivers

### Missing Dependencies
Install required packages:
```bash
pip install pandas numpy torch scikit-learn matplotlib seaborn scipy
```

## Citation

If you use this pipeline, please cite the TSB-AD paper:

```bibtex
@article{tsb-ad,
  title={TSB-AD: Time Series Benchmark for Anomaly Detection},
  author={...},
  journal={...},
  year={...}
}
```

## Notes

- PCA is an unsupervised method (no training data needed)
- Default PCA uses automatic component selection (MLE)
- Sliding window size is automatically determined per dataset
- Results are saved incrementally to prevent data loss
- All operations are logged for debugging

## Expected Results

Based on TSB-AD benchmarks, PCA typically achieves:
- Mean VUS-PR: 0.30-0.45 (varies by dataset category)
- Mean VUS-ROC: 0.50-0.65
- Runtime: 0.1-1.0s per dataset (depends on size)

## Next Steps

1. **Run the pipeline**: `python Run_PCA_Pipeline.py`
2. **Analyze results**: Open `PCA_Statistical_Analysis.ipynb`
3. **Compare with baselines**: Check against results in `../benchmark_exp/benchmark_eval_results/`
4. **Tune hyperparameters**: Experiment with different PCA configurations
5. **Publication**: Use generated plots for papers/presentations

---

**Questions?** Check the TSB-AD documentation or open an issue on GitHub.
