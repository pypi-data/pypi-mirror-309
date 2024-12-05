#!/usr/bin/env python3

import sys
from multiprocessing import Process
from classhoster.public.robot_api import host_class
from classhoster.utility.tools.cmd_line_parser import check_cmd_line
from classhoster.public.loadclass import load_class

def host_a_class(class_type):
    process = Process(target=host_class, args=[class_type])
    process.start()
    
def main():
    check_cmd_line()  
    clz = sys.argv[1]  
    loaded_class = load_class(clz)
    host_a_class(loaded_class)

if __name__ == "__main__":
    main()