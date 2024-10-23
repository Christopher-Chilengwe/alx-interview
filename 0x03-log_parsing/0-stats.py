#!/usr/bin/python3
"""
Log Parsing Script
"""
import sys
import re
import signal

# Initialize counters and data storage
log = {
    "file_size": 0,
    "code_frequency": {str(code): 0 for code in [200, 301, 400, 401, 403, 404, 405, 500]}
}
line_count = 0

# Regular expression to match the required log format
log_regex = re.compile(
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} - \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+\] "GET /projects/260 HTTP/1.1" (\d{3}) (\d+)'  # regex to capture status code and file size
)

# Output statistics
def output(log):
    """
    Helper function to display statistics
    """
    print("File size: {}".format(log["file_size"]))
    for code in sorted(log["code_frequency"]):
        if log["code_frequency"][code] > 0:
            print("{}: {}".format(code, log["code_frequency"][code]))

# Signal handler for handling Ctrl+C (SIGINT)
def signal_handler(sig, frame):
    """
    Handle Ctrl+C signal
    """
    output(log)
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Main logic: read stdin and process lines
try:
    for line in sys.stdin:
        match = log_regex.match(line.strip())
        if match:
            line_count += 1
            code = match.group(1)
            file_size = int(match.group(2))

            # Update file size
            log["file_size"] += file_size

            # Update status code count
            if code in log["code_frequency"]:
                log["code_frequency"][code] += 1

            # Print statistics every 10 lines
            if line_count % 10 == 0:
                output(log)
finally:
    # Ensure output is printed when exiting
    output(log)
