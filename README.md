# Bar Chart Racer

[![](https://img.shields.io/pypi/v/bar_chart_racer)](https://pypi.org/project/bar_chart_racer)
[![PyPI - License](https://img.shields.io/pypi/l/bar_chart_racer)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)

Make animated bar and line chart races in Python with matplotlib and plotly.

![img](https://github.com/sofus-nl/bar_chart_racer/raw/main/images/covid19_horiz.gif)

## Official Documentation

Visit the [bar_chart_racer official documentation](https://github.com/sofus-nl/bar_chart_racer) for detailed usage instructions.

## Requirements

- Python 3.11 or higher
- pandas 2.0.0 or higher
- matplotlib 3.7.0 or higher
- plotly 5.13.0 or higher

## Installation

Install with:

* `pip install bar_chart_racer`

## Quickstart

Must begin with a pandas DataFrame containing 'wide' data where:

* Every row represents a single period of time
* Each column holds the value for a particular category
* The index contains the time component (optional)
  
The data below is an example of properly formatted data. It shows total deaths from COVID-19 for several countries by date.

![img](https://github.com/sofus-nl/bar_chart_racer/raw/main/images/wide_data.png)

### Create bar and line chart races

There are three core functions available to construct the animations.

* `bar_chart_race`
* `bar_chart_race_plotly`
* `line_chart_race`

The above animation was created with the help of matplotlib using the following call to `bar_chart_race`.

```python
import bar_chart_racer as bcr
df = bcr.load_dataset('covid19_tutorial')
bcr.bar_chart_race(
        df=df,
        filename='../docs/images/covid19_horiz.gif',
        orientation='h',
        sort='desc',
        n_bars=8,
        fixed_order=False,
        fixed_max=True,
        steps_per_period=20,
        period_length=500,
        end_period_pause=0,
        interpolate_period=False,
        period_label={'x': .98, 'y': .3, 'ha': 'right', 'va': 'center'},
        period_template='%B %d, %Y',
        period_summary_func=lambda v, r: {'x': .98, 'y': .2,
                                          's': f'Total deaths: {v.sum():,.0f}',
                                          'ha': 'right', 'size': 11},
        perpendicular_bar_func='median',
        colors='dark12',
        title='COVID-19 Deaths by Country',
        bar_size=.95,
        bar_textposition='inside',
        bar_texttemplate='{x:,.0f}',
        bar_label_font=7,
        tick_label_font=7,
        tick_template='{x:,.0f}',
        shared_fontdict=None,
        scale='linear',
        fig=None,
        writer=None,
        bar_kwargs={'alpha': .7},
        fig_kwargs={'figsize': (6, 3.5), 'dpi': 144},
        filter_column_colors=False)
```

### Save animation to disk or embed into a Jupyter Notebook

If you are working within a Jupyter Notebook, leave the `filename` as `None` and it will be automatically embedded into a Jupyter Notebook.

```python
bcr.bar_chart_race(df=df, filename=None)
```

![img](https://github.com/sofus-nl/bar_chart_racer/raw/main/images/bcr_notebook.png)

### Customization

There are many options to customize the bar chart race to get the animation you desire. Below, we have an animation where the maximum x-value and order of the bars are set for the entire duration. A custom summary label and perpendicular bar of the median is also added.

```python
def period_summary(values, ranks):
    top2 = values.nlargest(2)
    leader = top2.index[0]
    lead = top2.iloc[0] - top2.iloc[1]
    s = f'{leader} by {lead:.0f}'
    return {'s': s, 'x': .99, 'y': .03, 'ha': 'right', 'size': 8}

df_baseball = bcr.load_dataset('baseball').pivot(index='year',
                                                 columns='name',
                                                 values='hr')
df_baseball.bcr.bar_chart_race(
                   period_length=1000,
                   fixed_max=True,
                   fixed_order=True,
                   n_bars=10,
                   period_summary_func=period_summary,
                   period_label={'x': .99, 'y': .1},
                   period_template='Season {x:,.0f}',
                   title='Top 10 Home Run Hitters by Season Played')
```

![img](https://github.com/sofus-nl/bar_chart_racer/raw/main/images/baseball_horiz.gif)
