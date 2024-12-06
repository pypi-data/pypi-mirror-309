# expression_lib/__init__.py
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from polars.plugins import register_plugin_function
from polars._typing import IntoExpr

PLUGIN_PATH = Path(__file__).parent


def match_intervals(values: IntoExpr, intervals: pl.Series) -> pl.Expr:
    """Match values to intervals."""
    intervals = ";".join(intervals.to_list())
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="match_intervals",
        args=values,
        kwargs={"intervals": intervals},
        is_elementwise=True,
    )
