import ast


class ASTParser:
    def __init__(self, code: str, filename: str = "unknown.py"):
        self.code = code
        self.filename = filename
        self.tree = ast.parse(code)

    def parse(self):
        result = {
            "file": self.filename,
            "imports": [],
            "classes": [],
            "functions": [],
            "function_calls": [],
            "variables": [],
            "assignments": [],
            "conditions": [],
            "loops": [],
            "returns": []
        }

        # First collect all function names.
        # This helps us identify function-to-function calls later.
        function_names = {
            node.name
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        for node in ast.walk(self.tree):

            # -------------------------------------------------
            # IMPORTS
            # -------------------------------------------------

            if isinstance(node, ast.Import):

                for alias in node.names:
                    result["imports"].append({
                        "name": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno,
                        "end_line": getattr(
                            node, "end_lineno", node.lineno
                        )
                    })

            elif isinstance(node, ast.ImportFrom):

                for alias in node.names:
                    result["imports"].append({
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno,
                        "end_line": getattr(
                            node, "end_lineno", node.lineno
                        )
                    })

            # -------------------------------------------------
            # FUNCTIONS
            # -------------------------------------------------

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                arguments = []

                for arg in node.args.args:
                    arguments.append({
                        "name": arg.arg,
                        "annotation": self._get_annotation(arg.annotation)
                    })

                calls = []

                for child in ast.walk(node):

                    if isinstance(child, ast.Call):

                        called_name = self._get_call_name(child)

                        if called_name:
                            calls.append({
                                "name": called_name,
                                "line": child.lineno,
                                "is_internal": called_name in function_names
                            })

                result["functions"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": getattr(
                        node, "end_lineno", node.lineno
                    ),
                    "arguments": arguments,
                    "argument_count": len(arguments),
                    "is_async": isinstance(
                        node, ast.AsyncFunctionDef
                    ),
                    "calls": calls,
                    "returns": self._get_function_returns(node)
                })

            # -------------------------------------------------
            # CLASSES
            # -------------------------------------------------

            elif isinstance(node, ast.ClassDef):

                methods = []

                for child in node.body:

                    if isinstance(
                        child,
                        (ast.FunctionDef, ast.AsyncFunctionDef)
                    ):
                        methods.append({
                            "name": child.name,
                            "line": child.lineno,
                            "end_line": getattr(
                                child, "end_lineno", child.lineno
                            )
                        })

                result["classes"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": getattr(
                        node, "end_lineno", node.lineno
                    ),
                    "methods": methods
                })

            # -------------------------------------------------
            # FUNCTION CALLS
            # -------------------------------------------------

            elif isinstance(node, ast.Call):

                called_name = self._get_call_name(node)

                if called_name:

                    result["function_calls"].append({
                        "name": called_name,
                        "line": node.lineno,
                        "is_internal": called_name in function_names
                    })

            # -------------------------------------------------
            # VARIABLES
            # -------------------------------------------------

            elif isinstance(node, ast.Name):

                if isinstance(node.ctx, ast.Store):

                    result["variables"].append({
                        "name": node.id,
                        "line": node.lineno,
                        "context": "store"
                    })

            # -------------------------------------------------
            # ASSIGNMENTS
            # -------------------------------------------------

            elif isinstance(node, ast.Assign):

                targets = []

                for target in node.targets:

                    target_name = self._get_target_name(target)

                    if target_name:
                        targets.append(target_name)

                result["assignments"].append({
                    "targets": targets,
                    "line": node.lineno,
                    "end_line": getattr(
                        node, "end_lineno", node.lineno
                    )
                })

            # -------------------------------------------------
            # CONDITIONS
            # -------------------------------------------------

            elif isinstance(node, ast.If):

                result["conditions"].append({
                    "line": node.lineno,
                    "end_line": getattr(
                        node, "end_lineno", node.lineno
                    )
                })

            # -------------------------------------------------
            # LOOPS
            # -------------------------------------------------

            elif isinstance(node, (ast.For, ast.While)):

                result["loops"].append({
                    "type": "for"
                    if isinstance(node, ast.For)
                    else "while",
                    "line": node.lineno,
                    "end_line": getattr(
                        node, "end_lineno", node.lineno
                    )
                })

            # -------------------------------------------------
            # RETURNS
            # -------------------------------------------------

            elif isinstance(node, ast.Return):

                result["returns"].append({
                    "line": node.lineno,
                    "has_value": node.value is not None
                })

        return result

    # =========================================================
    # HELPER FUNCTIONS
    # =========================================================

    def _get_call_name(self, node):

        if not isinstance(node, ast.Call):
            return None

        # Example:
        # calculate_price()
        if isinstance(node.func, ast.Name):
            return node.func.id

        # Example:
        # user.login()
        if isinstance(node.func, ast.Attribute):

            parts = []

            current = node.func

            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value

            if isinstance(current, ast.Name):
                parts.append(current.id)

            return ".".join(reversed(parts))

        return None

    def _get_target_name(self, node):

        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):

            parts = []

            current = node

            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value

            if isinstance(current, ast.Name):
                parts.append(current.id)

            return ".".join(reversed(parts))

        if isinstance(node, (ast.Tuple, ast.List)):

            names = []

            for element in node.elts:
                name = self._get_target_name(element)

                if name:
                    names.append(name)

            return names

        return None

    def _get_annotation(self, annotation):

        if annotation is None:
            return None

        try:
            return ast.unparse(annotation)
        except Exception:
            return None

    def _get_function_returns(self, function_node):

        returns = []

        for node in ast.walk(function_node):

            if isinstance(node, ast.Return):

                returns.append({
                    "line": node.lineno,
                    "has_value": node.value is not None
                })

        return returns