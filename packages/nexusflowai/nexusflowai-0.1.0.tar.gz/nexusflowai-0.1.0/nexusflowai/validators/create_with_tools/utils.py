from typing import Any, List, Tuple, Optional, Union

from ast import AST, parse as ast_parse
from ast import Call, Import, ImportFrom, NodeVisitor, Name

ALLOWED_ROLES = [
    "system",
    "tool",
    "user",
    "assistant",
]

ALLOWED_IMPORTS = [
    "typing",
    "itertools",
    "collections",
    "tabulate",
    "dataclasses",
    "requests",
]
DISALLOWED_FUNCTIONS = ["eval", "exec", "setattr", "locals", "globals"]


class SecurityVisitor(NodeVisitor):
    def visit_Call(self, node: Call):
        if isinstance(node.func, Name):
            func_name = node.func.id
            if func_name in DISALLOWED_FUNCTIONS:
                raise ValueError(
                    f"Found dangerous call to {func_name} at line {node.lineno}. Disallowed functions: {DISALLOWED_FUNCTIONS}"
                )

        self.generic_visit(node)

    def visit_Import(self, node: Import) -> Any:
        import_names = [a.name for a in node.names]
        self.check_imports(node, import_names)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ImportFrom) -> Any:
        import_names = [node.module]
        self.check_imports(node, import_names)

        self.generic_visit(node)

    def check_imports(
        self, node: Union[Import, ImportFrom], import_names: List[str]
    ) -> None:
        disallowed_import_names = [n for n in import_names if n not in ALLOWED_IMPORTS]
        if disallowed_import_names:
            raise ImportError(
                f"Not allowed to import {disallowed_import_names} at line {node.lineno}. Allowed imports include {ALLOWED_IMPORTS}"
            )


class CodeExecutionHelper:
    def clean_input(self, source: str) -> Tuple[str, Optional[AST]]:
        source = source.strip()
        if len(source) == 0:
            return source, None

        tree = ast_parse(source)
        return source, tree

    def check_security(self, tree: AST) -> None:
        security_visitor = SecurityVisitor()
        try:
            security_visitor.visit(tree)
        except ValueError as e:
            raise TypeError from e
