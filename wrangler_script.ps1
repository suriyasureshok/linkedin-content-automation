$directories = Get-ChildItem -Path "cloudflare-workers\" -Directory
foreach ($dir in $directories) {
    Write-Host "Deploying $($dir.Name)"
    Set-Location $dir.FullName
    wrangler deploy
    Set-Location ..
}