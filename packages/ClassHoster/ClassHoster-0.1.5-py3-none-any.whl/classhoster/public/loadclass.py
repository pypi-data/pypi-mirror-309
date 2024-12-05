import importlib

def load_class(class_name: str):
    try:
        module_name, class_name = class_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        class_obj = getattr(module, class_name)
        return class_obj
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error loading class {class_name}: {e}")
        return None

