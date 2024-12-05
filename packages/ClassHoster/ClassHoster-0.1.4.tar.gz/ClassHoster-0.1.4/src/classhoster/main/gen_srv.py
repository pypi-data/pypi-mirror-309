#!/usr/bin/env python3

from classhoster.utility.types.req_resp import GenericRequest
from classhoster.main.server import start_server

def generic_callback(request: GenericRequest, object): 
    """ 
        This will work for any class, think of this like a way to call a function of another process (you don't have access to the object, just a port)
        When the port is hit with a request it uses reflection to get a pointer to the function of the name passed in
        Then it calls the function using variable dictionary args (kwargs) so the user can pass in any number of arguments by name
    """
    function_call = getattr(object, request.function)
    return function_call(**request.args)

def start_generic_server(name: str, port: str, classtype):
    """ 
        Instantiate any custom class type (before calling this) and pass it in as object param
        Setup your class on any (free) port you like with whatever name you like
    """
    object = classtype()
    try:
        start_server(name=name, port=port, callback=lambda request: generic_callback(request, object))
    except KeyboardInterrupt:
        print("Shutting down server...")
