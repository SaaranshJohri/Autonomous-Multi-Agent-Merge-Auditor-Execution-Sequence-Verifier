"""Public, framework-independent API for MergeMind."""

from .ast_parser import ASTParser
from .dependency_graph import DependencyGraph
from .merge_analyzer import analyze_merge_from_code


def analyze_code(code: str, filename: str = "unknown.py") -> dict:
    """Parse Python source and return AST details plus dependency graph data."""
    parser = ASTParser(code=code, filename=filename)
    analysis = parser.parse()
    graph = DependencyGraph(analysis)
    graph.build()
    return {
        "ast_analysis": analysis,
        "dependency_graph": graph.get_graph_data(),
    }


def analyze_file(file_path: str) -> dict:
    """Analyze a Python source file and return the analysis results."""
    with open(file_path, "r") as f:
        code = f.read()
    return analyze_code(code, filename=file_path)


def analyze_merge_files(base_file: str, a_file: str, b_file: str) -> dict:
    """Analyze three versions of a Python file and return the merge analysis results."""
    with open(base_file, "r") as f:
        base_code = f.read()
    with open(a_file, "r") as f:
        a_code = f.read()
    with open(b_file, "r") as f:
        b_code = f.read()
    return analyze_merge_from_code(base_code, a_code, b_code)


__all__ = ["analyze_code", "analyze_merge_from_code"]
