param(
    [switch]$WithKey = $false
)

# 1. 使用 PyArmor 混淆代码
$pyarmor_command = "pyarmor gen --output obf_dist think_mcp_host"
Write-Host "Obfuscating code with PyArmor..."
Invoke-Expression $pyarmor_command

if ($LASTEXITCODE -ne 0) {
    Write-Host "PyArmor obfuscation failed!" -ForegroundColor Red
    exit 1
}

# 2. 修改 PyInstaller 命令，指向混淆后的入口文件
$command = "pyinstaller --noconfirm --onefile"
$command += " --hidden-import asyncio"
$command += " --hidden-import platform"
$command += " --hidden-import argparse"
$command += " --hidden-import os"
$command += " --hidden-import re"
$command += " --hidden-import sys"
$command += " --hidden-import time"
$command += " --hidden-import datetime"
$command += " --hidden-import importlib.metadata"
$command += " --hidden-import pathlib"
$command += " --hidden-import dotenv"
$command += " --hidden-import prompt_toolkit"
$command += " --hidden-import prompt_toolkit.application"
$command += " --hidden-import prompt_toolkit.key_binding"
$command += " --hidden-import prompt_toolkit.keys"
$command += " --hidden-import rich.align"
$command += " --hidden-import rich.panel"
$command += " --hidden-import rich.prompt"
$command += " --hidden-import think_llm_client.cli"
$command += " --hidden-import think_llm_client.utils.display"
$command += " --hidden-import think_llm_client.utils.logger"
$command += " --hidden-import think_llm_client.utils.terminal_config"
$command += " --hidden-import think_mcp_client"
$command += " --hidden-import think_mcp_client.mcp_processor"
$command += " --collect-all prompt_toolkit"
$command += " --collect-all rich"
$command += " --collect-all think_llm_client"
$command += " --collect-all think_mcp_client"
$command += " --add-data `"obf_dist\think_mcp_host;think_mcp_host`""          # 添加混淆后的代码
$command += " --add-data `".venv\Lib\site-packages\pyfiglet;pyfiglet`""       # 保留原资源
$command += " --icon `"think_mcp_host\resources\icons\heart.ico`""
$command += " --name `"AI-Zen-Love`""

# 3. 选择性包含配置文件（根据 -WithKey 参数）
if ($WithKey) {
    Write-Host "Including config files in the build..."
    $command += " --add-data `"think_mcp_host\config;think_mcp_host\config`""
} else {
    Write-Host "Skipping config files in the build..."
}

# 4. 指定混淆后的入口脚本路径
$command += " `"obf_dist\think_mcp_host\destiny_host.py`""

# 5. 执行 PyInstaller 打包
Write-Host "Executing PyInstaller command: $command"
Invoke-Expression $command

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

# 6. 等待一小段时间以确保所有文件操作完成
Start-Sleep -Seconds 2

# 7. 清理临时文件
Remove-Item -Recurse -Force obf_dist

# 8. 检查结果
if ($LASTEXITCODE -eq 0) {
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "Output executable can be found in the 'dist' directory." -ForegroundColor Green
} else {
    Write-Host "Build failed with exit code $LASTEXITCODE" -ForegroundColor Red
}