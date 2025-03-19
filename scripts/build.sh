#!/bin/bash

# 检查参数
WITH_KEY=false
if [ "$1" == "--with-key" ]; then
    WITH_KEY=true
fi

# 清理之前的构建
rm -rf build dist *.spec

# 确保目录存在
mkdir -p build dist

# 获取 pyfiglet 路径
PYFIGLET_PATH=$(python -c "import pyfiglet; import os; print(os.path.dirname(pyfiglet.__file__))")
echo "PyFiglet path: $PYFIGLET_PATH"

# 基础命令
COMMAND=(
    "pyinstaller --noconfirm"
    "--clean"  # 清理之前的构建
    "--onefile"  # 创建单文件包
    "--add-data think_mcp_host:think_mcp_host"
    "--add-data think_mcp_host/resources:think_mcp_host/resources"
    "--add-data $PYFIGLET_PATH/fonts:pyfiglet/fonts"  # 添加 pyfiglet 字体
    "--name AI-Zen-Love-bin"  # 改名为 bin 文件
    "--target-arch arm64"  # 明确指定目标架构
    "--codesign-identity=-"  # 跳过代码签名
    "--osx-bundle-identifier com.thinkthinking.aizenapp"  # 添加 bundle identifier
    "--icon think_mcp_host/resources/icons/heart.icns"  # 添加应用图标
)

# 根据 WITH_KEY 参数决定是否包含配置文件
if [ "$WITH_KEY" = true ]; then
    echo "Including config files in the build..."
    COMMAND+=("--add-data think_mcp_host/config:think_mcp_host/config")
else
    echo "Skipping config files in the build..."
fi

# 添加主程序文件
COMMAND+=("think_mcp_host/destiny_host.py")

# 合并命令并执行
FINAL_COMMAND="${COMMAND[*]}"
echo "Executing command: $FINAL_COMMAND"
eval "$FINAL_COMMAND"

# 检查构建结果
if [ $? -eq 0 ]; then
    echo -e "\033[32mBuild completed successfully!\033[0m"
    echo -e "\033[32mOutput .app can be found in the 'dist' directory.\033[0m"
    
    # 构建完成后创建 .app 包装
    echo "Creating .app bundle..."
    APP_DIR="dist/AI-Zen-Love.app"
    mkdir -p "$APP_DIR/Contents/MacOS"
    mkdir -p "$APP_DIR/Contents/Resources"

    # 复制可执行文件和启动器
    cp "dist/AI-Zen-Love-bin" "$APP_DIR/Contents/MacOS/"
    cp "scripts/launcher.sh" "$APP_DIR/Contents/MacOS/AI-Zen-Love"

    # 复制图标
    cp "think_mcp_host/resources/icons/heart.icns" "$APP_DIR/Contents/Resources/"

    # 创建 Info.plist
    cat > "$APP_DIR/Contents/Info.plist" << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>AI-Zen-Love</string>
    <key>CFBundleIconFile</key>
    <string>heart.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.thinkthinking.aizenapp</string>
    <key>CFBundleName</key>
    <string>AI·禅·爱</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOL

    # 设置可执行权限
    chmod +x "$APP_DIR/Contents/MacOS/AI-Zen-Love"
    chmod +x "$APP_DIR/Contents/MacOS/AI-Zen-Love-bin"

    echo "Application bundle has been created at: $APP_DIR"
else
    echo -e "\033[31mBuild failed!\033[0m"
    exit 1
fi
