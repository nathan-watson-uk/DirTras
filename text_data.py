help_info = """

Usage Example:

>dirtras.py -u http://192.168.28.129/download.php?item= -p 80 --L1

-H  --help      Display this menu

-u  --url       Set the URL to traverse
-o  --output    Specify output folder directory
-p  --port      Set the port (default is 80)
-f  --file      Use a file of custom traversal directories

    --host-system   Define the OS that dirtras is running on (Default linux)

    --L1        Light Traversal
    --L2        Medium Traversal
    --L3        Heavy Traversal

Note: Unless the website is behind a login you typically don't need to use cookies

-c  --cookie        Use a session cookie, mainly used if page is behind a login
-n  --cookie-name   Use this to define the name of the cookie (PHPSESSID etc)

(To use multiple cookies seperate each name/cookie with a comma (,) and place in respective order.)
e.g --cookie-name PHPSESSID,security -c uif2fs4mpdqv6undddgmpgf9m0,low

-d  --delay     Set a delay between requests (Default is 0.01)
    --target-os        Define what OS the web server is on (linux/windows) (Default linux)

-b  --bugs      Display currently known bugs and problems

If you're getting a [WinError 10048] error or similar ephemeral port exhaustion, try increasing the delay.


Upcoming Features:

Level of scans (-l1 -l2 -l3)
    To determine how intensive a scan which will increase/decrease number of packets

Performance Improvements and Bug Fixes
    General fixes to issues stated in bug info (-b --bugs)
"""

bug_info = """

KNOWN DIRTRAS BUGS:

--- 1 ---
/proc/self/cwd/index.php 
Was removed from linux_files.txt because it crashed DVWA during testing.
Feel free to add it back but if you get HTTPConnectionPool Read timed out error than that might be it.

--- 2 ---

[WinError 10048]
Ephemeral Port Exhausation is a problem when sending thousands of requests in a short span of time.
To mitigate this I increased the delay to 0.02 and that seemed to work. However, you may want it higher.
The way to fix this would be by using connection pools which allows the connection to be reused but I can't
seem to currently get this to work.

--- 3 ---
fail_traversal
Whilst the variable fail_traversal is sent as \"../thisdoesntwork\" it hasn't been fully tested so
it may not always provide accruate results for what a failed traversal looks like.

--- 4 ---
file_counter | files_to_get
This counter is used purely to give the user an idea of how many files have been retrieved so far.
It isn't meant to be accurate as the system around detecting files is pretty poor at the moment.
This might mean that the counter goes higher than the expected number of files to get and that's
probably due to tcp/udp files increasing and decreasing in size.


"""

run_info = r"""

██████  ██ ██████  ████████ ██████   █████  ███████ 
██   ██ ██ ██   ██    ██    ██   ██ ██   ██ ██      
██   ██ ██ ██████     ██    ██████  ███████ ███████ 
██   ██ ██ ██   ██    ██    ██   ██ ██   ██      ██ 
██████  ██ ██   ██    ██    ██   ██ ██   ██ ███████             
      by Nathan Watson                                      

Automated Directory Traversal Exploitation Tool

This tool allows for the automation of directory traversal for windows and linux based file systems.

(This is currently a work in progress so expect bugs)

Created by @Nathan-Watson-UK
https://github.com/nathan-watson-uk

Tested On:
VulnHub - Seattle 0.0.3
DVWA (Low, Medium, High)

Use -H or --help for the usage menu

"""
