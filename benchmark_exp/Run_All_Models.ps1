# Run All TSB-AD Univariate Models
# This script runs all available anomaly detection models on the evaluation set

# Activate virtual environment
cd "C:\Users\Anne Louise\Documents\GitHub\TSB-AD"
.\venv\Scripts\Activate.ps1
cd benchmark_exp

# List of all models with optimal hyperparameters
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
Write-Host "TSB-AD BENCHMARK - RUNNING ALL MODELS" -ForegroundColor Cyan
Write-Host "Total models to run: $($models.Count)" -ForegroundColor Cyan
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
        # Run the model
        python Run_Detector_U.py --AD_Name $model --save True
        
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
Write-Host "BENCHMARK COMPLETE" -ForegroundColor Cyan
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
Write-Host ("="*80) -ForegroundColor Cyan

