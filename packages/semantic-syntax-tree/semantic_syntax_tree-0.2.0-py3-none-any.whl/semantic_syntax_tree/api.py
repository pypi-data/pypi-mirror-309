from fastapi import FastAPI
from pydantic import BaseModel
from typing import Generic, TypeVar
from pathlib import Path

from fastapi_cli.cli import main as fastapi_cli_main, app as fastapi_cli_app

# from fastapi.middleware.cors import CORSMiddleware
from semantic_syntax_tree.models import SstSearchResult
from semantic_syntax_tree.search import search

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    data: T


app = FastAPI(
    title="Semantic Syntax Tree API",
    description="API for interacting with the Semantic Syntax Tree.",
    version="0.1.0",
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


class SearchParams(BaseModel):
    query: str
    n: int = 10
    repo: str | None = None
    collection_name: str | None = None


@app.post("/search")
async def search_(body: SearchParams) -> StandardResponse[list[SstSearchResult]]:
    return StandardResponse(
        data=search(
            query=body.query,
            n=body.n,
            repo=Path(body.repo) if body.repo else None,
            collection_name=body.collection_name,
        )
    )


# uv run fastapi dev semantic_syntax_tree/api.py


# def main():
#     # fastapi_cli_main()
#     fastapi_cli_app()


# if __name__ == "__main__":
#     main()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host=")
