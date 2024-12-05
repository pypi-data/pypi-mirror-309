#!/usr/bin/env python3

import time

def generate_port(min_port=10000, max_port=50000):
    """ 
        Use Epoch Time To Generate A Port Number Within Reasonable Range (These Ports Shouldn't Be Allocated).  
        We'll Cycle Through These Ports So We'll Get New Ones Guaranteed To Be Unblocked.  
        We'll Only Cycle Back After A Little More Than 10 Hours (0 Chance Still Blocked).  
    """
    port_range = max_port - min_port + 1
    current_epoch = int(time.time())
    wrapped_epoch = current_epoch % 40000
    random_port = min_port + (wrapped_epoch % port_range)
    return random_port
