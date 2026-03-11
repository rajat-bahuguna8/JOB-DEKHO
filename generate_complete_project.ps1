# PowerShell Script to Generate Complete JOB DEKHO Project Files

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  JOB DEKHO - Complete Project Setup  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "C:\Users\PC\Desktop\Job_Dekho"
Set-Location $projectRoot

# Create necessary directories
Write-Host "Creating directory structure..." -ForegroundColor Yellow
$directories = @(
    "templates",
    "templates\admin",
    "templates\student",
    "templates\company",
    "static",
    "static\css",
    "static\js",
    "static\images",
    "uploads",
    "uploads\resumes"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ Created $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Project structure created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run: pip install -r requirements.txt"
Write-Host "2. Run: python init_db.py  (to create database)"
Write-Host "3. Run: python app.py      (to start the application)"
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
