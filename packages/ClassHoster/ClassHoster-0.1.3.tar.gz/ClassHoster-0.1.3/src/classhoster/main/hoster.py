import os
import inspect
from typing import Type, Any
from multiprocessing import Process
from classhoster.main.gen_srv import start_generic_server
from classhoster.utility.tools.port_allocator import generate_port
from classhoster.utility.tools.file_reader import get_robot_api

output_file = get_robot_api()

class ClassHoster:

    _instance = None

    """
        Singleton since we are using class hoster to host itself
    """
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClassHoster, cls).__new__(cls)
            with open(output_file, 'w') as f:
                f.write(f"# Generated stubs for All Classes Hosted By ClassHoster\n\n")
                f.write(f"from classhoster.main.client import call_service\n")
                f.write(f"from classhoster.utility.types.req_resp import GenericRequest\n")
                f.write("")
            cls._instance.port = generate_port()
        return cls._instance

    def host_class(self, class_type: Type[Any]):
        name = class_type.__name__
        port = self._allocate_new_port()
        self._generate_function_stubs(class_type, port)
        process = Process(target=start_generic_server, args=[name, port, class_type])
        process.start()
        return None

    def _allocate_new_port(self):
        self.port += 1
        port = self.port
        return port

    @staticmethod
    def _generate_function_stubs(class_type: Type[Any], class_port: int):
        functions = inspect.getmembers(class_type, predicate=inspect.isfunction)
        with open(output_file, 'a') as f:
            f.write(f"# Generated stubs for class_type: {class_type.__name__}\n\n")
            for func_name, func in functions:
                if func_name.startswith('_'):
                    continue
                signature = inspect.signature(func)
                params = [param.name for param in signature.parameters.values() if param.name != 'self']
                param_str = ', '.join(str(param) for param in params)
                args_dict = ', '.join(f'"{param}": {param}' for param in params)
                f.write(f"def {func_name}({param_str}):\n")
                f.write(f"   return call_service(port={class_port}, \n"
                        f"      request=GenericRequest(function=\"{func_name}\", \n"
                        f"      args={{{args_dict}}}))\n\n")

def main():
    classHoster = ClassHoster()
    classHoster.host_class(ClassHoster)

if __name__ == "__main__":
    main()