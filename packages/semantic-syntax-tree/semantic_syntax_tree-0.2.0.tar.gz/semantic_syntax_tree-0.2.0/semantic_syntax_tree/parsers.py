from hashlib import sha1
from pathlib import Path
from typing import Any, TypeGuard

import libcst as cst
from libcst.helpers import calculate_module_and_package, get_full_name_for_node_or_raise
from libcst.metadata import (
    GlobalScope,
    MetadataWrapper,
    QualifiedNameSource,
    Scope,
    ScopeProvider,
)

from semantic_syntax_tree.models import SstNode, SstNodeMetadata


def parse_python_module(file: str | Path, repo: str | Path) -> list[SstNode]:
    """
    Split a Python module into separate nodes for top-level class and functions.
    Each node will contain the source code as well as a list of the dependencies.
    """
    file, repo = Path(file), Path(repo)
    text = file.read_text()
    if not text.strip():
        return []
    tree = MetadataWrapper(cst.parse_module(text))
    parser = _PythonModuleParser(tree.module, file, repo)
    tree.visit(parser)
    return parser.nodes


class _PythonModuleParser(cst.CSTVisitor):
    """
    Parse a module, collecting 'SstNode' instances for top-level classes and functions
    """

    METADATA_DEPENDENCIES = (ScopeProvider,)

    def __init__(self, module: cst.Module, file_path: Path, repo_path: Path):
        super().__init__()
        module_info = calculate_module_and_package(repo_path, file_path)
        self.module = module
        self.module_name = module_info.name
        self.package = module_info.package
        self.file = str(file_path.relative_to(repo_path))
        self.module_shal_hash = sha1(module.code.encode()).hexdigest()

        self.nodes: list[SstNode] = []
        # 'self._members' contains the names of all the top-level classes and functions
        self._members = set(
            node.name.value
            for node in self.module.body
            if isinstance(node, (cst.ClassDef, cst.FunctionDef))
        )

    def _get_qualified_name(self, node: cst.ClassDef | cst.FunctionDef) -> str:
        """Return the fully qualified name of the class/function."""
        return f"{self.module_name}.{get_full_name_for_node_or_raise(node)}"

    def _get_dependencies(self, node: cst.ClassDef | cst.FunctionDef) -> dict[str, str]:
        """Return all the names that are used in the class/function."""
        scope = self.get_metadata(ScopeProvider, node)

        if not isinstance(scope, Scope):
            raise ValueError(f"Expected a Scope, got {scope}")

        node_name = get_full_name_for_node_or_raise(node)

        dependencies: dict[str, str] = {}

        for name in _NameCollector.get_all_names(node):
            if name == node_name:
                continue
            for assignment in scope[name]:
                for qn in assignment.get_qualified_names_for(assignment.name):
                    match qn.source:
                        case QualifiedNameSource.IMPORT:
                            dependencies[assignment.name] = qn.name
                        case QualifiedNameSource.LOCAL:
                            if assignment.name in self._members:
                                dependencies[assignment.name] = (
                                    f"'{self.module_name}.{qn.name}"
                                )
                        case QualifiedNameSource.BUILTIN:
                            pass

        return dependencies

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        scope = self.get_metadata(ScopeProvider, node)
        if _is_global_scope(scope):
            code = self.module.code_for_node(node)
            self.nodes.append(
                SstNode(
                    id=self._get_qualified_name(node),
                    code=code,
                    dependencies=self._get_dependencies(node),
                    metadata=SstNodeMetadata(
                        type="class",
                        file=self.file,
                        sha1_hash=sha1(code.encode()).hexdigest(),
                    ),
                )
            )

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        scope = self.get_metadata(ScopeProvider, node)
        if _is_global_scope(scope):
            code = self.module.code_for_node(node)
            self.nodes.append(
                SstNode(
                    id=self._get_qualified_name(node),
                    code=code,
                    dependencies=self._get_dependencies(node),
                    metadata=SstNodeMetadata(
                        type="function",
                        file=self.file,
                        sha1_hash=sha1(code.encode()).hexdigest(),
                    ),
                )
            )


class _NameCollector(cst.CSTVisitor):
    @classmethod
    def get_all_names(cls, target: cst.CSTNode) -> set[str]:
        collector = cls()
        target.visit(collector)
        return collector.names

    def __init__(self):
        super().__init__()
        self.names: set[str] = set()

    def visit_Name(self, node: cst.Name) -> None:
        self.names.add(node.value)


def _is_global_scope(scope: Any) -> TypeGuard[GlobalScope]:
    return isinstance(scope, Scope) and scope is scope.globals
