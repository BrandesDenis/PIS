
from typing import Iterable

import plotly.graph_objects as go


def pie_plot(values: Iterable, labels: Iterable, title: str) -> go.Figure:
    pie = go.Pie(labels=labels, values=values, textinfo='label+percent')
    fig = go.Figure(data=[pie])
    fig.update_layout(showlegend=False)

    return fig


def get_plot_html(figure: go.Figure,
                  height: int,
                  width: int) -> str:

    return figure.to_html(full_html=False,
                          default_height=height,
                          default_width=width)
