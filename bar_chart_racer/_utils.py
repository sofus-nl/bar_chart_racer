from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, Union, Any, Callable

import pandas as pd
import numpy as np
from matplotlib import image as mimage


def load_dataset(name: str = 'covid19') -> pd.DataFrame:
    '''
    Return a pandas DataFrame suitable for immediate use in `bar_chart_race`.
    Must be connected to the internet

    Parameters
    ----------
    name : str, default 'covid19'
        Name of dataset to load from the bar_chart_racer github repository.
        Choices include:
        * 'covid19'
        * 'covid19_tutorial'
        * 'urban_pop'
        * 'baseball'

    Returns
    -------
    pd.DataFrame
        DataFrame ready for use with bar_chart_race functions
    
    Raises
    ------
    ValueError
        If the dataset name is not recognized
    '''
    # TODO: Update this URL to your own repository once you've uploaded the data files
    url = f'https://raw.githubusercontent.com/dexplo/bar_chart_race/master/data/{name}.csv'

    index_dict = {
        'covid19_tutorial': 'date',
        'covid19': 'date',
        'urban_pop': 'year',
        'baseball': None
    }
    
    if name not in index_dict:
        raise ValueError(
            f"Dataset '{name}' not recognized. Available datasets: "
            f"{', '.join(index_dict.keys())}"
        )
        
    index_col = index_dict[name]
    parse_dates = [index_col] if index_col else None
    
    try:
        return pd.read_csv(url, index_col=index_col, parse_dates=parse_dates)
    except Exception as e:
        raise ConnectionError(f"Failed to load dataset '{name}': {e}")

def prepare_wide_data(
    df: pd.DataFrame,
    orientation: Literal['h', 'v'] = 'h',
    sort: Literal['desc', 'asc'] = 'desc',
    n_bars: Optional[int] = None,
    interpolate_period: bool = False,
    steps_per_period: int = 10,
    compute_ranks: bool = True
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
    '''
    Prepares 'wide' data for bar chart animation.
    Returns two DataFrames - the interpolated values and the interpolated ranks
    
    There is no need to use this function directly to create the animation.
    You can pass your DataFrame directly to `bar_chart_race`.

    This function is useful if you want to view the prepared data without
    creating an animation.

    Parameters
    ----------
    df : pd.DataFrame
        Must be a 'wide' pandas DataFrame where each row represents a
        single period of time.
        Each column contains the values of the bars for that category.
        Optionally, use the index to label each time period.

    orientation : 'h' or 'v', default 'h'
        Bar orientation - horizontal or vertical

    sort : 'desc' or 'asc', default 'desc'
        Choose how to sort the bars. Use 'desc' to put largest bars on
        top and 'asc' to place largest bars on bottom.

    n_bars : int, default None
        Choose the maximum number of bars to display on the graph.
        By default, use all bars. New bars entering the race will
        appear from the bottom or top.

    interpolate_period : bool, default `False`
        Whether to interpolate the period. Only valid for datetime or
        numeric indexes. When set to `True`, for example,
        the two consecutive periods 2020-03-29 and 2020-03-30 with
        `steps_per_period` set to 4 would yield a new index of
        2020-03-29 00:00:00
        2020-03-29 06:00:00
        2020-03-29 12:00:00
        2020-03-29 18:00:00
        2020-03-30 00:00:00

    steps_per_period : int, default 10
        The number of steps to go from one time period to the next.
        The bars will grow linearly between each period.

    compute_ranks : bool, default True
        When `True` return both the interpolated values and ranks DataFrames
        Otherwise just return the values

    Returns
    -------
    Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]
        If compute_ranks is True, returns a tuple of (values_df, ranks_df)
        Otherwise, returns just the values_df

    Examples
    --------
    df_values, df_ranks = bcr.prepare_wide_data(df)
    '''
    if n_bars is None:
        n_bars = df.shape[1]

    df_values = df.reset_index()
    df_values.index = df_values.index * steps_per_period
    new_index = range(df_values.index[-1] + 1)
    df_values = df_values.reindex(new_index)
    
    if interpolate_period:
        if df_values.iloc[:, 0].dtype.kind == 'M':
            first, last = df_values.iloc[[0, -1], 0]
            dr = pd.date_range(first, last, periods=len(df_values))
            df_values.iloc[:, 0] = dr
        else:
            df_values.iloc[:, 0] = df_values.iloc[:, 0].interpolate()
    else:
        df_values.iloc[:, 0] = df_values.iloc[:, 0].fillna(method='ffill')
    
    df_values = df_values.set_index(df_values.columns[0])
    
    if compute_ranks:
        df_ranks = df_values.rank(axis=1, method='first', ascending=False).clip(upper=n_bars + 1)
        if (sort == 'desc' and orientation == 'h') or (sort == 'asc' and orientation == 'v'):
            df_ranks = n_bars + 1 - df_ranks
        df_ranks = df_ranks.interpolate()
    
    df_values = df_values.interpolate()
    
    if compute_ranks:
        return df_values, df_ranks
    return df_values

def prepare_long_data(
    df: pd.DataFrame,
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
    '''
    Prepares 'long' data for bar chart animation.
    Returns two DataFrames - the interpolated values and the interpolated ranks
    
    You (currently) cannot pass long data to `bar_chart_race` directly. Use this function
    to create your wide data first before passing it to `bar_chart_race`.

    Parameters
    ----------
    df : pd.DataFrame
        Must be a 'long' pandas DataFrame where one column contains
        the period, another the categories, and the third the values
        of each category for each period.
        
        This DataFrame will be passed to the `pivot_table` method to turn
        it into a wide DataFrame. It will then be passed to the
        `prepare_wide_data` function.

    index : str
        Name of column used for the time period. It will be placed in the index

    columns : str
        Name of column containing the categories for each time period. This column
        will get pivoted so that each unique value is a column.

    values : str
        Name of column holding the values for each time period of each category.
        This column will become the values of the resulting DataFrame

    aggfunc : str or aggregation function, default 'sum'
        String name of aggregation function ('sum', 'min', 'mean', 'max, etc...)
        or actual function (np.sum, np.min, etc...).
        Categories that have multiple values for the same time period must be
        aggregated for the animation to work.

    orientation : 'h' or 'v', default 'h'
        Bar orientation - horizontal or vertical

    sort : 'desc' or 'asc', default 'desc'
        Choose how to sort the bars. Use 'desc' to put largest bars on
        top and 'asc' to place largest bars on bottom.

    n_bars : int, default None
        Choose the maximum number of bars to display on the graph.
        By default, use all bars. New bars entering the race will
        appear from the bottom or top.

    interpolate_period : bool, default `False`
        Whether to interpolate the period. Only valid for datetime or
        numeric indexes. When set to `True`, for example,
        the two consecutive periods 2020-03-29 and 2020-03-30 with
        `steps_per_period` set to 4 would yield a new index of
        2020-03-29 00:00:00
        2020-03-29 06:00:00
        2020-03-29 12:00:00
        2020-03-29 18:00:00
        2020-03-30 00:00:00

    steps_per_period : int, default 10
        The number of steps to go from one time period to the next.
        The bars will grow linearly between each period.

    compute_ranks : bool, default True
        When `True` return both the interpolated values and ranks DataFrames
        Otherwise just return the values

    Returns
    -------
    Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]
        If compute_ranks is True, returns a tuple of (values_df, ranks_df)
        Otherwise, returns just the values_df

    Examples
    --------
    df_values, df_ranks = bcr.prepare_long_data(df)
    bcr.bar_chart_race(df_values, steps_per_period=1, period_length=50)
    '''
    df_wide = df.pivot_table(
        index=index,
        columns=columns,
        values=values,
        aggfunc=aggfunc
    ).fillna(method='ffill')
    
    return prepare_wide_data(
        df_wide,
        orientation=orientation,
        sort=sort,
        n_bars=n_bars,
        interpolate_period=interpolate_period,
        steps_per_period=steps_per_period,
        compute_ranks=compute_ranks
    )


def read_images(filename: str, columns: List[str]) -> Dict[str, np.ndarray]:
    """
    Read images for columns based on codes in the _codes directory.
    
    Parameters
    ----------
    filename : str
        Name of the code file without extension (e.g., 'country', 'nfl')
    columns : List[str]
        List of column names to get images for
        
    Returns
    -------
    Dict[str, np.ndarray]
        Dictionary mapping column names to image arrays
    
    Raises
    ------
    FileNotFoundError
        If the code files cannot be found
    ValueError
        If a column code cannot be found
    """
    image_dict: Dict[str, np.ndarray] = {}
    code_path = Path(__file__).resolve().parent / "_codes"
    code_value_path = code_path / 'code_value.csv'
    data_path = code_path / f'{filename}.csv'
    
    if not code_path.exists():
        raise FileNotFoundError(f"Code directory not found at {code_path}")
    if not code_value_path.exists():
        raise FileNotFoundError(f"Code value file not found at {code_value_path}")
    if not data_path.exists():
        raise FileNotFoundError(f"Data file for {filename} not found at {data_path}")
    
    url_path = pd.read_csv(code_value_path).query('code == @filename')['value'].values[0]
    codes = pd.read_csv(data_path, index_col='code')['value'].to_dict()

    for col in columns:
        col_lower = col.lower()
        if col_lower not in codes:
            raise ValueError(f"Code for column '{col}' not found in {filename}.csv")
            
        code = codes[col_lower]
        if url_path == 'self':
            final_url = code
        else:
            final_url = url_path.format(code=code)
            
        try:
            image_dict[col] = mimage.imread(final_url)
        except Exception as e:
            raise ValueError(f"Failed to read image for column '{col}': {e}")
            
    return image_dict