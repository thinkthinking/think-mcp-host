param(
    [switch]$WithKey = $false
)

# 生成随机密钥
#$key = (openssl rand -hex 16)
#Write-Host "Generated encryption key: $key"

# 基础命令
$command = "pyinstaller --noconfirm --onefile"
$command += " --add-data `"think_mcp_host;think_mcp_host`""
$command += " --add-data `".venv/Lib/site-packages/pyfiglet;pyfiglet`""
$command += " --icon `"think_mcp_host/resources/icons/heart.ico`""
$command += " --name `"AI-Zen-Love`""
#$command += " --key=`"$key`""

if ($WithKey) {
    Write-Host "Including config files in the build..."
    $command += " --add-data `"think_mcp_host/config;think_mcp_host/config`""
}
else {
    Write-Host "Skipping config files in the build..."
}

$command += " `"think_mcp_host/destiny_host.py`""

Write-Host "Executing command: $command"
Invoke-Expression $command

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "Output executable can be found in the 'dist' directory." -ForegroundColor Green
}
else {
    Write-Host "Build failed with exit code $LASTEXITCODE" -ForegroundColor Red
}