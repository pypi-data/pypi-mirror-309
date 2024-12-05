#!/usr/bin/env python3

from classhoster.utility.tools.forker import Forker
from classhoster.utility.tools.file_reader import get_start_hoster

def main():
    Forker.run_scripts(
        [
            get_start_hoster()
        ]
    )
    
if __name__ == "__main__":
    main()