from __future__ import annotations

__version__ = "0.3.2"

from polars_upgrade._main import Settings
from polars_upgrade._main import fix_plugins as rewrite

__all__ = ["rewrite", "Settings"]
