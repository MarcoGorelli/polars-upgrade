from __future__ import annotations

import ast
import functools
from typing import Iterable

from tokenize_rt import Offset
from tokenize_rt import Token

from polars_upgrade._ast_helpers import ast_to_offset
from polars_upgrade._data import register
from polars_upgrade._data import State
from polars_upgrade._data import TokenFunc


def myfunc(
    i: int,
    tokens: list[Token],
) -> None:
    tokens[i] = tokens[i]._replace(src=tokens[i].src.replace('mo_saturating', 'mo'))


@register(ast.Constant)
def visit_Constant(
        state: State,
        node: ast.Constant,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    if (
            isinstance(node.value, str) and node.value.endswith('mo_saturating') and
            isinstance(parent, (ast.Call, ast.keyword)) and
            state.settings.target_version >= (0, 19, 3)
    ):
        func = functools.partial(myfunc)
        yield ast_to_offset(node), func
