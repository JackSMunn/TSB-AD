# PCA Pipeline Workflow - Visual Guide

## 🎯 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PCA ANOMALY DETECTION PIPELINE               │
│                                                                 │
│  Input: 870 TSB-AD-U Datasets → Process → Analyze → Compare    │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Complete Workflow

```
START
  │
  ├─► STEP 1: Data Processing
  │    ├─ Load 870 CSV files from Datasets/TSB-AD-U/
  │    ├─ Extract features and labels
  │    ├─ Calculate metadata (length, anomaly ratio, etc.)
  │    └─ Compute optimal sliding window per dataset
  │
  ├─► STEP 2: PCA Execution
  │    ├─ For each dataset:
  │    │   ├─ Run PCA (unsupervised)
  │    │   ├─ Generate anomaly scores
  │    │   ├─ Save scores (.npy)
  │    │   └─ Measure runtime
  │    └─ Checkpoint every 10 datasets
  │
  ├─► STEP 3: Evaluation
  │    ├─ For each dataset:
  │    │   ├─ Compute VUS-PR (main metric)
  │    │   ├─ Compute VUS-ROC
  │    │   ├─ Compute Affiliation metrics
  │    │   └─ Save to results CSV
  │    └─ Generate summary statistics
  │
  ├─► STEP 4: Statistical Analysis
  │    ├─ Overall performance stats
  │    ├─ Distribution analysis
  │    ├─ Category breakdown
  │    ├─ Correlation analysis
  │    ├─ Top/bottom performers
  │    └─ Generate 8+ visualizations
  │
  └─► STEP 5: Benchmark Comparison
       ├─ Load TSB-AD benchmark results
       ├─ Rank PCA vs 30+ methods
       ├─ Statistical significance tests
       └─ Generate comparison plots
       
END (All results saved)
```

## 🗂️ Directory Structure After Completion

```
master_pipeline/
│
├─ Run_PCA_Pipeline.py              ← Main execution script
├─ PCA_Statistical_Analysis.ipynb  ← Analysis notebook
├─ Compare_PCA_with_Benchmark.py   ← Comparison tool
├─ PCA_Quick_Start.py               ← One-command launcher
├─ PCA_Pipeline_README.md           ← Detailed documentation
├─ PCA_PIPELINE_SUMMARY.md          ← This summary
│
└─ eval/
   └─ PCA_pipeline/
      │
      ├─ PCA_pipeline.log                  ← Execution log
      │
      ├─ scores/                            ← 870 anomaly score files
      │  ├─ 001_NAB_id_1_*.npy
      │  ├─ 002_NAB_id_2_*.npy
      │  └─ ...
      │
      └─ metrics/
         │
         ├─ PCA_all_results.csv            ← ⭐ Main results file
         ├─ PCA_summary_report.csv         ← Summary statistics
         ├─ PCA_failed_files.csv           ← Error tracking (if any)
         │
         ├─ distribution_analysis.png       ← Distribution plots
         ├─ boxplot_analysis.png           ← Box plots
         ├─ performance_by_category.png    ← Category analysis
         ├─ correlation_matrix.png         ← Correlation heatmap
         ├─ scatter_relationships.png      ← Scatter plots
         ├─ top_bottom_performers.png      ← Best/worst datasets
         ├─ qq_plots.png                   ← Normality tests
         ├─ comprehensive_dashboard.png    ← Full dashboard
         │
         └─ comparisons/                    ← Benchmark comparisons
            ├─ pca_vs_top_methods.png
            ├─ method_ranking.png
            ├─ pca_vs_best.png
            └─ combined_results.csv
```

## 🔄 Execution Flow

### Option 1: Manual (Step by Step)

```bash
# Terminal
cd master_pipeline

# Step 1: Run pipeline
python Run_PCA_Pipeline.py
# ⏱️ ~20-30 minutes
# ✓ Generates scores + metrics

# Step 2: Analyze
jupyter notebook PCA_Statistical_Analysis.ipynb
# ⏱️ ~5 minutes
# ✓ Generates all plots

# Step 3: Compare
python Compare_PCA_with_Benchmark.py
# ⏱️ ~1 minute
# ✓ Generates comparison plots
```

### Option 2: Quick Start (Automated)

```bash
# Terminal
cd master_pipeline
python PCA_Quick_Start.py

# Prompts you through:
# 1. Run pipeline
# 2. Launch analysis notebook
# All automatic!
```

## 📈 Data Flow Diagram

```
┌──────────────┐
│   Dataset    │  001_NAB_id_1_Facility_tr_1007_1st_2014.csv
│   (CSV)      │  [time_series, labels]
└──────┬───────┘
       │
       ├─► Load & Parse
       │   ├─ data: (2014, 1) float array
       │   └─ label: (2014,) int array
       │
       ├─► Metadata Extraction
       │   ├─ data_length: 2014
       │   ├─ num_features: 1
       │   ├─ num_anomalies: 7
       │   ├─ anomaly_ratio: 0.0035
       │   └─ sliding_window: 67 (auto-computed)
       │
       ├─► PCA Execution
       │   ├─ Fit PCA on data
       │   ├─ Transform to components
       │   ├─ Compute reconstruction error
       │   └─ anomaly_scores: (2014,) float array
       │
       ├─► Save Scores
       │   └─ scores/001_NAB_id_1_*.npy
       │
       ├─► Evaluation
       │   ├─ Compute VUS-PR: 0.xxxx
       │   ├─ Compute VUS-ROC: 0.xxxx
       │   └─ Compute other metrics
       │
       └─► Append to Results
           └─ PCA_all_results.csv (new row)

[Repeat for all 870 datasets]
```

## 🎨 Analysis Outputs Visual Map

```
PCA_Statistical_Analysis.ipynb
│
├─ Section 1: Load Results
│  └─ Display: First 5 rows, column info
│
├─ Section 2: Overall Statistics
│  └─ Print: Mean, std, median, min, max for all metrics
│
├─ Section 3: Distribution Analysis
│  └─ Plot: distribution_analysis.png
│     ├─ VUS-PR histogram + KDE
│     ├─ VUS-ROC histogram + KDE
│     ├─ Affiliation Precision histogram + KDE
│     └─ Affiliation Recall histogram + KDE
│
├─ Section 4: Box Plot Analysis
│  └─ Plot: boxplot_analysis.png
│     └─ All metrics in one figure
│
├─ Section 5: Category Performance
│  └─ Plot: performance_by_category.png
│     ├─ Box plot by category
│     └─ Bar chart with error bars
│
├─ Section 6: Correlation Analysis
│  ├─ Plot: correlation_matrix.png (heatmap)
│  └─ Plot: scatter_relationships.png
│     ├─ VUS-PR vs Data Length
│     ├─ VUS-PR vs Anomaly Ratio
│     ├─ Runtime vs Data Length
│     └─ VUS-PR vs VUS-ROC
│
├─ Section 7: Top/Bottom Performers
│  ├─ Print: Top 10 datasets table
│  ├─ Print: Bottom 10 datasets table
│  └─ Plot: top_bottom_performers.png
│
├─ Section 8: Statistical Tests
│  ├─ Print: Shapiro-Wilk results
│  └─ Plot: qq_plots.png (4 subplots)
│
├─ Section 9: Quartile Analysis
│  └─ Print: Performance by quartile
│
├─ Section 10: Summary Report
│  └─ Save: PCA_summary_report.csv
│
├─ Section 11: Comprehensive Dashboard
│  └─ Plot: comprehensive_dashboard.png
│     ├─ VUS-PR distribution
│     ├─ VUS-ROC distribution
│     ├─ Runtime distribution
│     ├─ Category performance (top 15)
│     ├─ VUS-PR vs Anomaly Ratio
│     ├─ VUS-PR vs Data Length
│     └─ VUS-PR vs VUS-ROC
│
└─ Section 12: Conclusions
   └─ Print: Key findings summary
```

## 🔍 Comparison Tool Flow

```
Compare_PCA_with_Benchmark.py
│
├─► Load Data
│   ├─ PCA results (PCA_all_results.csv)
│   └─ Benchmark results (uni_mergedTable_VUS-PR.csv)
│
├─► Align Datasets
│   ├─ Find common datasets
│   └─ Merge on filename
│
├─► Calculate Rankings
│   ├─ Mean VUS-PR for each method
│   └─ Sort descending
│
├─► Statistical Tests
│   ├─ Wilcoxon signed-rank tests
│   ├─ PCA vs top 5 methods
│   └─ Significance levels (*, **, ***)
│
├─► Generate Plots
│   ├─ pca_vs_top_methods.png (box plot)
│   ├─ method_ranking.png (bar chart)
│   └─ pca_vs_best.png (scatter)
│
└─► Save Results
    └─ combined_results.csv
```

## 🎓 Metrics Explained Visually

```
┌─────────────────────────────────────────────┐
│         VUS-PR (Primary Metric)             │
│                                             │
│  Z-axis: Precision                          │
│     ▲                                       │
│   1.0│     ╱╲  ← Surface                   │
│      │   ╱    ╲                             │
│   0.5│ ╱        ╲                           │
│      │╱__________╲___                       │
│   0.0└────────────────→ X-axis: Recall     │
│       0    Window   100                     │
│            Size                             │
│                                             │
│  Volume = ∫∫ Precision × dRecall × dWindow │
│  Range: [0, 1], Higher = Better            │
└─────────────────────────────────────────────┘
```

## 🏆 Success Indicators

```
After running the complete pipeline:

✅ Files Check
   • 870 .npy files in scores/
   • PCA_all_results.csv exists (870 rows)
   • 8+ PNG plots generated
   • Summary report created

✅ Data Sanity
   • Mean VUS-PR: 0.30-0.45
   • No NaN values in results
   • Runtime reasonable (<1s per dataset avg)

✅ Analysis Complete
   • All notebook cells executed
   • No errors in output
   • Plots look reasonable

✅ Comparison Done
   • PCA ranked among methods
   • Comparison plots generated
   • Statistical tests completed
```

## 🚨 Common Issues & Solutions

```
Issue                        Solution
───────────────────────────────────────────────────
"File not found"          → Check DATASET_DIR path
Memory error              → Process in batches
Slow execution            → Normal for 870 datasets
Unicode error             → Check log file encoding
Missing benchmark         → Comparison optional
CUDA warning              → Ignore (PCA doesn't use GPU)
```

## 📊 Example Results Preview

```
Sample from PCA_all_results.csv:

file                               VUS-PR  VUS-ROC  time  category
─────────────────────────────────────────────────────────────────
001_NAB_id_1_Facility_*.csv       0.4521  0.6234  0.23   NAB
002_NAB_id_2_WebService_*.csv     0.3891  0.5876  0.18   NAB
003_NAB_id_3_WebService_*.csv     0.5234  0.7123  0.19   NAB
...

Summary Statistics:
  Total datasets: 870
  Mean VUS-PR: 0.3847 ± 0.1523
  Best: 0.9123 (file: XXX)
  Worst: 0.0234 (file: YYY)
  Total runtime: 18.5 minutes
```

## 🎯 Quick Reference Commands

```bash
# Run everything
python PCA_Quick_Start.py

# Just run PCA
python Run_PCA_Pipeline.py

# Just analyze
jupyter notebook PCA_Statistical_Analysis.ipynb

# Just compare
python Compare_PCA_with_Benchmark.py

# Check progress
tail -f eval/PCA_pipeline/PCA_pipeline.log

# View results
head eval/PCA_pipeline/metrics/PCA_all_results.csv
```

---

**Now you have a complete visual understanding of the pipeline! Ready to run it! 🚀**
