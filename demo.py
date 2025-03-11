"""
Bar Chart Racer Demo Script

This script demonstrates the basic functionality of the bar_chart_racer package.
It creates a simple bar chart race using sample data.
"""

import pandas as pd
import bar_chart_racer as bcr

# Load sample data
print("Loading sample COVID-19 data...")
df = bcr.load_dataset('covid19')
print(f"Data loaded with shape: {df.shape}")

# Create a bar chart race
print("\nCreating bar chart race animation...")
print("This will be saved as 'covid19_demo.html' in the current directory.")

# Use a smaller subset of data for quick demonstration
df_subset = df.iloc[-30:-10]  # Use 20 days of data

# Create the animation
bcr.bar_chart_race_plotly(
    df=df_subset,
    filename='covid19_demo.html',
    title='COVID-19 Deaths by Country',
    orientation='h',
    sort='desc',
    n_bars=8,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=10,
    period_length=500,
    period_template='%B %d, %Y',
    period_summary_func=lambda v, r: {
        'x': .99, 'y': .05,
        'text': f'Total deaths: {v.sum():,.0f}',
        'align': 'right', 'size': 12
    },
    bar_size=.95,
    bar_textposition='outside',
    bar_label_font=10,
    tick_label_font=10,
    filter_column_colors=True
)

print("\nDemo completed! Open 'covid19_demo.html' in your browser to view the animation.")
print("For more examples and documentation, visit: https://github.com/yourusername/bar_chart_racer")