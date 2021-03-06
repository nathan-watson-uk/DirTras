# DirTras

Automated Directory Traversal Exploitation Tool

This tool allows for the automation of directory traversal for windows and linux based file system.

![Screenshot](https://raw.githubusercontent.com/Nate-one/DirTras/master/content/img1.png)


# Benchmark

* [DVWA](https://github.com/ethicalhack3r/DVWA) (low/medium/high)
* [VulnHub Seattle 0.0.3](https://www.vulnhub.com/entry/seattle-v03,145/)

# Installation
```
git clone https://github.com/Nate-one/DirTras
```

# Requirements
```
python -m pip install requests
```

# Usage

Example:
```
# Example of DVWA (Hard) Exploitation
dirtras.py -u http://192.168.28.129/DVWA-master/vulnerabilities/fi/?page=include.php --output C:\\Users\\nate\\projects\\DirTras\\output --target-os linux --host-system windows --L1 -c uif2fs4mpdqv6undddgmpgf9m0,high,1,USD --cookie-name PHPSESSID,security,level,lang
```

![Screenshot](https://raw.githubusercontent.com/Nate-one/DirTras/master/content/img2.png)


# Legal Disclaimer

Usage of DirTras for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.


# Note

Currently the best way to change the scan intersity is by modifying the deep_directory_list.txt file.
This will be changed in the future so you can use a level system to change intensity.
