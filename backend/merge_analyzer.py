import ast
from pathlib import Path


def load_code(file_path):
    """Load a UTF-8 source file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path.read_text(encoding="utf-8")


def parse_code(code):
    """Parse Python source, allowing an empty/missing file."""
    return ast.parse(code or "")


def _source(node):
    """Return normalized source for an AST node."""
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def extract_function_calls(function_node):
    calls = set()
    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
    return sorted(calls)


def extract_functions(tree):
    """Extract functions using qualified names to reduce name collisions."""
    functions = {}

    def visit(node, prefix=""):
        for child in getattr(node, "body", []):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = f"{prefix}.{child.name}" if prefix else child.name
                functions[name] = {
                    "name": child.name,
                    "qualified_name": name,
                    "line": child.lineno,
                    "end_line": getattr(child, "end_lineno", child.lineno),
                    "arguments": [arg.arg for arg in child.args.args],
                    "calls": extract_function_calls(child),
                    "source": _source(child),
                }
                visit(child, name)
            elif isinstance(child, ast.ClassDef):
                class_prefix = f"{prefix}.{child.name}" if prefix else child.name
                visit(child, class_prefix)

    visit(tree)
    return functions


def extract_classes(tree):
    classes = {}

    def visit(node, prefix=""):
        for child in getattr(node, "body", []):
            if isinstance(child, ast.ClassDef):
                name = f"{prefix}.{child.name}" if prefix else child.name
                classes[name] = {
                    "name": child.name,
                    "qualified_name": name,
                    "line": child.lineno,
                    "end_line": getattr(child, "end_lineno", child.lineno),
                    "bases": [_source(base) for base in child.bases],
                    "methods": [
                        method.name
                        for method in child.body
                        if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
                    ],
                    "source": _source(child),
                }
                visit(child, name)

    visit(tree)
    return classes


def _target_names(target):
    """Yield names assigned by a module-level assignment target."""
    if isinstance(target, ast.Name):
        yield target.id
    elif isinstance(target, (ast.Tuple, ast.List)):
        for element in target.elts:
            yield from _target_names(element)


def extract_module_variables(tree):
    """
    Extract assignments directly in module scope.
    Assignments inside functions/classes are deliberately excluded.
    """
    variables = {}
    for node in tree.body:
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            targets = [node.target]
        else:
            # Function/class bodies are analyzed separately.
            continue

        assignment_source = _source(node)
        annotation = (
            _source(node.annotation)
            if isinstance(node, ast.AnnAssign) and node.annotation
            else None
        )

        for target in targets:
            for name in _target_names(target):
                variables[name] = {
                    "name": name,
                    "line": getattr(node, "lineno", 0),
                    "source": assignment_source,
                    "annotation": annotation,
                }
    return variables


def extract_imports(tree):
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.extend(f"{module}.{alias.name}" for alias in node.names)
    return sorted(set(imports))


def analyze_version(code):
    tree = parse_code(code)
    return {
        "functions": extract_functions(tree),
        "classes": extract_classes(tree),
        "variables": extract_module_variables(tree),
        "imports": extract_imports(tree),
    }


def compare_entities(base_entities, branch_entities):
    base_names = set(base_entities)
    branch_names = set(branch_entities)
    added = sorted(branch_names - base_names)
    removed = sorted(base_names - branch_names)
    modified = sorted(
        name
        for name in base_names & branch_names
        if base_entities[name].get("source", "")
        != branch_entities[name].get("source", "")
    )
    return {"added": added, "removed": removed, "modified": modified}


def compare_branch(base_analysis, branch_analysis):
    return {
        "functions": compare_entities(
            base_analysis["functions"], branch_analysis["functions"]
        ),
        "classes": compare_entities(
            base_analysis["classes"], branch_analysis["classes"]
        ),
        "variables": compare_entities(
            base_analysis["variables"], branch_analysis["variables"]
        ),
        "imports_added": sorted(
            set(branch_analysis["imports"]) - set(base_analysis["imports"])
        ),
        "imports_removed": sorted(
            set(base_analysis["imports"]) - set(branch_analysis["imports"])
        ),
    }


def _make_conflict(conflict_type, severity, entity, description, base, a, b, **extra):
    result = {
        "type": conflict_type,
        "severity": severity,
        "entity": entity,
        "description": description,
        "base": base,
        "developer_a": a,
        "developer_b": b,
    }
    result.update(extra)
    return result


def _detect_entity_conflicts(
    entity_type, label, base_entities, a_entities, b_entities
):
    conflicts = []

    # Both branches modify an entity that existed in the common ancestor.
    common = set(base_entities) & set(a_entities) & set(b_entities)
    for name in sorted(common):
        base_source = base_entities[name].get("source", "")
        a_source = a_entities[name].get("source", "")
        b_source = b_entities[name].get("source", "")
        if (
            a_source != base_source
            and b_source != base_source
            and a_source != b_source
        ):
            conflicts.append(
                _make_conflict(
                    f"{entity_type}_conflict",
                    "high",
                    name,
                    f"Both developers modified {label} '{name}' differently.",
                    base_source,
                    a_source,
                    b_source,
                )
            )

    # Both branches independently add the same entity name with different content.
    added_by_both = (set(a_entities) & set(b_entities)) - set(base_entities)
    for name in sorted(added_by_both):
        a_source = a_entities[name].get("source", "")
        b_source = b_entities[name].get("source", "")
        if a_source != b_source:
            conflicts.append(
                _make_conflict(
                    f"{entity_type}_conflict",
                    "high",
                    name,
                    f"Both developers added {label} '{name}' differently.",
                    "<not present in base>",
                    a_source,
                    b_source,
                )
            )
    return conflicts


def detect_direct_conflicts(base_analysis, branch_a_analysis, branch_b_analysis):
    conflicts = []
    conflicts.extend(
        _detect_entity_conflicts(
            "function",
            "function",
            base_analysis["functions"],
            branch_a_analysis["functions"],
            branch_b_analysis["functions"],
        )
    )
    conflicts.extend(
        _detect_entity_conflicts(
            "class",
            "class",
            base_analysis["classes"],
            branch_a_analysis["classes"],
            branch_b_analysis["classes"],
        )
    )
    conflicts.extend(
        _detect_entity_conflicts(
            "variable",
            "module-level variable",
            base_analysis["variables"],
            branch_a_analysis["variables"],
            branch_b_analysis["variables"],
        )
    )
    return conflicts


def detect_dependency_conflicts(base_analysis, branch_a_analysis, branch_b_analysis):
    conflicts = []
    base_functions = base_analysis["functions"]
    a_functions = branch_a_analysis["functions"]
    b_functions = branch_b_analysis["functions"]

    a_modified = set(compare_entities(base_functions, a_functions)["modified"])
    b_modified = set(compare_entities(base_functions, b_functions)["modified"])

    for function_a in sorted(a_modified):
        if function_a not in a_functions or function_a not in base_functions:
            continue
        calls = set(a_functions[function_a].get("calls", []))
        for function_b in sorted(b_modified):
            if (
                function_b in calls
                and function_b in b_functions
                and function_b in base_functions
            ):
                conflicts.append(
                    _make_conflict(
                        "semantic_dependency_conflict",
                        "medium",
                        function_a,
                        f"Developer A modified '{function_a}', which depends on "
                        f"'{function_b}', modified by Developer B.",
                        base_functions[function_a]["source"],
                        a_functions[function_a]["source"],
                        b_functions[function_b]["source"],
                        related_entity=function_b,
                        direction="A depends on B",
                    )
                )

    for function_b in sorted(b_modified):
        if function_b not in b_functions or function_b not in base_functions:
            continue
        calls = set(b_functions[function_b].get("calls", []))
        for function_a in sorted(a_modified):
            if (
                function_a in calls
                and function_a in a_functions
                and function_a in base_functions
            ):
                conflicts.append(
                    _make_conflict(
                        "semantic_dependency_conflict",
                        "medium",
                        function_b,
                        f"Developer B modified '{function_b}', which depends on "
                        f"'{function_a}', modified by Developer A.",
                        base_functions[function_b]["source"],
                        a_functions[function_a]["source"],
                        b_functions[function_b]["source"],
                        related_entity=function_a,
                        direction="B depends on A",
                    )
                )
    return conflicts


def detect_conflicts(base_analysis, branch_a_analysis, branch_b_analysis):
    direct = detect_direct_conflicts(
        base_analysis, branch_a_analysis, branch_b_analysis
    )
    semantic = detect_dependency_conflicts(
        base_analysis, branch_a_analysis, branch_b_analysis
    )

    # Remove duplicate dependency records while preserving order.
    seen = set()
    unique_semantic = []
    for conflict in semantic:
        key = (
            conflict.get("type"),
            conflict.get("entity"),
            conflict.get("related_entity"),
            conflict.get("direction"),
        )
        if key not in seen:
            seen.add(key)
            unique_semantic.append(conflict)
    return direct + unique_semantic


def analyze_merge_from_code(base_code, developer_a_code, developer_b_code):
    base_analysis = analyze_version(base_code)
    developer_a_analysis = analyze_version(developer_a_code)
    developer_b_analysis = analyze_version(developer_b_code)

    developer_a_changes = compare_branch(base_analysis, developer_a_analysis)
    developer_b_changes = compare_branch(base_analysis, developer_b_analysis)
    conflicts = detect_conflicts(
        base_analysis, developer_a_analysis, developer_b_analysis
    )

    return {
        "base": base_analysis,
        "developer_a": {
            "analysis": developer_a_analysis,
            "changes": developer_a_changes,
        },
        "developer_b": {
            "analysis": developer_b_analysis,
            "changes": developer_b_changes,
        },
        "conflicts": conflicts,
        "summary": {
            "conflict_count": len(conflicts),
            "direct_conflicts": sum(
                conflict["type"] != "semantic_dependency_conflict"
                for conflict in conflicts
            ),
            "semantic_conflicts": sum(
                conflict["type"] == "semantic_dependency_conflict"
                for conflict in conflicts
            ),
            "status": "conflicts_detected" if conflicts else "no_conflicts",
        },
    }


def analyze_merge(base_path, developer_a_path, developer_b_path):
    return analyze_merge_from_code(
        load_code(base_path),
        load_code(developer_a_path),
        load_code(developer_b_path),
    )


if __name__ == "__main__":
    result = analyze_merge(
        "../sample_repos/base/test.py",
        "../sample_repos/developer_a/test.py",
        "../sample_repos/developer_b/test.py",
    )
    print("MERGEMIND MERGE ANALYSIS")
    print("Conflicts:", result["summary"]["conflict_count"])
    print("Direct conflicts:", result["summary"]["direct_conflicts"])
    print("Semantic conflicts:", result["summary"]["semantic_conflicts"])
    print("Status:", result["summary"]["status"])
    for conflict in result["conflicts"]:
        print(f"\n[!] {conflict['entity']}")
        print(f"    Type: {conflict['type']}")
        print(f"    {conflict['description']}")
