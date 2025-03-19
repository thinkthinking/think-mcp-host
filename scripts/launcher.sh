#!/bin/bash

# 获取应用程序包的路径
APP_PATH=$(dirname "$(dirname "$(dirname "$0")")")
EXECUTABLE="$APP_PATH/Contents/MacOS/AI-Zen-Love-bin"

# 打开终端并运行程序
osascript <<EOF
tell application "Terminal"
    activate

    # 创建新窗口并运行程序（等待窗口初始化）
    do script "export TERM=xterm-256color && export COLORTERM=truecolor && cd \"$APP_PATH/Contents/MacOS\" && \"$EXECUTABLE\"; exit"

    # 等待窗口创建完成
    delay 1

    # 设置窗口属性
    tell front window
        # 设置背景颜色（黑色）和透明度
        set background color to {0, 0, 0}
        set transparency to 0.2

        # 设置文字颜色（白色）和光标颜色（白色）
        set normal text color to {65535, 65535, 65535}  # RGB 白色
        set cursor color to {65535, 65535, 65535}        # RGB 白色

        # 设置字体大小（需在 Profile 中预先配置支持）
    end tell

    # 进入全屏模式（可选）
    delay 0.5
    activate
    tell application "System Events"
        keystroke "f" using {command down, control down}
    end tell
end tell
EOF