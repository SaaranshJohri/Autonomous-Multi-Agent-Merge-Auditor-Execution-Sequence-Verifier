from fastapi import FastAPI
from pydantic import BaseModel

from ast_parser import ASTParser


app = FastAPI(
    title="MergeMind Backend",
    description="Semantic Merge Conflict Detection System",
    version="0.1.0"
)


class CodeRequest(BaseModel):
    code: str


@app.get("/")
def home():
    return {
        "message": "MergeMind Backend is running"
    }


@app.post("/parse")
def parse_code(request: CodeRequest):

    try:
        parser = ASTParser(request.code)

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
            "message": e.msg
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }