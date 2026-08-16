import ast


class ASTParser:
    def __init__(self, code: str):
        self.code = code
        self.tree = ast.parse(code)

    def parse(self):
        result = {
            "imports": [],
            "functions": [],
            "classes": [],
            "function_calls": [],
            "variables": []
        }

        for node in ast.walk(self.tree):

            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for alias in node.names:
                    result["imports"].append(
                        f"{module}.{alias.name}"
                    )

            # Functions
            elif isinstance(node, ast.FunctionDef):
                result["functions"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "arguments": [
                        arg.arg for arg in node.args.args
                    ]
                })

            # Classes
            elif isinstance(node, ast.ClassDef):
                result["classes"].append({
                    "name": node.name,
                    "line": node.lineno
                })

            # Function calls
            elif isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):
                    result["function_calls"].append({
                        "name": node.func.id,
                        "line": node.lineno
                    })

                elif isinstance(node.func, ast.Attribute):
                    result["function_calls"].append({
                        "name": node.func.attr,
                        "line": node.lineno
                    })

            # Variables
            elif isinstance(node, ast.Assign):
                for target in node.targets:

                    if isinstance(target, ast.Name):
                        result["variables"].append({
                            "name": target.id,
                            "line": node.lineno
                        })

        return result