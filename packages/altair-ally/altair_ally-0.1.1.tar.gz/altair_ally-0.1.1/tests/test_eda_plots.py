import pandas as pd
import altair as alt
import altair_ally.eda_plots as eda_plots

def test_get_label_angle():
    # Test with 7 labels and 2 offset groups
    labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    offset_groups = 2
    angle = eda_plots.get_label_angle(labels, offset_groups)
    assert angle == 20

    # Test with 5 labels and 1 offset group
    labels = ['a', 'b', 'c', 'd', 'e']
    offset_groups = 1
    angle = eda_plots.get_label_angle(labels, offset_groups)
    assert angle == 0

def test_dist():
    # Test with numerical data and default options
    data = pd.DataFrame({'x': [1, 2, 3, 4, 5]})
    chart = eda_plots.dist(data)
    assert isinstance(chart, alt.ConcatChart)

    # Test with categorical data and custom options
    data = pd.DataFrame({'x': ['a', 'b', 'c', 'd', 'e'], 'y': [1, 2, 3, 4, 5]})
    chart = eda_plots.dist(data, color='y', dtype='categorical', mark='bar')
    assert isinstance(chart, alt.ConcatChart)