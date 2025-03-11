import re
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from ._bar_chart_race import bar_chart_race as bcr
from ._bar_chart_race_plotly import bar_chart_race_plotly as bcrp
from ._line_chart_race import line_chart_race as lcr
from ._utils import prepare_wide_data as pwd, prepare_long_data as pld


@pd.api.extensions.register_dataframe_accessor("bcr")
class _BCR:
    """
    Pandas DataFrame accessor for bar_chart_racer functionality.
    Allows direct method calls on DataFrame objects using the .bcr accessor.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize the accessor with a DataFrame.
        
        Parameters
        ----------
        df : pd.DataFrame
            The pandas DataFrame to operate on
        """
        self._df = df

    def bar_chart_race(
        self,
        filename: Optional[str] = None,
        orientation: Literal['h', 'v'] = 'h',
        sort: Literal['desc', 'asc'] = 'desc',
        n_bars: Optional[int] = None,
        fixed_order: bool = False,
        fixed_max: bool = False,
        steps_per_period: int = 10,
        period_length: int = 500,
        end_period_pause: int = 0,
        interpolate_period: bool = False,
        period_label: Union[bool, Dict[str, Any]] = True,
        period_template: Optional[str] = None,
        period_summary_func: Optional[Callable] = None,
        perpendicular_bar_func: Optional[Union[str, Callable]] = None,
        colors: Optional[Union[str, List, Dict]] = None,
        title: Optional[str] = None,
        bar_size: float = .95,
        bar_textposition: str = 'outside',
        bar_texttemplate: str = '{x:,.0f}',
        bar_label_font: Optional[Union[int, Dict[str, Any]]] = None,
        tick_label_font: Optional[Union[int, Dict[str, Any]]] = None,
        tick_template: str = '{x:,.0f}',
        shared_fontdict: Optional[Dict[str, Any]] = None,
        scale: str = 'linear',
        fig: Optional[plt.Figure] = None,
        writer: Optional[Any] = None,
        bar_kwargs: Optional[Dict[str, Any]] = None,
        fig_kwargs: Optional[Dict[str, Any]] = None,
        filter_column_colors: bool = False
    ) -> Union[str, None]:
        """
        Create an animated bar chart race using matplotlib.
        """
        return bcr(
            self._df, filename, orientation, sort, n_bars, fixed_order, fixed_max,
            steps_per_period, period_length, end_period_pause, interpolate_period,
            period_label, period_template, period_summary_func, perpendicular_bar_func,
            colors, title, bar_size, bar_textposition, bar_texttemplate,
            bar_label_font, tick_label_font, tick_template, shared_fontdict, scale,
            fig, writer, bar_kwargs, fig_kwargs, filter_column_colors
        )

    def bar_chart_race_plotly(
        self,
        filename: Optional[str] = None,
        orientation: Literal['h', 'v'] = 'h',
        sort: Literal['desc', 'asc'] = 'desc',
        n_bars: Optional[int] = None,
        fixed_order: bool = False,
        fixed_max: bool = False,
        steps_per_period: int = 10,
        period_length: int = 500,
        end_period_pause: int = 0,
        interpolate_period: bool = False,
        period_label: Union[bool, Dict[str, Any]] = True,
        period_template: Optional[str] = None,
        period_summary_func: Optional[Callable] = None,
        perpendicular_bar_func: Optional[Union[str, Callable]] = None,
        colors: Optional[Union[str, List, Dict]] = None,
        title: Optional[str] = None,
        bar_size: float = .95,
        bar_textposition: str = 'outside',
        bar_texttemplate: Optional[str] = None,
        bar_label_font: Optional[Union[int, Dict[str, Any]]] = None,
        tick_label_font: Optional[Union[int, Dict[str, Any]]] = None,
        hovertemplate: Optional[str] = None,
        slider: bool = True,
        scale: str = 'linear',
        bar_kwargs: Optional[Dict[str, Any]] = None,
        layout_kwargs: Optional[Dict[str, Any]] = None,
        write_html_kwargs: Optional[Dict[str, Any]] = None,
        filter_column_colors: bool = False
    ) -> Any:
        """
        Create an animated bar chart race using plotly.
        """
        return bcrp(
            self._df, filename, orientation, sort, n_bars, fixed_order, fixed_max,
            steps_per_period, period_length, end_period_pause, interpolate_period,
            period_label, period_template, period_summary_func, perpendicular_bar_func,
            colors, title, bar_size, bar_textposition, bar_texttemplate, bar_label_font,
            tick_label_font, hovertemplate, slider, scale, bar_kwargs, layout_kwargs,
            write_html_kwargs, filter_column_colors
        )

    def line_chart_race(
        self,
        filename: Optional[str] = None,
        n_lines: Optional[int] = None,
        steps_per_period: int = 10,
        period_length: int = 500,
        end_period_pause: int = 0,
        period_summary_func: Optional[Callable] = None,
        line_width_data: Optional[pd.DataFrame] = None,
        agg_line_func: Optional[Callable] = None,
        agg_line_kwargs: Optional[Dict[str, Any]] = None,
        others_line_func: Optional[Callable] = None,
        others_line_kwargs: Optional[Dict[str, Any]] = None,
        fade: float = 1,
        min_fade: float = .3,
        images: Optional[Dict[str, np.ndarray]] = None,
        colors: Optional[Union[str, List, Dict]] = None,
        title: Optional[str] = None,
        line_label_font: Optional[Union[int, Dict[str, Any]]] = None,
        tick_label_font: Optional[Union[int, Dict[str, Any]]] = None,
        tick_template: str = '{x:,.0f}',
        shared_fontdict: Optional[Dict[str, Any]] = None,
        scale: str = 'linear',
        fig: Optional[plt.Figure] = None,
        writer: Optional[Any] = None,
        line_kwargs: Optional[Dict[str, Any]] = None,
        fig_kwargs: Optional[Dict[str, Any]] = None
    ) -> Union[str, None]:
        """
        Create an animated line chart race using matplotlib.
        """
        return lcr(
            self._df, filename, n_lines, steps_per_period, period_length, end_period_pause,
            period_summary_func, line_width_data, agg_line_func, agg_line_kwargs,
            others_line_func, others_line_kwargs, fade, min_fade, images, colors,
            title, line_label_font, tick_label_font, tick_template, shared_fontdict,
            scale, fig, writer, line_kwargs, fig_kwargs
        )

    def prepare_wide_data(
        self,
        orientation: Literal['h', 'v'] = 'h',
        sort: Literal['desc', 'asc'] = 'desc',
        n_bars: Optional[int] = None,
        interpolate_period: bool = False,
        steps_per_period: int = 10,
        compute_ranks: bool = True
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Prepare wide data for bar chart animation.
        """
        return pwd(
            self._df,
            orientation=orientation,
            sort=sort,
            n_bars=n_bars,
            interpolate_period=interpolate_period,
            steps_per_period=steps_per_period,
            compute_ranks=compute_ranks
        )

    def prepare_long_data(
        self,
        index: str,
        columns: str,
        values: str,
        aggfunc: Union[str, Callable] = 'sum',
        orientation: Literal['h', 'v'] = 'h',
        sort: Literal['desc', 'asc'] = 'desc',
        n_bars: Optional[int] = None,
        interpolate_period: bool = False,
        steps_per_period: int = 10,
        compute_ranks: bool = True
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Prepare long data for bar chart animation.
        """
        return pld(
            self._df,
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            orientation=orientation,
            sort=sort,
            n_bars=n_bars,
            interpolate_period=interpolate_period,
            steps_per_period=steps_per_period,
            compute_ranks=compute_ranks
        )


# Update docstrings by removing the df parameter description
for method_name, func in [
    ('bar_chart_race', bcr),
    ('bar_chart_race_plotly', bcrp),
    ('line_chart_race', lcr),
    ('prepare_wide_data', pwd),
    ('prepare_long_data', pld)
]:
    if hasattr(_BCR, method_name) and func.__doc__:
        # Remove the df parameter description from the docstring
        doc = re.sub(r'df\s*:.*?(?=\n\s+\w+\s*:|\Z)', '', func.__doc__, flags=re.S)
        # Set the updated docstring
        getattr(_BCR, method_name).__doc__ = doc