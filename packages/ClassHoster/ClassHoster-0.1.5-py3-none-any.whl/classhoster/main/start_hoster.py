#!/usr/bin/env python3

import sys
import time
import signal
import multiprocessing
from classhoster.main.hoster import ClassHoster
from classhoster.utility.tools.forker import Forker

def init_class_hoster():
    """
        Initialize ClassHoster and host itself.
    """
    class_hoster = ClassHoster()
    class_hoster.host_class(ClassHoster)

def start_hoster_process():
    """
        Start the ClassHoster in a separate process.
    """
    process = multiprocessing.Process(target=init_class_hoster)
    process.start()
    return process

def start_hoster():
    """
        Main function to coordinate processes and host classes.
    """
    class_hoster_process = start_hoster_process()

    def signal_handler(signum, frame):
        class_hoster_process.terminate()
        exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

def main(): 
    start_hoster()

if __name__ == "__main__":
    main()
