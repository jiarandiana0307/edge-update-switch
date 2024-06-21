# Edge Update Switch

Language: [中文](README.zh_CN.md)

---

Use this script to disable automatic updates of Microsoft Edge, or enable it whenever you want.

By terminating the update programs running in the background and renaming the relevant programs for updating Edge, this script is capable to making Edge failed to run the update programs, disabling Edge updating. Also, you can run the script again to rename these programs to their original names, so as to enable Edge updates.

## Requirements

- Python3

- Supported OS: Windows10+, macOS

- Microsoft Edge installed

## Note

Must run this script as admin.

## Usage

1. Download this project then enter into the project directory

2. Download necessary python packages

```shell
pip3 install -r requirements.txt
```

3. Run the script as admin

- Windows

```batch
python edge_update_switch.py
```

- macOS

```shell
sudo python3 edge_update_switch.py
```

4. Check the result

For the first time, it will output `Edge update disabled`, which means automatic Edge update is disabled.

Run the scirpt again, it will output `Edge update enabled`, which means automatic Edge update is enabled again.