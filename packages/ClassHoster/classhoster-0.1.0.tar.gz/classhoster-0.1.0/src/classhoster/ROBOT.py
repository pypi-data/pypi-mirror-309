#!/usr/bin/env python3

from forker import Forker

if __name__ == "__main__":
    Forker.run_scripts(
        [
            "robot.py"
        ]
    )