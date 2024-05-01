from __future__ import annotations

import ast
import functools
from typing import TYPE_CHECKING

from polars_upgrade._ast_helpers import ast_to_offset
from polars_upgrade._data import register
from polars_upgrade._data import State
from polars_upgrade._data import TokenFunc
from polars_upgrade._token_helpers import is_simple_expression

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
    new_name: str,
) -> None:
    while not (tokens[i].name == "NAME" and tokens[i].src == name):
        i += 1
    tokens[i] = tokens[i]._replace(src=new_name)


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if (
        state.settings.target_version >= (0, 19, 13) and
        isinstance(node.value, ast.Attribute) and
        is_simple_expression(node.value.value, state.aliases["polars"]) and
        node.value.attr == "dt" and
        node.attr
        in (
            "nanoseconds",
            "microseconds",
            "milliseconds",
            "seconds",
            "minutes",
            "hours",
            "days",
            "weeks",
        )
    ):
        new_attr = f"total_{node.attr}"
        func = functools.partial(
            rename,
            name=node.attr,
            new_name=new_attr,
        )
        yield ast_to_offset(node), func
