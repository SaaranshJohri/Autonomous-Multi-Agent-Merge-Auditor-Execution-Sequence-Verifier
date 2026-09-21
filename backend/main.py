from fastapi import FastAPI
from pydantic import BaseModel
from dependency_graph import DependencyGraph

from ast_parser import ASTParser
from merge_analyzer import analyze_merge_from_code

app = FastAPI(
    title="MergeMind Backend",
    description="Semantic Merge Conflict Detection System",
    version="0.2.0"
)


class CodeRequest(BaseModel):
    code: str
    filename: str = "unknown.py"

class MergeRequest(BaseModel):
    base_code: str
    developer_a_code: str
    developer_b_code: str

    base_filename: str = "base.py"
    developer_a_filename: str = "developer_a.py"
    developer_b_filename: str = "developer_b.py"

@app.get("/")
def home():

    return {
        "message": "MergeMind Backend is running",
        "version": "0.2.0"
    }


@app.post("/parse")
def parse_code(request: CodeRequest):

    try:

        parser = ASTParser(
            code=request.code,
            filename=request.filename
        )

        result = parser.parse()

        dependency_graph = DependencyGraph(
            result
        )

        graph = dependency_graph.build()

        graph_data = dependency_graph.get_graph_data()

        return {
            "success": True,
            "ast_analysis": result,
            "dependency_graph": graph_data
        }

    except SyntaxError as e:

        return {
            "success": False,
            "error": "Invalid Python syntax",
            "line": e.lineno,
            "column": e.offset,
            "message": e.msg
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

@app.post("/merge")
def merge_code(request: MergeRequest):

    try:

        result = analyze_merge_from_code(
            request.base_code,
            request.developer_a_code,
            request.developer_b_code
        )

        return {
            "success": True,
            "merge_analysis": result
        }

    except SyntaxError as e:

        return {
            "success": False,
            "error": "Invalid Python syntax",
            "line": e.lineno,
            "column": e.offset,
            "message": e.msg
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }