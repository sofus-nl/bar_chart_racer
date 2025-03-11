import pytest
import matplotlib.pyplot as plt
from typing import Dict, Any
import pandas as pd

from bar_chart_racer import load_dataset, bar_chart_race


# Load test data
df = load_dataset('covid19')
df = df.iloc[-20:-16]
df1 = df.reset_index(drop=True)


class TestSimpleBC:
    """Test suite for bar_chart_race functionality."""

    def test_defaults(self):
        """Test default parameters."""
        bar_chart_race(df)
        bar_chart_race(df, orientation='v')

    def test_sort(self):
        """Test sorting options."""
        bar_chart_race(df, sort='asc')
        bar_chart_race(df, orientation='v', sort='asc')

    def test_nbars(self):
        """Test number of bars parameter."""
        bar_chart_race(df, sort='desc', n_bars=8)
        bar_chart_race(df, orientation='v', sort='desc', n_bars=8)

    def test_fixed_order(self):
        """Test fixed order parameter."""
        bar_chart_race(df, sort='asc', n_bars=8, fixed_order=True)
        bar_chart_race(df, fixed_order=['Iran', 'USA', 'Italy', 'Spain'])

    def test_fixed_max(self):
        """Test fixed maximum parameter."""
        bar_chart_race(df, fixed_max=True)

    def test_steps_per_period(self):
        """Test steps per period parameter."""
        bar_chart_race(df, sort='asc', steps_per_period=2)
        bar_chart_race(df, sort='asc', steps_per_period=30)

    def test_interpolate_period(self):
        """Test period interpolation."""
        bar_chart_race(df, interpolate_period=True, n_bars=8)

    def test_bar_size(self):
        """Test bar size parameter."""
        bar_chart_race(df, n_bars=8, bar_size=.99)

    def test_period_label(self):
        """Test period label options."""
        bar_chart_race(df, n_bars=8, period_label=False)
        bar_chart_race(df, n_bars=8, period_label={'x': .99, 'y': .1, 'ha': 'right'})

    def test_period_fmt(self):
        """Test period format templates."""
        bar_chart_race(df, n_bars=8, period_template='%b %d, %Y')
        bar_chart_race(df1, n_bars=8, interpolate_period=True, period_template='{x: .2f}')

    def test_period_summary_func(self):
        """Test period summary function."""
        def summary(values: pd.Series, ranks: pd.Series) -> Dict[str, Any]:
            total_deaths = int(round(values.sum(), -2))
            s = f'Total Deaths - {total_deaths:,.0f}'
            return {'x': .99, 'y': .05, 's': s, 'ha': 'right', 'size': 8}

        bar_chart_race(df, n_bars=8, period_summary_func=summary)
    
    def test_perpendicular_bar_func(self):
        """Test perpendicular bar function."""
        bar_chart_race(df, n_bars=8, perpendicular_bar_func='mean')
        
        def func(values: pd.Series, ranks: pd.Series) -> float:
            return values.quantile(.9)
        
        bar_chart_race(df, n_bars=8, perpendicular_bar_func=func)

    def test_period_length(self):
        """Test period length parameter."""
        bar_chart_race(df, n_bars=8, period_length=1200)

    def test_figsize(self):
        """Test figure size parameters."""
        bar_chart_race(df, fig_kwargs={'figsize': (4, 2), 'dpi': 120})

    def test_filter_column_colors(self):
        """Test column color filtering."""
        with pytest.warns(UserWarning):
            bar_chart_race(df, n_bars=6, sort='asc', colors='Accent')

        bar_chart_race(df, n_bars=6, sort='asc', colors='Accent', filter_column_colors=True)
        bar_chart_race(df, n_bars=6, colors=plt.cm.tab20.colors[:19])

    def test_colors(self):
        """Test color options."""
        bar_chart_race(df, colors=['red', 'blue'], filter_column_colors=True)

        with pytest.raises(KeyError):
            bar_chart_race(df, colors='adf')

    def test_title(self):
        """Test title options."""
        bar_chart_race(df, n_bars=6, title='Great title')
        bar_chart_race(df, n_bars=6, title={'label': 'Great title', 'size': 20})

    def test_shared_fontdict(self):
        """Test shared font dictionary."""
        bar_chart_race(df, n_bars=6, shared_fontdict={
            'family': 'Courier New',
            'weight': 'bold',
            'color': 'teal'
        })

    def test_scale(self):
        """Test scale parameter."""
        bar_chart_race(df, n_bars=6, scale='log')

    def test_save(self):
        """Test saving to different formats."""
        bar_chart_race(df, 'tests/videos/test.mp4', n_bars=6)
        bar_chart_race(df, 'tests/videos/test.gif', n_bars=6, writer='imagemagick')
        bar_chart_race(df, 'tests/videos/test.html', n_bars=6)

    def test_writer(self):
        """Test different writers."""
        bar_chart_race(df, 'tests/videos/test.gif', n_bars=6, writer='pillow')

    def test_fig(self):
        """Test using a custom figure."""
        fig, ax = plt.subplots(dpi=100)
        bar_chart_race(df, n_bars=6, fig=fig)

    def test_bar_kwargs(self):
        """Test bar keyword arguments."""
        bar_chart_race(df, n_bars=6, bar_kwargs={'alpha': .2, 'ec': 'black', 'lw': 3})
        