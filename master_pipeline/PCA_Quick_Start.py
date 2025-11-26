#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick Start Script for PCA Pipeline
Runs the complete PCA analysis workflow with one command
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False, text=True)
        print(f"✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}")
        print(f"Error: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("PCA PIPELINE - QUICK START")
    print("="*80)
    print("\nThis script will:")
    print("  1. Run PCA on all TSB-AD-U datasets")
    print("  2. Generate comprehensive statistical analysis")
    print("  3. Create visualizations and reports")
    print("\n" + "="*80)
    
    response = input("\nDo you want to continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Aborted by user.")
        sys.exit(0)
    
    # Step 1: Run PCA pipeline
    success = run_command(
        "python Run_PCA_Pipeline.py",
        "Step 1/2: Running PCA on all datasets"
    )
    
    if not success:
        print("\n✗ Pipeline failed. Check the logs for details.")
        sys.exit(1)
    
    # Step 2: Open analysis notebook
    print(f"\n{'='*80}")
    print("Step 2/2: Statistical Analysis")
    print(f"{'='*80}")
    print("\nPipeline execution complete!")
    print("\nNext step: Open the analysis notebook")
    print("  Command: jupyter notebook PCA_Statistical_Analysis.ipynb")
    print("\nOr view results directly:")
    print(f"  Results CSV: eval/PCA_pipeline/metrics/PCA_all_results.csv")
    print(f"  Log file: eval/PCA_pipeline/PCA_pipeline.log")
    
    response = input("\nWould you like to open the analysis notebook now? (y/n): ").strip().lower()
    if response == 'y':
        try:
            print("\nLaunching Jupyter notebook...")
            subprocess.run("jupyter notebook PCA_Statistical_Analysis.ipynb", shell=True)
        except Exception as e:
            print(f"Could not launch Jupyter: {e}")
            print("Please run manually: jupyter notebook PCA_Statistical_Analysis.ipynb")
    
    print("\n" + "="*80)
    print("PCA PIPELINE COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  • eval/PCA_pipeline/scores/ - Anomaly scores for all datasets")
    print("  • eval/PCA_pipeline/metrics/PCA_all_results.csv - Full results")
    print("  • eval/PCA_pipeline/metrics/PCA_summary_report.csv - Summary statistics")
    print("\nFor more information, see: PCA_Pipeline_README.md")
    print("="*80 + "\n")

if __name__ == "__main__":
    # Change to benchmark_exp directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
