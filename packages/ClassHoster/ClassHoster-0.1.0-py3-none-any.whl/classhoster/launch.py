#!/usr/bin/env python3

from forker import Forker

def main():
    Forker.run_scripts(
        [
            "robot.py"
        ]
    )
    
if __name__ == "__main__":
    main()