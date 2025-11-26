# PCA Pipeline - Complete Package Summary

## 📦 What You've Got

A complete, production-ready pipeline for PCA anomaly detection on TSB-AD-U with comprehensive statistical analysis.

## 📁 Files Created

### 1. Core Pipeline
- **`Run_PCA_Pipeline.py`** - Main execution script
  - Processes all 870 datasets in TSB-AD-U
  - Automatic sliding window calculation
  - Incremental saving (checkpoints)
  - Comprehensive logging
  - ~20-30 min runtime

### 2. Analysis Notebook
- **`PCA_Statistical_Analysis.ipynb`** - Comprehensive analysis
  - 12 analysis sections
  - 10+ visualization types
  - Statistical tests (Shapiro-Wilk, correlations)
  - Category-wise breakdown
  - Top/bottom performers
  - Publication-ready figures

### 3. Comparison Tool
- **`Compare_PCA_with_Benchmark.py`** - Benchmark comparison
  - Compares PCA with 30+ methods
  - Statistical significance tests (Wilcoxon)
  - Ranking and visualization
  - Publication-ready comparison plots

### 4. Quick Start
- **`PCA_Quick_Start.py`** - One-command execution
  - Runs entire pipeline
  - Launches analysis notebook
  - User-friendly prompts

### 5. Documentation
- **`PCA_Pipeline_README.md`** - Complete documentation
  - Usage instructions
  - File descriptions
  - Troubleshooting guide
  - Expected results

## 🚀 Quick Start (3 Steps)

### Step 1: Run the Pipeline
```bash
cd master_pipeline
python Run_PCA_Pipeline.py
```

**What it does:**
- Loads all 870 CSV files from `Datasets/TSB-AD-U/`
- Runs PCA on each dataset
- Computes VUS-PR, VUS-ROC, and other metrics
- Saves anomaly scores and results

**Output:**
```
eval/PCA_pipeline/
├── scores/          # 870 .npy files (anomaly scores)
├── metrics/
│   └── PCA_all_results.csv    # Main results
└── PCA_pipeline.log           # Execution log
```

### Step 2: Analyze Results
```bash
jupyter notebook PCA_Statistical_Analysis.ipynb
```

**What it generates:**
- Distribution analysis plots
- Box plots and Q-Q plots
- Category performance analysis
- Correlation matrices
- Top/bottom performers
- Comprehensive dashboard
- Summary report

### Step 3: Compare with Benchmarks
```bash
python Compare_PCA_with_Benchmark.py
```

**What it does:**
- Loads TSB-AD benchmark results
- Ranks PCA against 30+ methods
- Statistical significance tests
- Generates comparison plots

## 📊 Expected Results

Based on TSB-AD benchmarks:

| Metric | Expected Range |
|--------|----------------|
| Mean VUS-PR | 0.30 - 0.45 |
| Mean VUS-ROC | 0.50 - 0.65 |
| Runtime per dataset | 0.1 - 1.0 seconds |
| Total runtime | 15 - 30 minutes |

## 🎯 What the Pipeline Does

### Data Processing
1. ✅ Loads all TSB-AD-U datasets (870 files)
2. ✅ Handles missing values and data types
3. ✅ Extracts metadata (length, features, anomaly ratio)
4. ✅ Calculates optimal sliding window size per dataset

### PCA Execution
1. ✅ Runs unsupervised PCA (no training data)
2. ✅ Automatic component selection (MLE)
3. ✅ Generates anomaly scores
4. ✅ Saves scores for reproducibility

### Evaluation
1. ✅ Computes VUS-PR (Volume Under Surface - PR)
2. ✅ Computes VUS-ROC
3. ✅ Computes Affiliation metrics
4. ✅ Measures runtime and efficiency

### Analysis
1. ✅ Overall performance statistics
2. ✅ Distribution analysis (histograms, KDE, box plots)
3. ✅ Category breakdown (NAB, WSD, MSL, etc.)
4. ✅ Correlation analysis (anomaly ratio, data length, etc.)
5. ✅ Statistical tests (normality, quartiles)
6. ✅ Top/bottom performer identification

### Comparison
1. ✅ Ranks PCA against benchmark methods
2. ✅ Statistical significance testing
3. ✅ Visual comparisons
4. ✅ Performance analysis

## 📈 Key Visualizations Generated

1. **Distribution Analysis**
   - VUS-PR, VUS-ROC distributions
   - Histograms with KDE overlays
   - Mean/median markers

2. **Box Plot Analysis**
   - All key metrics
   - Outlier detection
   - Quartile visualization

3. **Category Performance**
   - Mean VUS-PR by data source
   - Error bars (standard deviation)
   - Sample size annotations

4. **Correlation Matrix**
   - Heatmap of all correlations
   - Dataset characteristics vs performance
   - Runtime relationships

5. **Scatter Plots**
   - VUS-PR vs data length
   - VUS-PR vs anomaly ratio
   - VUS-PR vs VUS-ROC
   - Runtime vs data length

6. **Top/Bottom Performers**
   - Best 10 datasets (green bars)
   - Worst 10 datasets (red bars)
   - Exact scores displayed

7. **Q-Q Plots**
   - Normality assessment
   - For all key metrics

8. **Comprehensive Dashboard**
   - 7 subplots in one figure
   - All key insights
   - Publication-ready

9. **Comparison Plots** (if benchmarks available)
   - Box plot: PCA vs top methods
   - Ranking bar chart
   - Scatter: PCA vs best method

## 🔬 Statistical Analysis Included

### Descriptive Statistics
- Mean, median, std, min, max
- For all metrics
- Overall and by category

### Distribution Analysis
- Shapiro-Wilk normality tests
- Q-Q plots
- Histogram + KDE

### Correlation Analysis
- Pearson correlations
- Heatmap visualization
- Interpretation guidance

### Comparative Analysis
- Wilcoxon signed-rank tests
- Statistical significance
- Effect sizes

### Quartile Analysis
- Performance quartiles
- Characteristics per quartile
- Trend identification

## 💡 Use Cases

### 1. Benchmark Your Method
Compare your anomaly detection method with PCA baseline.

### 2. Dataset Analysis
Understand which datasets are easy/hard for PCA.

### 3. Publication
Use generated plots and statistics in papers.

### 4. Hyperparameter Tuning
Baseline for tuning other methods.

### 5. Category Insights
Identify which data types PCA works best on.

## 🔧 Customization Options

### Change PCA Parameters
Edit `Run_PCA_Pipeline.py`:
```python
PCA_PARAMS = {
    'n_components': 5,      # Fixed number of components
    'whiten': True          # Enable whitening
}
```

### Filter Datasets
```python
# Process only specific categories
all_files = [f for f in all_files if 'NAB' in f]
```

### Modify Metrics
Add custom metrics in evaluation section:
```python
custom_metric = my_custom_function(output, label)
result_dict['custom_metric'] = custom_metric
```

## 📝 Output Files Reference

### Main Results CSV Columns
- `file` - Dataset filename
- `time` - Runtime (seconds)
- `data_length` - Number of points
- `num_features` - Number of dimensions
- `num_anomalies` - Anomaly count
- `anomaly_ratio` - % anomalies
- `sliding_window` - Window size used
- `VUS-PR` - Main metric ⭐
- `VUS-ROC` - Alternative metric
- `Affiliation_Precision` - Range-based
- `Affiliation_Recall` - Range-based
- Plus 5+ additional metrics

### Generated Plots
All saved to `eval/PCA_pipeline/metrics/`:
- `distribution_analysis.png`
- `boxplot_analysis.png`
- `performance_by_category.png`
- `correlation_matrix.png`
- `scatter_relationships.png`
- `top_bottom_performers.png`
- `qq_plots.png`
- `comprehensive_dashboard.png`

### Comparison Plots
Saved to `eval/PCA_pipeline/metrics/comparisons/`:
- `pca_vs_top_methods.png`
- `method_ranking.png`
- `pca_vs_best.png`
- `combined_results.csv`

## 🎓 Understanding the Results

### VUS-PR (Most Important)
- **What**: Volume under precision-recall surface across window sizes
- **Range**: [0, 1], higher is better
- **Interpretation**:
  - > 0.7: Excellent
  - 0.5-0.7: Good
  - 0.3-0.5: Moderate
  - < 0.3: Needs improvement

### VUS-ROC
- **What**: Volume under ROC surface across window sizes
- **Range**: [0, 1], higher is better
- **Use**: Complement to VUS-PR

### Category Performance
- Shows which data types PCA works well on
- NAB, WSD, MSL, Stock, UCR, etc.
- Helps identify strengths/weaknesses

### Correlations
- Negative with anomaly_ratio: Harder with more anomalies
- Weak with data_length: Size doesn't matter much
- Reveals what factors affect performance

## 🐛 Troubleshooting

### "PCA results not found"
→ Run `python Run_PCA_Pipeline.py` first

### "Benchmark results not found"
→ Normal if you haven't run other methods yet
→ Pipeline still works, just no comparison

### Memory errors
→ Process in batches
→ Close other applications

### CUDA errors
→ PCA doesn't use GPU, ignore these

### Slow execution
→ Normal, 870 datasets take time
→ Check progress in log file

## 🤝 Integration with TSB-AD

This pipeline follows TSB-AD conventions:
- ✅ Uses same evaluation metrics
- ✅ Same dataset format
- ✅ Compatible with existing scripts
- ✅ Results merge with benchmark tables

## 📚 Next Steps

After running the pipeline:

1. **Review Results**
   - Open `PCA_all_results.csv` in Excel/pandas
   - Check log file for any errors

2. **Analyze Performance**
   - Run the Jupyter notebook
   - Review all visualizations
   - Read the summary report

3. **Compare with Benchmarks**
   - Run comparison script
   - Check PCA ranking
   - Identify improvement opportunities

4. **Tune Hyperparameters**
   - Modify PCA parameters
   - Re-run pipeline
   - Compare results

5. **Publish Results**
   - Use generated plots in papers
   - Include summary statistics
   - Reference TSB-AD benchmark

## ✅ Checklist

Before running:
- [ ] Python 3.7+ installed
- [ ] Required packages installed
- [ ] TSB-AD repository cloned
- [ ] Datasets downloaded to `Datasets/TSB-AD-U/`

After running:
- [ ] Check `PCA_all_results.csv` created
- [ ] Verify 870 score files in `scores/`
- [ ] Review log file for errors
- [ ] Run analysis notebook
- [ ] Generate all plots
- [ ] Run comparison (if benchmarks available)

## 🎉 Success Criteria

You'll know it worked when:
1. ✅ 870 .npy files in `scores/` directory
2. ✅ `PCA_all_results.csv` has 870 rows
3. ✅ All plots generated successfully
4. ✅ Summary report shows reasonable statistics
5. ✅ No errors in log file

## 📧 Support

If you encounter issues:
1. Check the log file: `eval/PCA_pipeline/PCA_pipeline.log`
2. Review the README: `PCA_Pipeline_README.md`
3. Check TSB-AD documentation
4. Verify your Python environment

---

**You're all set! Just run `python Run_PCA_Pipeline.py` to get started! 🚀**
