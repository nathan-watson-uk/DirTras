# DirTras

Automated Directory / Path Traversal Exploitation Tool

This tool allows for the automation of directory traversal for windows and linux file systems.

![Screenshot](https://raw.githubusercontent.com/Nate-one/DirTras/master/content/img1.png)


# Benchmark

* [DVWA](https://github.com/ethicalhack3r/DVWA) (low/medium/high)
* [VulnHub Seattle 0.0.3](https://www.vulnhub.com/entry/seattle-v03,145/)

# Testing

Tested on Windows 10 20H2, Ubuntu 20.04.2 and Kali Linux 2021.1 | Using Python 3.8

Please raise an issue if you encounter any problems.

Alternatively join our [Discord Server](https://discord.gg/wz9X6pTrZm).


# Installation
```
git clone https://github.com/Nate-one/DirTras
```

# Requirements
```
Python 3 | Requests 2.25.1 or above
```

```
python -m pip install requests
```

## Don't have pip?
```
Apt:
sudo apt-get install python3-pip

Yum:
sudo yum install epel-release
sudo yum install python-pip
```

# Usage
Example:
```
# Example of DVWA (Hard) Exploitation
dirtras.py -u http://192.168.28.129/DVWA-master/vulnerabilities/fi/?page=include.php -p 80 --L3 --host-system windows --target-os linux --output C:\\Users\\nate\\Projects\\dirtras\\output
```

```
# Use -h or --help to access DirTras flags
```

![Screenshot](https://raw.githubusercontent.com/Nate-one/DirTras/master/content/img2.png)


# Discord

To ask questions, keep up with development and join our community:

* [Join The Discord Server]([Discord Server](https://discord.gg/wz9X6pTrZm).)

# Legal Disclaimer

Usage of DirTras for attacking targets without prior mutual consent is illegal. 
It's the end user's responsibility to obey all applicable local, state and federal laws. 
Developers assume no liability and are not responsible for any misuse or damage caused by this program.

This tool was developed specifically for educational and professional security testing.

