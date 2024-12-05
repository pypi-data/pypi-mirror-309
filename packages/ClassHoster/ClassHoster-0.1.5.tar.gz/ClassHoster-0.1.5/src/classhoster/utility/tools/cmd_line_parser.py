import sys

def check_cmd_line():
    if len(sys.argv) < 2:
        print("Please provide the class to host (e.g., mymodule.MyClass).")
        return