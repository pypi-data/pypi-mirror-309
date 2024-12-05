from classhoster.public.hostclass import host_class
from classhoster.public.systems import robot_systems

def main():
    for system in robot_systems:
        host_class(system) 

if __name__ == "__main__":
   main()