# Edge更新开关

语言：[English](README.md)

---

使用此脚本禁用Edge浏览器的自动更新，或者再需要时重新启用。

通过关闭当前正在后台运行的Edge更新程序，并将用于更新Edge的相关程序重命名，此脚本能够让Edge无法运行更新程序，从而禁用Edge更新。另外，你还可以再次运行此脚本将这些程序重命名为原来的名称，以便启用Edge更新。

## 运行要求

- Python3

- 操作系统： Windows10+, macOS

- 已安装Edge浏览器

## 注意

需要以管理员身份运行此脚本。

## 用法

1. 下载此项目并进入项目目录

2. 下载必要的Python包

```shell
pip3 install -r requirements.txt
```

3. 以管理员身份运行脚本

- Windows

```batch
python edge_update_switch.py
```

- macOS

```shell
sudo python3 edge_update_switch.py
```

4. 检查运行结果

首次运行时，输出 `Edge update disabled` 说明已禁用Edge自动更新。

再次运行脚本，输出 `Edge update enabled` 说明已启用Edge自动更新。