from __future__ import annotations

import ast
import functools
from typing import TYPE_CHECKING

from polars_upgrade._ast_helpers import ast_to_offset
from polars_upgrade._data import register
from polars_upgrade._data import State
from polars_upgrade._data import TokenFunc

if TYPE_CHECKING:
    from typing import Iterable
    from typing import List
    from typing import Tuple

    from tokenize_rt import Offset
    from tokenize_rt import Token


def rename(
    i: int,
    tokens: List[Token],
    *,
    name: str,
    new: str,
) -> None:
    while not (tokens[i].name == "NAME" and tokens[i].src == name):
        i += 1
    tokens[i] = tokens[i]._replace(src=new)


def rename_and_add_argument(
    i: int,
    tokens: List[Token],
    *,
    name: str,
    new: str,
    argument: str,
) -> None:
    while not (tokens[i].name == "NAME" and tokens[i].src == name):
        i += 1
    tokens[i] = tokens[i]._replace(src=new)
    while not (tokens[i].name == "OP" and tokens[i].src == "("):
        i += 1
    tokens[i] = tokens[i]._replace(src=f"({argument}, ")


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    # If `name` was specified we can just rename, easy
    if (
        isinstance(node.func, ast.Attribute) and
        node.func.attr == "with_row_count" and
        (node.args or "name" in {kw.arg for kw in node.keywords}) and
        state.settings.target_version >= (0, 20, 4)
    ):
        func = functools.partial(rename, name=node.func.attr, new="with_row_index")
        yield ast_to_offset(node), func

    # If no `name` was specified, we set it to 'row_nr' to not break code
    if (
        isinstance(node.func, ast.Attribute) and
        node.func.attr == "with_row_count" and
        not node.args and
        "name" not in {kw.arg for kw in node.keywords} and
        state.settings.target_version >= (0, 20, 4)
    ):
        func = functools.partial(
            rename_and_add_argument,
            name=node.func.attr,
            new="with_row_index",
            argument='"row_nr"',
        )
        yield ast_to_offset(node), func
