#!/usr/bin/env python3
from classhoster.utility.types.req_resp import GenericRequest

class Defaults:
    DEFAULT_NAME    = "Generic"
    LOCALHOST       = '127.0.0.1'
    PORT            = 10000
    BUFFER_SIZE     = 1024

    """ Example Callback """
    REQUEST = GenericRequest("Default Function", {"arg1": "default"})  
    @staticmethod
    def default_callback(request: GenericRequest):
        return print(
            f"{request.function} called with {request.args} args"
        )
    """ ############### """