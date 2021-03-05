import plotly.graph_objects as go
from PIL import Image

import numpy as np
import pandas as pd

XMAX = 5216
YMAX = 2653


def render_map(data):
    # Create figure
    fig = go.Figure()

    data_cols = data.columns[2:]

    # Add trace
    fig.add_trace(
        # go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
        go.Scatter(
            x=data["x"], y=data["y"],
            mode='markers', hoverinfo="text",
            hovertext=data[data_cols[0]],
            marker_size=data[data_cols[0]],
        )
    )

    # Add images
    img = Image.open('./a3_data/Vastopolis_Map.png')
    fig.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=YMAX,
            sizex=XMAX,
            sizey=YMAX,
            sizing="stretch",
            opacity=1,
            layer="below")
    )

    buttons = []
    for col in data_cols:
        button = dict(
            args=[{"hovertext": [["{}: {}".format(col, str(i)) for i in data[col]]], "marker.size": [
                data[col]]}],
            label=col,
            method="restyle",
        )
        buttons.append(button)

    # Set templates
    fig.update_layout(template="plotly_white")
    fig.update_xaxes(showgrid=False, range=[0, XMAX], showticklabels=False)
    fig.update_yaxes(showgrid=False, range=[0, YMAX], showticklabels=False)
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.05,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    fig.update_layout(
        annotations=[
            dict(text="Metric: ", x=0, xref="paper", y=1.07, yref="paper",
                 align="left", showarrow=False)]
    )
    fig.show()


if __name__ == "__main__":
    x = np.random.randint(0, XMAX, (10))
    y = np.random.randint(0, YMAX, (10))
    var1 = np.random.randint(50, 100, (10))
    var2 = np.random.randint(50, 100, (10))
    data = pd.DataFrame(data=zip(x, y, var1, var2),
                        columns=["x", "y", "var1", "var2"])

    render_map(data)
