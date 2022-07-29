import os
import importlib

__commands_path = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(__commands_path):
    for file in files:
        if file == "__init__.py": continue
        if not file.endswith(".py"): continue

        module_name = root + "." + file

        spec = importlib.util.spec_from_file_location(module_name, os.path.join(__commands_path, root, file))
        spec.loader.exec_module(importlib.util.module_from_spec(spec))