# -*- coding: utf-8 -*-
"""
Compare PCA with TSB-AD Benchmark Results
Loads existing benchmark results and compares with PCA performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Configuration
PCA_RESULTS_PATH = './eval/PCA_pipeline/metrics/PCA_all_results.csv'
BENCHMARK_PATH = '../benchmark_exp/benchmark_eval_results/uni_mergedTable_VUS-PR.csv'
OUTPUT_DIR = './eval/PCA_pipeline/metrics/comparisons/'

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    """Load PCA and benchmark results"""
    print("Loading data...")
    
    # Load PCA results
    if not os.path.exists(PCA_RESULTS_PATH):
        print(f"Error: PCA results not found at {PCA_RESULTS_PATH}")
        print("Please run Run_PCA_Pipeline.py first!")
        return None, None
    
    pca_df = pd.read_csv(PCA_RESULTS_PATH)
    print(f"✓ Loaded PCA results: {len(pca_df)} datasets")
    
    # Load benchmark results
    if not os.path.exists(BENCHMARK_PATH):
        print(f"Warning: Benchmark results not found at {BENCHMARK_PATH}")
        print("Comparison with other methods will be limited.")
        benchmark_df = None
    else:
        benchmark_df = pd.read_csv(BENCHMARK_PATH)
        print(f"✓ Loaded benchmark results: {len(benchmark_df)} datasets, {len(benchmark_df.columns)-1} methods")
    
    return pca_df, benchmark_df

def compare_with_benchmark(pca_df, benchmark_df):
    """Compare PCA with benchmark methods"""
    
    if benchmark_df is None:
        print("Skipping benchmark comparison (no data)")
        return
    
    print("\n" + "="*80)
    print("COMPARISON WITH TSB-AD BENCHMARK METHODS")
    print("="*80)
    
    # Create a mapping from PCA filenames to benchmark filenames
    pca_df['file_base'] = pca_df['file'].str.replace('.csv', '')
    
    # Common datasets
    common_files = set(pca_df['file'].unique()) & set(benchmark_df['file'].unique())
    print(f"\nCommon datasets: {len(common_files)}")
    
    if len(common_files) == 0:
        print("Warning: No common datasets found. Check filename formats.")
        return
    
    # Filter to common datasets
    pca_common = pca_df[pca_df['file'].isin(common_files)].copy()
    benchmark_common = benchmark_df[benchmark_df['file'].isin(common_files)].copy()
    
    # Get list of methods from benchmark
    methods = [col for col in benchmark_common.columns if col not in ['file', 'category', 'point_anomaly', 'seq_anomaly', 'num_anomaly']]
    
    # Add PCA to benchmark dataframe
    pca_scores = pca_common.set_index('file')['VUS-PR'].to_dict()
    benchmark_common['PCA'] = benchmark_common['file'].map(pca_scores)
    methods.append('PCA')
    
    # Calculate mean scores
    mean_scores = {}
    for method in methods:
        if method in benchmark_common.columns:
            mean_scores[method] = benchmark_common[method].mean()
    
    # Sort by mean score
    sorted_methods = sorted(mean_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Print ranking
    print("\n" + "="*60)
    print("RANKING BY MEAN VUS-PR (higher is better)")
    print("="*60)
    print(f"{'Rank':<6} {'Method':<30} {'Mean VUS-PR':<15} {'Std'}")
    print("-"*60)
    
    pca_rank = None
    for rank, (method, score) in enumerate(sorted_methods, 1):
        std = benchmark_common[method].std()
        marker = " ← PCA" if method == 'PCA' else ""
        print(f"{rank:<6} {method:<30} {score:.4f}          {std:.4f}{marker}")
        if method == 'PCA':
            pca_rank = rank
    
    print("="*60)
    print(f"\nPCA ranks #{pca_rank} out of {len(sorted_methods)} methods")
    print(f"PCA outperforms {len(sorted_methods) - pca_rank} methods")
    
    # Statistical comparison with top methods
    print("\n" + "="*80)
    print("STATISTICAL COMPARISON (Wilcoxon signed-rank test)")
    print("="*80)
    
    top_methods = [m for m, _ in sorted_methods[:10] if m != 'PCA'][:5]
    
    for method in top_methods:
        if method in benchmark_common.columns:
            pca_scores_arr = benchmark_common['PCA'].dropna().values
            method_scores_arr = benchmark_common[method].dropna().values
            
            # Align the arrays
            min_len = min(len(pca_scores_arr), len(method_scores_arr))
            pca_scores_arr = pca_scores_arr[:min_len]
            method_scores_arr = method_scores_arr[:min_len]
            
            stat, p_value = stats.wilcoxon(pca_scores_arr, method_scores_arr, alternative='two-sided')
            
            pca_mean = pca_scores_arr.mean()
            method_mean = method_scores_arr.mean()
            diff = pca_mean - method_mean
            
            significance = ""
            if p_value < 0.001:
                significance = "***"
            elif p_value < 0.01:
                significance = "**"
            elif p_value < 0.05:
                significance = "*"
            else:
                significance = "ns"
            
            print(f"\nPCA vs {method}:")
            print(f"  Mean difference: {diff:+.4f}")
            print(f"  p-value: {p_value:.4f} {significance}")
            print(f"  Interpretation: ", end="")
            if p_value < 0.05:
                if diff > 0:
                    print("PCA is significantly better")
                else:
                    print(f"{method} is significantly better")
            else:
                print("No significant difference")
    
    print("\n* p<0.05, ** p<0.01, *** p<0.001, ns=not significant")
    
    # Visualization
    create_comparison_plots(benchmark_common, methods, top_methods)
    
    return benchmark_common, pca_rank, len(sorted_methods)

def create_comparison_plots(benchmark_common, all_methods, top_methods):
    """Create comparison visualizations"""
    
    print("\nGenerating comparison plots...")
    
    # 1. Box plot comparison with top methods
    fig, ax = plt.subplots(figsize=(14, 6))
    
    methods_to_plot = top_methods + ['PCA']
    data_to_plot = [benchmark_common[m].dropna() for m in methods_to_plot]
    
    bp = ax.boxplot(data_to_plot, labels=methods_to_plot, patch_artist=True,
                    showmeans=True, meanline=True,
                    meanprops=dict(color='red', linestyle='--', linewidth=2))
    
    # Highlight PCA box
    for i, (box, method) in enumerate(zip(bp['boxes'], methods_to_plot)):
        if method == 'PCA':
            box.set_facecolor('lightcoral')
            box.set_alpha(0.8)
            box.set_edgecolor('red')
            box.set_linewidth(2)
        else:
            box.set_facecolor('lightblue')
            box.set_alpha(0.6)
    
    ax.set_ylabel('VUS-PR', fontweight='bold', fontsize=12)
    ax.set_title('PCA vs Top Benchmark Methods', fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=15, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/pca_vs_top_methods.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {OUTPUT_DIR}/pca_vs_top_methods.png")
    
    # 2. Ranking bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    
    methods_subset = top_methods[:15] + ['PCA']
    means = [benchmark_common[m].mean() for m in methods_subset]
    
    colors = ['red' if m == 'PCA' else 'steelblue' for m in methods_subset]
    
    y_pos = np.arange(len(methods_subset))
    ax.barh(y_pos, means, color=colors, alpha=0.7, edgecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods_subset)
    ax.set_xlabel('Mean VUS-PR', fontweight='bold', fontsize=12)
    ax.set_title('Method Ranking by Mean VUS-PR', fontweight='bold', fontsize=14)
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(means):
        ax.text(v + 0.01, i, f'{v:.4f}', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/method_ranking.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {OUTPUT_DIR}/method_ranking.png")
    
    # 3. Scatter plot: PCA vs best method
    if len(top_methods) > 0:
        best_method = top_methods[0]
        fig, ax = plt.subplots(figsize=(8, 8))
        
        ax.scatter(benchmark_common[best_method], benchmark_common['PCA'], 
                  alpha=0.5, s=50, c='purple', edgecolor='black')
        
        # Add diagonal line
        lims = [0, 1]
        ax.plot(lims, lims, 'k--', alpha=0.5, linewidth=2)
        
        ax.set_xlabel(f'{best_method} VUS-PR', fontweight='bold', fontsize=12)
        ax.set_ylabel('PCA VUS-PR', fontweight='bold', fontsize=12)
        ax.set_title(f'PCA vs {best_method} (Best Method)', fontweight='bold', fontsize=14)
        ax.grid(alpha=0.3)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        
        # Add correlation
        corr = benchmark_common[[best_method, 'PCA']].corr().iloc[0, 1]
        ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', 
               transform=ax.transAxes, fontsize=12, 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/pca_vs_best.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {OUTPUT_DIR}/pca_vs_best.png")

def main():
    print("="*80)
    print("PCA BENCHMARK COMPARISON TOOL")
    print("="*80)
    
    # Load data
    pca_df, benchmark_df = load_data()
    
    if pca_df is None:
        return
    
    # Compare with benchmark
    if benchmark_df is not None:
        benchmark_common, pca_rank, total_methods = compare_with_benchmark(pca_df, benchmark_df)
        
        # Save combined results
        if benchmark_common is not None:
            benchmark_common.to_csv(f'{OUTPUT_DIR}/combined_results.csv', index=False)
            print(f"\n✓ Saved combined results: {OUTPUT_DIR}/combined_results.csv")
    
    # Print PCA-only statistics
    print("\n" + "="*80)
    print("PCA STANDALONE STATISTICS")
    print("="*80)
    print(f"Total datasets processed: {len(pca_df)}")
    print(f"Mean VUS-PR: {pca_df['VUS-PR'].mean():.4f} ± {pca_df['VUS-PR'].std():.4f}")
    print(f"Median VUS-PR: {pca_df['VUS-PR'].median():.4f}")
    print(f"Best VUS-PR: {pca_df['VUS-PR'].max():.4f}")
    print(f"Worst VUS-PR: {pca_df['VUS-PR'].min():.4f}")
    
    print("\n" + "="*80)
    print("COMPARISON COMPLETE!")
    print("="*80)
    print(f"\nResults saved to: {OUTPUT_DIR}")
    print("\nGenerated files:")
    print("  • pca_vs_top_methods.png - Box plot comparison")
    print("  • method_ranking.png - Ranking bar chart")
    print("  • pca_vs_best.png - Scatter plot vs best method")
    print("  • combined_results.csv - Combined results table")
    print("="*80)

if __name__ == '__main__':
    main()
