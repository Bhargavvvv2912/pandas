# agent_utils.py

import subprocess
import re
import sys

def start_group(title):
    """Starts a collapsible log group in GitHub Actions."""
    print(f"\n::group::{title}")

def end_group():
    """Ends a collapsible log group in GitHub Actions."""
    print("::endgroup::")

def run_command(command, cwd=None):
    """Runs a command and returns the output, error, and return code."""
    display_command = ' '.join(command)
    if len(display_command) > 200:
        display_command = display_command[:200] + "..."
    # print(f"Running command: {display_command}")
    
    result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    return result.stdout, result.stderr, result.returncode

def validate_changes(python_executable, group_title="Running Validation Script"):
    """
    Runs the Pandas-specific validation process and captures metrics.
    Returns a tuple of (success, metrics_string, full_output).
    """
    start_group(group_title)
    
    print("\n--- Running Pandas Functional Validation ---")
    
    # We assume validation.py is in the same directory as this script.
    validation_command = [python_executable, "validation.py"]
    
    stdout, stderr, returncode = run_command(validation_command)

    if stdout:
        print(f"STDOUT:\n---\n{stdout}\n---")
    if stderr:
        print(f"STDERR:\n---\n{stderr}\n---")

    if returncode != 0:
        print("Validation Failed: validation.py returned a non-zero exit code.", file=sys.stderr)
        end_group()
        return False, None, stdout + stderr
    
    print("Validation script completed successfully.")
    end_group()

    try:
        # Try to parse a metric from the successful run's output
        shape_metric = re.search(r"Final DataFrame shape (.*)", stdout).group(1)
        metrics_body = f"Performance Metrics:\n- Final DataFrame Shape: {shape_metric}"
        return True, metrics_body, stdout + stderr
    except (AttributeError, IndexError):
        # If parsing fails but the script succeeded, it's still a success.
        return True, "Metrics not available, but validation passed.", stdout + stderr