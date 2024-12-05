import os
import stat
import pkg_resources

PACKAGE_ROOT = 'classhoster'
START_HOSTER_PATH = "main/start_hoster.py"
ROBOT_API_PATH = "public/robot_api.py"

def get_package_file(filename: str):
    filepath = pkg_resources.resource_filename(PACKAGE_ROOT, filename)
    ensure_permissions(filepath)
    return filepath

def get_robot_api():
    return get_package_file(ROBOT_API_PATH)   

def get_start_hoster():
    return get_package_file(START_HOSTER_PATH)    

def ensure_permissions(filepath):
    if os.path.exists(filepath):
        current_permissions = stat.S_IMODE(os.lstat(filepath).st_mode)
        if not current_permissions & stat.S_IEXEC:
            os.chmod(filepath, current_permissions | stat.S_IEXEC)
        if not current_permissions & stat.S_IRUSR:
            os.chmod(filepath, current_permissions | stat.S_IRUSR)
        os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR | stat.S_IEXEC)
