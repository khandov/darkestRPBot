import ast
import os

def extract_command_names_from_register(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    command_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Str) and key.s == "name":
                    if isinstance(value, ast.Str):
                        command_names.append(value.s)
    return command_names

def extract_command_names_from_api(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    command_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr == 'hybrid_command':
                        for keyword in decorator.keywords:
                            if keyword.arg == 'name' and isinstance(keyword.value, ast.Str):
                                command_names.append(keyword.value.s)
    return command_names

def validate_commands(register_file, api_file):
    register_commands = extract_command_names_from_register(register_file)
    api_commands = extract_command_names_from_api(api_file)
    
    missing_in_api = set(register_commands) - set(api_commands)
    missing_in_register = set(api_commands) - set(register_commands)
    
    if missing_in_api:
        print(f"Commands missing in {api_file}: {missing_in_api}")
    if missing_in_register:
        print(f"Commands missing in {register_file}: {missing_in_register}")
    if not missing_in_api and not missing_in_register:
        print("All commands are properly registered.")

if __name__ == "__main__":
    register_file = os.path.join(os.path.dirname(__file__), 'registerCommands.py')
    api_file = os.path.join(os.path.dirname(__file__), 'api', 'commands.py')
    validate_commands(register_file, api_file)