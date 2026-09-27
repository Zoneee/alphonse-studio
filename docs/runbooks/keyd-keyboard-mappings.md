# keyd 键盘映射启用与维护

## 适用场景

在 Linux Mint 主机上启用或更新仓库中的 keyd 键盘映射，检查加载状态，或撤销这份映射。

配置源文件为 `key_mapper/linux_keyd.conf`。当前配置会匹配 keyd 管理的所有键盘（`[ids] *`）。

## 操作前检查

在仓库根目录运行：

```bash
systemctl is-active keyd
keyd --version
keyd check /home/alphonse/projects/alphonse-studio/key_mapper/linux_keyd.conf
ls -la /etc/keyd
```

- `systemctl is-active keyd` 应返回 `active`。
- `keyd check` 应返回 `No errors found.`。
- 检查 `/etc/keyd/default.conf` 是否已存在。若已有文件或链接，先检查其内容和用途，不要覆盖。

## 启用配置

确认 `/etc/keyd/default.conf` 不存在后，创建指向仓库配置的软链接：

```bash
sudo ln -s /home/alphonse/projects/alphonse-studio/key_mapper/linux_keyd.conf /etc/keyd/default.conf
sudo keyd check /etc/keyd/default.conf
sudo keyd reload
```

验证服务仍在运行并检查加载日志：

```bash
systemctl is-active keyd
sudo journalctl -u keyd -b -n 50 --no-pager
```

日志中应能看到 keyd 解析 `/etc/keyd/default.conf`，并为键盘设备匹配该配置。实际按键确认时，可在文本编辑器中按 Caps Lock，预期行为是输入 Enter。

## 更新配置

编辑 `key_mapper/linux_keyd.conf` 后，先验证语法，再让 keyd 重新读取：

```bash
keyd check /home/alphonse/projects/alphonse-studio/key_mapper/linux_keyd.conf
sudo keyd reload
```

软链接会继续指向仓库文件，但 keyd 不会因文件编辑而自动 reload。

## 反引号映射

配置使用 keyd 的 Unicode 输出生成字面反引号。X11 下需要让 keyd 的 Compose 定义可用；本机 keyd 安装路径可用以下命令设置：

```bash
ln -s /usr/local/share/keyd/keyd.compose ~/.XCompose
```

如果 `~/.XCompose` 已存在，先检查并合并所需 Compose 定义，不要覆盖已有文件。设置后需要重新启动相关应用。当前输入法仍可能拦截 Compose 序列，因此应单独验证 `grave` 和 `Super+Shift+Insert` 两个反引号映射。

## 已知未映射的 AHK 动作

keyd 只重映射键盘事件，当前文件不实现以下依赖桌面或应用的 AHK 行为：

- Alt+Escape 最小化当前窗口。
- Super+1 打开 Windows 路径 `D:\W_workflower`。
- Super+Shift+Enter 切换窗口置顶。

此外，Alt+7 和 Alt+9 按 AHK 实际发送 10 次 Left/Right 键；原 AHK 注释提到鼠标移动，但代码没有发送鼠标事件。

## 撤销

先确认链接仍指向本仓库的配置文件：

```bash
readlink /etc/keyd/default.conf
```

确认输出为 `/home/alphonse/projects/alphonse-studio/key_mapper/linux_keyd.conf` 后，删除链接并 reload：

```bash
sudo rm /etc/keyd/default.conf
sudo keyd reload
```

这只会删除 `/etc/keyd/default.conf` 软链接，不会删除仓库中的配置文件。若链接已指向其他文件，先停止并查明其用途。

## 维护提示

软链接依赖仓库保持在原路径。若仓库被移动、删除或目标权限发生变化，keyd 将无法读取该配置；此时可恢复路径，或将配置复制到 `/etc/keyd/default.conf` 并由 root 管理。
