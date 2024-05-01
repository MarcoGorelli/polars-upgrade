from __future__ import annotations

import ast
import functools
from typing import TYPE_CHECKING

from polars_upgrade._ast_helpers import ast_to_offset
from polars_upgrade._data import register
from polars_upgrade._data import State
from polars_upgrade._data import TokenFunc
from polars_upgrade._token_helpers import replace_name

if TYPE_CHECKING:
    from typing import Iterable
    from typing import Tuple

    from tokenize_rt import Offset

RENAMINGS = {
    "count": ((0, 20, 4), "len"),
}


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if (
        isinstance(node.func, ast.Attribute) and
        isinstance(node.func.value, ast.Name) and
        node.func.value.id in state.aliases["polars"] and
        node.func.attr in RENAMINGS and
        not node.args and
        not node.keywords
    ):
        min_version, new_name = RENAMINGS[node.func.attr]
        if state.settings.target_version >= min_version:
            new_attr = f"{node.func.value.id}.{new_name}"
            func = functools.partial(
                replace_name,
                name=node.func.attr,
                new=new_attr,
            )
            yield ast_to_offset(node), func
