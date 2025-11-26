# Run Fast Classical Models Only (for quick benchmarking)
# Skips slow deep learning and foundation models

cd "C:\Users\Anne Louise\Documents\GitHub\TSB-AD"
.\venv\Scripts\Activate.ps1
cd benchmark_exp

# Fast classical methods only
$models = @(
    'IForest',
    'LOF',
    'PCA',
    'Sub_PCA',
    'Sub_HBOS',
    'Sub_KNN',
    'KMeansAD_U',
    'FFT'
)

Write-Host ("="*80) -ForegroundColor Cyan
Write-Host "RUNNING FAST CLASSICAL MODELS ONLY" -ForegroundColor Cyan
Write-Host "Total models: $($models.Count)" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan

$completed = 0
foreach ($model in $models) {
    $completed++
    Write-Host ""
    Write-Host "[$completed/$($models.Count)] Running: $model" -ForegroundColor Yellow
    python Run_Detector_U.py --AD_Name $model --save True
    Write-Host "[OK] $model completed" -ForegroundColor Green
}

Write-Host ""
Write-Host ("="*80) -ForegroundColor Cyan
Write-Host "FAST MODELS COMPLETE!" -ForegroundColor Green
Write-Host ("="*80) -ForegroundColor Cyan
