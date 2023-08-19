import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def algorithms_benchmarks_plot(df):
    maps = df["map"].unique()
    algorithms = df["algorithm"].unique()

    cols = 2
    rows = len(maps) // cols + (len(maps) % cols)

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=maps)

    for i, map in enumerate(maps):

        row = (i % rows) + 1
        col = (i // cols) + 1

        map_timestamps = df[df['map'] == map]

        x = algorithms
        y = map_timestamps['without_deadlocks']

        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                text=y,
                texttemplate='%{text:.4f}',
                name="Without deadlocks",
                marker_color="#F7BE15",
                textposition="outside",
                showlegend=False if i > 0 else True
            ),
            row=row,
            col=col
        )

        y = map_timestamps['with_deadlocks']

        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                text=y,
                texttemplate='%{text:.4f}',
                name="With deadlocks",
                marker_color="#1C818A",
                textposition="outside",
                showlegend=False if i > 0 else True
            ),
            row=row,
            col=col,
        )

        fig.update_xaxes(title_text="Algorithms used", row=row, col=col)
        fig.update_yaxes(title_text="Execution time [seconds]", row=row, col=col)    

    fig.show()