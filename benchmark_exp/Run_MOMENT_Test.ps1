# Test MOMENT Models on 2 Datasets
# This script runs both MOMENT configurations (MOMENT_ZS and MOMENT_FT) on just 2 datasets
# NOTE: Must be run from within the momentfm_3_11 conda environment

# Navigate to benchmark directory
cd "C:\Users\Anne Louise\Documents\GitHub\TSB-AD\benchmark_exp"

# Create a temporary file list with only 2 datasets
$fileListPath = "../Datasets/File_List/TSB-AD-U-Eva.csv"
$tempFileListPath = "../Datasets/File_List/TSB-AD-U-Eva-MOMENT-Test.csv"

# Read the original file list and take only first 3 lines (header + 2 datasets)
Get-Content $fileListPath | Select-Object -First 3 | Set-Content $tempFileListPath

Write-Host "Created temporary file list with 2 datasets: $tempFileListPath" -ForegroundColor Cyan
Write-Host ""

# List of MOMENT models to test
$models = @(
    'MOMENT_ZS',
    'MOMENT_FT'
)

Write-Host ("="*80) -ForegroundColor Cyan
Write-Host "MOMENT MODEL TEST - 2 DATASETS" -ForegroundColor Cyan
Write-Host "Total models to run: $($models.Count)" -ForegroundColor Cyan
Write-Host "Datasets: 2" -ForegroundColor Cyan
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
        # Run the model with the test file list
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
Write-Host "MOMENT TEST COMPLETE" -ForegroundColor Cyan
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
