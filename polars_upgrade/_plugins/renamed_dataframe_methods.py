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


RENAMINGS = {
    "groupby_dynamic": ((0, 19, 0), "group_by_dynamic"),
    "groupby_rolling": ((0, 19, 0), "rolling"),
}


@register(ast.Attribute)
def visit_Attribute(
    state: State,
    node: ast.Attribute,
    parent: ast.AST,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if node.attr in RENAMINGS:
        min_version, new_name = RENAMINGS[node.attr]
        if state.settings.target_version >= min_version:
            func = functools.partial(rename, name=node.attr, new=new_name)
            yield ast_to_offset(node), func
