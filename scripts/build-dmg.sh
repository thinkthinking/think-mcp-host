#!/bin/bash

# 首先运行原有的构建脚本
./scripts/build.sh "$@"

# 检查构建是否成功
if [ $? -ne 0 ]; then
    echo -e "\033[31mBuild failed! Aborting DMG creation.\033[0m"
    exit 1
fi

echo "Creating DMG package..."

# 设置变量
APP_NAME="AI-Zen-Love"
DMG_NAME="${APP_NAME}.dmg"
VOLUME_NAME="AI·禅·爱"
SOURCE_APP="dist/${APP_NAME}.app"
DMG_PATH="dist/${DMG_NAME}"

# 确保删除旧的 DMG 文件
rm -f "${DMG_PATH}"

# 创建临时 DMG
echo "Creating temporary DMG..."
hdiutil create -srcfolder "${SOURCE_APP}" -volname "${VOLUME_NAME}" -fs HFS+ \
        -fsargs "-c c=64,a=16,e=16" -format UDRW -size 200m "dist/temp.dmg"

# 挂载临时 DMG
echo "Mounting temporary DMG..."
DEVICE=$(hdiutil attach -readwrite -noverify -noautoopen "dist/temp.dmg" | \
         egrep '^/dev/' | sed 1q | awk '{print $1}')

# 设置卷的图标排列方式和背景
echo '
   tell application "Finder"
     tell disk "'${VOLUME_NAME}'"
           open
           set current view of container window to icon view
           set toolbar visible of container window to false
           set statusbar visible of container window to false
           set the bounds of container window to {400, 100, 900, 400}
           set theViewOptions to the icon view options of container window
           set arrangement of theViewOptions to not arranged
           set icon size of theViewOptions to 128
           close
           open
           update without registering applications
           delay 5
           close
     end tell
   end tell
' | osascript

# 创建应用程序文件夹的符号链接
echo "Creating Applications symlink..."
pushd "/Volumes/${VOLUME_NAME}" > /dev/null
ln -s /Applications
popd > /dev/null

# 设置权限
echo "Setting permissions..."
chmod -Rf go-w "/Volumes/${VOLUME_NAME}"

# 卸载临时 DMG
echo "Unmounting temporary DMG..."
sync
hdiutil detach "${DEVICE}"

# 转换 DMG 格式
echo "Converting DMG..."
hdiutil convert "dist/temp.dmg" -format UDZO -o "${DMG_PATH}"
rm -f "dist/temp.dmg"

# 完成
echo -e "\033[32mDMG package created successfully!\033[0m"
echo -e "\033[32mOutput DMG can be found at: ${DMG_PATH}\033[0m"
