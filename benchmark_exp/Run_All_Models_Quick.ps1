# Run All Models on Small Subset (10 datasets only)
# This script runs all 37 models on just 10 datasets for quick testing

# Activate virtual environment
cd "C:\Users\Anne Louise\Documents\GitHub\TSB-AD"
.\venv\Scripts\Activate.ps1
cd benchmark_exp

# Create a temporary file list with only 10 datasets
$fileListPath = "../Datasets/File_List/TSB-AD-U-Eva.csv"
$tempFileListPath = "../Datasets/File_List/TSB-AD-U-Eva-Quick.csv"

# Read the original file list and take only first 11 lines (header + 10 datasets)
Get-Content $fileListPath | Select-Object -First 11 | Set-Content $tempFileListPath

Write-Host "Created temporary file list with 10 datasets: $tempFileListPath" -ForegroundColor Cyan
Write-Host ""

# List of all models
$models = @(
    # Classical/Statistical Methods
    'Sub_IForest',
    'IForest',
    'Sub_LOF',
    'LOF',
    'POLY',
    'MatrixProfile',
    'NORMA',
    'SAND',
    'Series2Graph',
    'SR',
    'PCA',
    'Sub_PCA',
    'Sub_HBOS',
    'Sub_OCSVM',
    'Sub_MCD',
    'Sub_KNN',
    'KMeansAD_U',
    'KShapeAD',
    'FFT',
    'Left_STAMPi',
    
    # Deep Learning Methods
    'AutoEncoder',
    'CNN',
    'LSTMAD',
    'TranAD',
    'AnomalyTransformer',
    'OmniAnomaly',
    'USAD',
    'Donut',
    'TimesNet',
    'FITS',
    'OFA',
    
    # Foundation Models
    'Lag_Llama',
    'Chronos',
    'TimesFM',
    'MOMENT_ZS',
    'MOMENT_FT',
    'M2N2'
)

Write-Host ("="*80) -ForegroundColor Cyan
Write-Host "QUICK BENCHMARK - ALL MODELS ON 10 DATASETS" -ForegroundColor Cyan
Write-Host "Total models to run: $($models.Count)" -ForegroundColor Cyan
Write-Host "Datasets: 10 (subset)" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan
Write-Host ""

$startTime = Get-Date
$completed = 0
$failed = @()

foreach ($model in $models) {
    $completed++
    Write-Host ""
    Write-Host "[$completed/$($models.Count)] Running model: $model" -ForegroundColor Yellow
    Write-Host ("-"*80) -ForegroundColor Gray
    
    try {
        # Run the model with the quick file list
        python Run_Detector_U.py --AD_Name $model --file_lsit $tempFileListPath --save True
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[SUCCESS] $model completed successfully" -ForegroundColor Green
        } else {
            Write-Host "[FAILED] $model failed with exit code $LASTEXITCODE" -ForegroundColor Red
            $failed += $model
        }
    }
    catch {
        Write-Host "[ERROR] $model encountered an error: $_" -ForegroundColor Red
        $failed += $model
    }
    
    Write-Host ""
}

# Summary
$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host ""
Write-Host ("="*80) -ForegroundColor Cyan
Write-Host "QUICK BENCHMARK COMPLETE" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan
Write-Host "Total models: $($models.Count)" -ForegroundColor White
Write-Host "Successful: $($models.Count - $failed.Count)" -ForegroundColor Green
Write-Host "Failed: $($failed.Count)" -ForegroundColor Red
Write-Host "Total time: $($duration.ToString("hh\:mm\:ss"))" -ForegroundColor White

if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "Failed models:" -ForegroundColor Red
    foreach ($model in $failed) {
        Write-Host "  - $model" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Results saved to: eval/metrics/uni/" -ForegroundColor Cyan
Write-Host "Temp file list: $tempFileListPath" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan
