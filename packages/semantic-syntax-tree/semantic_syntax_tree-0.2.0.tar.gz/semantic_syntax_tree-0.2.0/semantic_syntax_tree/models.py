import json
from typing import Literal, TypeAlias, TypedDict

from chromadb.api.types import Document, Metadata
from pydantic import BaseModel
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.pretty import Pretty
from rich.text import Text

NodeType: TypeAlias = Literal["class", "function"]
QualifiedName: TypeAlias = str

CODE_DEPENDENCIES_DIVIDER = "\n----- DEPENDENCIES -----\n"


class SstNodeMetadata(TypedDict):
    type: NodeType
    file: str
    sha1_hash: str


class SstNode(BaseModel):
    id: QualifiedName
    code: str
    dependencies: dict[str, QualifiedName]
    metadata: SstNodeMetadata

    @property
    def document(self) -> str:
        return f"{self.code}{CODE_DEPENDENCIES_DIVIDER}{json.dumps(self.dependencies, indent=2)}"

    @classmethod
    def from_db_values(
        cls, id: str, document: Document, metadata: Metadata
    ) -> "SstNode":
        """Create a PythonNode from the values stored in the vector database."""
        code, dependencies = document.split(CODE_DEPENDENCIES_DIVIDER)
        return cls(
            id=id,
            code=code,
            dependencies=json.loads(dependencies),
            metadata=metadata,  # type: ignore
        )

    def __rich__(self, title_extra: str = "") -> Panel:
        code_block = Panel(
            Text.from_markup(f"{self.code.strip()}"),
            title="Code",
            title_align="left",
            border_style="grey50",
        )
        deps_block = Panel(
            Pretty(self.dependencies),
            title="Dependencies",
            title_align="left",
            border_style="grey50",
        )
        return Panel(
            Columns([code_block, deps_block]),
            title=Text.from_markup(
                f"[bold][green]{self.id}[/green][/bold] {title_extra}"
            ),
            title_align="left",
            border_style="green",
            padding=(1, 2),
        )


class SstSearchResult(BaseModel):
    node: SstNode
    query: str
    distance: float

    def __rich__(self) -> Group:
        return Group(
            Text(f"Query: '{self.query}'", style="magenta"),
            self.node.__rich__(
                title_extra=f"[magenta](distance: {self.distance:.2f})[/magenta]"
            ),
        )
