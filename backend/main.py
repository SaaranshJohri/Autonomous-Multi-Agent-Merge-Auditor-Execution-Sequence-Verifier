from fastapi import FastAPI
from pydantic import BaseModel

from ast_parser import ASTParser


app = FastAPI(
    title="MergeMind Backend",
    description="Semantic Merge Conflict Detection System",
    version="0.2.0"
)


class CodeRequest(BaseModel):
    code: str
    filename: str = "unknown.py"


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

        return {
            "success": True,
            "ast_analysis": result
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