# DirTras
## _An Automated Solution for Directory Traversal Attacks_

_A web application testing tool used to automate directory traversal (path traversal/local file inclusion) on Windows and Linux file systems._


```
usage: dirtras.py [-h] [--help] -u URL [--target-os {linux,windows}] [-p PORT]
                  [-d DELAY] [-f FILE] [-o OUTPUT] [-c COOKIES]
                  [--cookie-name COOKIE_NAME] [--host-system {linux,windows}]
                  [-b] [--L1] [--L2] [--L3]
```

## Installation

DirTras likely requires [Python 3 - 3.8+](https://www.python.org/) to run.

Git Clone the repository & navigate to the directory

```bash
git clone https://github.com/nathan-watson-uk/DirTras.git

cd DirTras
```

Install the requirements:

```bash
pip3 install -r requirements.txt
```

Run the script and view the usage page:
```bash
python3 dirtras.py --help
```

## Known Issues -

- Ephemeral Port Exhaustion, please modify the delay if this is encountered
- /proc/self/cwd/index.php is not included due to crashing DVWA host, please add it back manually if you wsh
- To determine a path that does not exist, "/thisdoesntwork" is used. If this exists, the script will return false positives
- The file counter can be buggy at times



## Disclaimer -

The DirTras tool is provided for educational and research purposes only. By using this tool, you acknowledge and agree that:

- **User Responsibility**: You are solely responsible for your use of DirTras and any consequences thereof. The developers of DirTras shall not be responsible for any misuse or illegal use of this tool by users.

- **Legal Compliance**: You will comply with all applicable laws, regulations, and ethical standards governing your use of this tool, including but not limited to data protection laws and regulations.