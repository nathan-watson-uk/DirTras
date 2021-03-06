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
dirtras.py -u http://192.168.28.129/DVWA-master/vulnerabilities/fi/?page=include.php -p 80 --L3 --host-system windows --target-os linux --output C:\\Users\\nate\\Projects\\dirtras\\output
```

![Screenshot](https://raw.githubusercontent.com/Nate-one/DirTras/master/content/img2.png)


# Legal Disclaimer

Usage of DirTras for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

