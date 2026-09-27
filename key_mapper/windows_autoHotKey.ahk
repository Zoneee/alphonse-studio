; AutoHotkey v2 脚本

; 字符文档 https://wyagd001.github.io/v2/docs/Hotkeys.htm#Symbols
; 这里列出一些常用的
; $ 避免触发自身。在 send 的内容包括快捷键的内容时使用。例如：$^!l::Send ^{Right} send内容和快捷键同时包含Ctrl
; ! Alt
; ^ Ctrl
; + Shift
; # Win

; 键盘定义
; ijkl uo 与上下左右/home/end绑定
; wasd qe 与Shlft+上下左右/home/end绑定
; Ctrl 主要与应用级键位绑定
; Shlft 主要与Edit绑定

; 不论输入法状态都输入`
`::Send("{U+0060}")

; 最小化当前窗口
!Esc::WinMinimize("A")

; 发送箭头键输入
$!j::Send("{Left}")  ; 按下 Alt+j 发送左箭头键
$^!j::Send("^Left")  ; 按下 Ctrl+Alt+j 发送 Ctrl+左箭头键
$!l::Send("{Right}")  ; 按下 Alt+l 发送右箭头键
$^!l::Send("^Right")  ; 按下 Ctrl+Alt+l 发送 Ctrl+右箭头键
$!i::Send("{Up}")  ; 按下 Alt+i 发送上箭头键
$!k::Send("{Down}")  ; 按下 Alt+k 发送下箭头键

; 发送 Shlft+箭头输入
$!w::Send("+{Up}") ; 按下 Alt+q 发送 Shlft+Up
$!s::Send("+{Down}") ; 按下 Alt+q 发送 Shlft+Down
$!a::Send("+{Left}") ; 按下 Alt+q 发送 Shlft+Left
$!d::Send("+{Right}") ; 按下 Alt+q 发送 Shlft+Right
; ~$!q::Send("+{Home}") ; 按下 Alt+q 发送 Shlft+Home（并向下传递 Alt+q）
$!q::Send("+{Home}") ; 按下 Alt+q 发送 Shlft+Home（并向下传递 Alt+q）
$!e::Send("+{End}") ; 按下 Alt+e 发送 Shlft+End

; 打开工作路径
#1::Run("D:\W_workflower")  ; 按下 Win+1

; 窗口操作和输入发送
#$Enter::WinSetAlwaysOnTop("A")  ; 按下 Win+Shift+Enter 设置当前窗口为总在最前
#$Insert::Send("``")  ; 按下 Win+Shift+Insert 发送反引号字符

; 发送 Home 和 End 键输入，并使用 Shift 进行修改
; $^u::Send("{Home}")  ; 按下 Ctrl+u 发送 Home 键
; $^o::Send("{End}")  ; 按下 Ctrl+o 发送 End 键
$!u::Send("{Home}")  ; 按下 Alt+u 发送 Home 键
$!o::Send("{End}")  ; 按下 Alt+o 发送 End 键
; $+u::Send("{Shift Down}{Home}{Shift Up}")  ; 按下 Shift+u 发送 Shift+Home
; $+o::Send("{Shift Down}{End}{Shift Up}")  ; 按下 Shift+o 发送 Shift+End

; 修复占用Ctrl+o问题
$^r::Send("^o")

; 发送 Delete 和 Backspace 键，以及一些自定义输入
$!m::Send("{Delete}")  ; 按下 m 发送 Delete 键
$!n::Send("{Backspace}")  ; 按下 < 发送 Backspace 键
; $a::Send("~")  ; 按下 a 发送波浪号

; 将鼠标光标左移和右移 10 像素
$!7::Send("{Left 10}")  ; 按下 7 发送光标左移 10 像素
$!9::Send("{Right 10}")  ; 按下 9 发送光标右移 10 像素

; 定义 Alt + Caps Lock 发送 Alt + F4
; !CapsLock::Send("!{F4}")

; 定义Caps Lock 发送 Enter
; CapsLock::Send("{Enter}")

; 更改屏幕分辨率
; #!End::ChangeResolution(1920, 1080)  ; 按下 Win+Alt+End 更改分辨率为 1920x1080
; #!Home::ChangeResolution(3840, 2160)  ; 按下 Win+Alt+Home 更改分辨率为 3840x2160

; ; 鼠标按键输入
; LShift & RButton::SendInput("{LButton 2}")  ; 按下 Left Shift+Right Button 发送左键双击

; ; 键盘布局控制（中英文切换）
; ; 切换到中文输入法
; ' Space & j::SetDefaultKeyboard(0x0409)  ; 按下空格+j 切换到中文输入法
; ; 切换到英文输入法
; ' Space & `::SetDefaultKeyboard(0x0804)  ; 按下空格+` 切换到英文输入法
; ' Space & `::SetDefaultKeyboard(0x0804)  ; 按下空格+` 再次切换到英文输入法
; ' Space::Send("{Space}")  ; 按下空格发送空格字符

; ; 切换到中文输入法
; LAlt & j::SetDefaultKeyboard(0x0804)  ; 按下 Left Alt+j 切换到中文输入法
; ; 切换到英文输入法
; LAlt & `::SetDefaultKeyboard(0x0409)  ; 按下 Left Alt+` 切换到英文输入法
