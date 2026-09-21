import ast
from pathlib import Path


# =========================================================
# LOAD SOURCE CODE
# =========================================================

def load_code(file_path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return path.read_text(
        encoding="utf-8"
    )


# =========================================================
# PARSE CODE
# =========================================================

def parse_code(code):

    return ast.parse(code)


# =========================================================
# EXTRACT FUNCTION CALLS
# =========================================================

def extract_function_calls(function_node):

    calls = set()

    for node in ast.walk(function_node):

        if isinstance(node, ast.Call):

            # Example:
            # calculate_tax(price)

            if isinstance(
                node.func,
                ast.Name
            ):

                calls.add(
                    node.func.id
                )

            # Example:
            # self.calculate_tax(price)

            elif isinstance(
                node.func,
                ast.Attribute
            ):

                calls.add(
                    node.func.attr
                )

    return sorted(calls)


# =========================================================
# EXTRACT FUNCTIONS
# =========================================================

def extract_functions(tree):

    functions = {}

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):

            functions[node.name] = {

                "name": node.name,

                "line": node.lineno,

                "end_line": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),

                "arguments": [
                    arg.arg
                    for arg in node.args.args
                ],

                "calls": extract_function_calls(
                    node
                ),

                "source": ast.unparse(
                    node
                )
            }

    return functions


# =========================================================
# EXTRACT CLASSES
# =========================================================

def extract_classes(tree):

    classes = {}

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.ClassDef
        ):

            classes[node.name] = {

                "name": node.name,

                "line": node.lineno,

                "end_line": getattr(
                    node,
                    "end_lineno",
                    node.lineno
                ),

                "bases": [
                    ast.unparse(base)
                    for base in node.bases
                ],

                "methods": [
                    child.name
                    for child in node.body
                    if isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef
                        )
                    )
                ],

                "source": ast.unparse(
                    node
                )
            }

    return classes


# =========================================================
# EXTRACT IMPORTS
# =========================================================

def extract_imports(tree):

    imports = []

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.Import
        ):

            for alias in node.names:

                imports.append(
                    alias.name
                )

        elif isinstance(
            node,
            ast.ImportFrom
        ):

            module = node.module or ""

            for alias in node.names:

                imports.append(
                    f"{module}.{alias.name}"
                )

    return sorted(
        set(imports)
    )


# =========================================================
# ANALYZE ONE VERSION
# =========================================================

def analyze_version(code):

    tree = parse_code(code)

    return {

        "functions":
            extract_functions(tree),

        "classes":
            extract_classes(tree),

        "imports":
            extract_imports(tree)
    }


# =========================================================
# COMPARE TWO DICTIONARIES
# =========================================================

def compare_entities(
    base_entities,
    branch_entities
):

    added = []
    removed = []
    modified = []

    base_names = set(
        base_entities.keys()
    )

    branch_names = set(
        branch_entities.keys()
    )


    # -----------------------------------------------------
    # ADDED
    # -----------------------------------------------------

    for name in (
        branch_names - base_names
    ):

        added.append(name)


    # -----------------------------------------------------
    # REMOVED
    # -----------------------------------------------------

    for name in (
        base_names - branch_names
    ):

        removed.append(name)


    # -----------------------------------------------------
    # MODIFIED
    # -----------------------------------------------------

    for name in (
        base_names & branch_names
    ):

        base_source = base_entities[
            name
        ].get(
            "source",
            ""
        )

        branch_source = branch_entities[
            name
        ].get(
            "source",
            ""
        )

        if base_source != branch_source:

            modified.append(name)


    return {

        "added":
            sorted(added),

        "removed":
            sorted(removed),

        "modified":
            sorted(modified)
    }


# =========================================================
# COMPARE BASE → BRANCH
# =========================================================

def compare_branch(
    base_analysis,
    branch_analysis
):

    return {

        "functions":
            compare_entities(
                base_analysis["functions"],
                branch_analysis["functions"]
            ),

        "classes":
            compare_entities(
                base_analysis["classes"],
                branch_analysis["classes"]
            ),

        "imports_added":
            sorted(
                set(
                    branch_analysis["imports"]
                )
                -
                set(
                    base_analysis["imports"]
                )
            ),

        "imports_removed":
            sorted(
                set(
                    base_analysis["imports"]
                )
                -
                set(
                    branch_analysis["imports"]
                )
            )
    }


# =========================================================
# DIRECT CONFLICT DETECTION
# =========================================================

def detect_direct_conflicts(
    base_analysis,
    branch_a_analysis,
    branch_b_analysis
):

    conflicts = []


    # =====================================================
    # FUNCTION CONFLICTS
    # =====================================================

    base_functions = (
        base_analysis["functions"]
    )

    a_functions = (
        branch_a_analysis["functions"]
    )

    b_functions = (
        branch_b_analysis["functions"]
    )


    common_functions = (

        set(base_functions.keys())

        & set(a_functions.keys())

        & set(b_functions.keys())
    )


    for name in common_functions:

        base_source = (
            base_functions[name]["source"]
        )

        a_source = (
            a_functions[name]["source"]
        )

        b_source = (
            b_functions[name]["source"]
        )


        changed_by_a = (
            a_source != base_source
        )

        changed_by_b = (
            b_source != base_source
        )


        if (
            changed_by_a
            and
            changed_by_b
            and
            a_source != b_source
        ):

            conflicts.append({

                "type":
                    "function_conflict",

                "severity":
                    "high",

                "entity":
                    name,

                "description":
                    (
                        f"Both developers modified "
                        f"function '{name}' differently."
                    ),

                "base":
                    base_source,

                "developer_a":
                    a_source,

                "developer_b":
                    b_source
            })


    # =====================================================
    # CLASS CONFLICTS
    # =====================================================

    base_classes = (
        base_analysis["classes"]
    )

    a_classes = (
        branch_a_analysis["classes"]
    )

    b_classes = (
        branch_b_analysis["classes"]
    )


    common_classes = (

        set(base_classes.keys())

        & set(a_classes.keys())

        & set(b_classes.keys())
    )


    for name in common_classes:

        base_source = (
            base_classes[name]["source"]
        )

        a_source = (
            a_classes[name]["source"]
        )

        b_source = (
            b_classes[name]["source"]
        )


        changed_by_a = (
            a_source != base_source
        )

        changed_by_b = (
            b_source != base_source
        )


        if (
            changed_by_a
            and
            changed_by_b
            and
            a_source != b_source
        ):

            conflicts.append({

                "type":
                    "class_conflict",

                "severity":
                    "high",

                "entity":
                    name,

                "description":
                    (
                        f"Both developers modified "
                        f"class '{name}' differently."
                    ),

                "base":
                    base_source,

                "developer_a":
                    a_source,

                "developer_b":
                    b_source
            })


    return conflicts


# =========================================================
# SEMANTIC DEPENDENCY CONFLICTS
# =========================================================

def detect_dependency_conflicts(
    base_analysis,
    branch_a_analysis,
    branch_b_analysis
):

    conflicts = []


    base_functions = (
        base_analysis["functions"]
    )

    a_functions = (
        branch_a_analysis["functions"]
    )

    b_functions = (
        branch_b_analysis["functions"]
    )


    # -----------------------------------------------------
    # WHAT DID A MODIFY?
    # -----------------------------------------------------

    a_modified = set(

        compare_entities(
            base_functions,
            a_functions
        )["modified"]

    )


    # -----------------------------------------------------
    # WHAT DID B MODIFY?
    # -----------------------------------------------------

    b_modified = set(

        compare_entities(
            base_functions,
            b_functions
        )["modified"]

    )


    # -----------------------------------------------------
    # A'S MODIFIED FUNCTIONS DEPEND ON B'S MODIFICATIONS
    # -----------------------------------------------------

    for function_a in a_modified:

        if function_a not in a_functions:
            continue

        calls = set(
            a_functions[
                function_a
            ].get(
                "calls",
                []
            )
        )


        for function_b in (
            b_modified
        ):

            if function_b in calls:

                conflicts.append({

                    "type":
                        "semantic_dependency_conflict",

                    "severity":
                        "medium",

                    "entity":
                        function_a,

                    "related_entity":
                        function_b,

                    "direction":
                        "A depends on B",

                    "description":
                        (
                            f"Developer A modified "
                            f"'{function_a}', which depends "
                            f"on '{function_b}', modified "
                            f"by Developer B."
                        ),

                    "base":
                        base_functions[
                            function_a
                        ]["source"],

                    "developer_a":
                        a_functions[
                            function_a
                        ]["source"],

                    "developer_b":
                        b_functions[
                            function_b
                        ]["source"]
                })


    # -----------------------------------------------------
    # B'S MODIFIED FUNCTIONS DEPEND ON A'S MODIFICATIONS
    # -----------------------------------------------------

    for function_b in b_modified:

        if function_b not in b_functions:
            continue

        calls = set(
            b_functions[
                function_b
            ].get(
                "calls",
                []
            )
        )


        for function_a in (
            a_modified
        ):

            if function_a in calls:

                conflicts.append({

                    "type":
                        "semantic_dependency_conflict",

                    "severity":
                        "medium",

                    "entity":
                        function_b,

                    "related_entity":
                        function_a,

                    "direction":
                        "B depends on A",

                    "description":
                        (
                            f"Developer B modified "
                            f"'{function_b}', which depends "
                            f"on '{function_a}', modified "
                            f"by Developer A."
                        ),

                    "base":
                        base_functions[
                            function_b
                        ]["source"],

                    "developer_a":
                        a_functions[
                            function_a
                        ]["source"],

                    "developer_b":
                        b_functions[
                            function_b
                        ]["source"]
                })


    return conflicts


# =========================================================
# COMPLETE CONFLICT DETECTION
# =========================================================

def detect_conflicts(
    base_analysis,
    branch_a_analysis,
    branch_b_analysis
):

    direct_conflicts = (
        detect_direct_conflicts(
            base_analysis,
            branch_a_analysis,
            branch_b_analysis
        )
    )


    semantic_conflicts = (
        detect_dependency_conflicts(
            base_analysis,
            branch_a_analysis,
            branch_b_analysis
        )
    )


    return (
        direct_conflicts
        +
        semantic_conflicts
    )


# =========================================================
# ANALYZE MERGE FROM CODE
# =========================================================

def analyze_merge_from_code(
    base_code,
    developer_a_code,
    developer_b_code
):

    # -----------------------------------------------------
    # ANALYZE THREE VERSIONS
    # -----------------------------------------------------

    base_analysis = analyze_version(
        base_code
    )

    developer_a_analysis = analyze_version(
        developer_a_code
    )

    developer_b_analysis = analyze_version(
        developer_b_code
    )


    # -----------------------------------------------------
    # CHANGES
    # -----------------------------------------------------

    developer_a_changes = (
        compare_branch(
            base_analysis,
            developer_a_analysis
        )
    )

    developer_b_changes = (
        compare_branch(
            base_analysis,
            developer_b_analysis
        )
    )


    # -----------------------------------------------------
    # CONFLICTS
    # -----------------------------------------------------

    conflicts = detect_conflicts(
        base_analysis,
        developer_a_analysis,
        developer_b_analysis
    )


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    return {

        "base":
            base_analysis,

        "developer_a": {

            "analysis":
                developer_a_analysis,

            "changes":
                developer_a_changes
        },

        "developer_b": {

            "analysis":
                developer_b_analysis,

            "changes":
                developer_b_changes
        },

        "conflicts":
            conflicts,

        "summary": {

            "conflict_count":
                len(conflicts),

            "direct_conflicts":
                len([
                    c
                    for c in conflicts
                    if c["type"]
                    != "semantic_dependency_conflict"
                ]),

            "semantic_conflicts":
                len([
                    c
                    for c in conflicts
                    if c["type"]
                    == "semantic_dependency_conflict"
                ]),

            "status":
                (
                    "conflicts_detected"
                    if conflicts
                    else "no_conflicts"
                )
        }
    }


# =========================================================
# FILE-BASED ANALYSIS
# =========================================================

def analyze_merge(
    base_path,
    developer_a_path,
    developer_b_path
):

    base_code = load_code(
        base_path
    )

    developer_a_code = load_code(
        developer_a_path
    )

    developer_b_code = load_code(
        developer_b_path
    )


    return analyze_merge_from_code(
        base_code,
        developer_a_code,
        developer_b_code
    )


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    result = analyze_merge(

        "../sample_repos/base/test.py",

        "../sample_repos/developer_a/test.py",

        "../sample_repos/developer_b/test.py"
    )


    print(
        "\n=============================="
    )

    print(
        "MERGEMIND MERGE ANALYSIS"
    )

    print(
        "=============================="
    )


    print(
        "\nConflicts:",
        result[
            "summary"
        ][
            "conflict_count"
        ]
    )


    print(
        "Direct conflicts:",
        result[
            "summary"
        ][
            "direct_conflicts"
        ]
    )


    print(
        "Semantic conflicts:",
        result[
            "summary"
        ][
            "semantic_conflicts"
        ]
    )


    print(
        "Status:",
        result[
            "summary"
        ][
            "status"
        ]
    )


    print(
        "\nDetected conflicts:"
    )


    for conflict in (
        result["conflicts"]
    ):

        print(
            f"\n  🔴 {conflict['entity']}"
        )

        print(
            f"     Type: "
            f"{conflict['type']}"
        )

        print(
            f"     {conflict['description']}"
        )

        if "related_entity" in conflict:

            print(
                f"     Related: "
                f"{conflict['related_entity']}"
            )