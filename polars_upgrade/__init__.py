from __future__ import annotations
__version__ = "0.2.4"

from polars_upgrade._main import fix_plugins as rewrite
from polars_upgrade._main import Settings

__all__ = ['rewrite', 'Settings']
