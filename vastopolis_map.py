import plotly.graph_objects as go
from PIL import Image

# import numpy as np
import pandas as pd

XMAX = 5216
YMAX = 2653


def render_map(data):
    # Create figure
    fig = go.Figure()

    data_cols = data.columns[3:]
    dates = data["date"].unique()
    filtered_data = data[data["date"] == dates[0]]

    # Add trace
    fig.add_trace(
        # go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
        go.Scatter(
            x=filtered_data["x"], y=filtered_data["y"],
            mode='markers', hoverinfo="text",
            hovertext=filtered_data[data_cols[0]],
            marker_size=filtered_data[data_cols[0]],
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

    menu, annotations = make_menu(data_cols, dates, data)

    # Set templates
    fig.update_layout(template="plotly_white")
    fig.update_xaxes(showgrid=False, range=[0, XMAX], showticklabels=False)
    fig.update_yaxes(showgrid=False, range=[0, YMAX], showticklabels=False)
    fig.update_layout(
        updatemenus=menu
    )

    fig.update_layout(
        annotations=annotations
    )
    fig.write_html("index.html")
    fig.show()


def make_menu(data_cols, dates, data):
    date_buttons = []
    col_button_sets = []

    for date in dates:
        date_data = data[data["date"] == date]
        column_buttons = []
        for col in data_cols:
            button = dict(
                args=[
                    {
                        "hovertext": [["{}: {}".format(col, str(i)) for i in
                                       date_data[col]]],
                        "marker.size": [date_data[col]]
                    }
                ],
                label=col,
                method="restyle",
            )
            column_buttons.append(button)
        col_button_sets.append(column_buttons)
        button = dict(
            args=[
                {
                    "x": [list(date_data["x"])],
                    "y": [list(date_data["y"])],
                },
                {
                    "updatemenus[1].buttons": col_button_sets[-1],
                    "updatemenus[1].active": 0
                }
            ],
            label=date,
            method="update",
        )
        button["args"][0].update(col_button_sets[-1][0]["args"][0])
        date_buttons.append(button)

    menu = [
        dict(
            buttons=date_buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.03,
            xanchor="left",
            y=1.115,
            yanchor="top"
        ),
        dict(
            buttons=col_button_sets[0],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.205,
            xanchor="left",
            y=1.115,
            yanchor="top"
        )
    ]

    annotations = [
        dict(text="Date: ", x=0, xref="paper", y=1.09, yref="paper",
             align="left", showarrow=False),
        dict(text="Metric: ", x=0.17, xref="paper", y=1.09, yref="paper",
             align="left", showarrow=False)
    ]

    return (menu, annotations)


def load_data():
    raw_data = pd.read_csv("./a3_data/disease_posts.csv")
    def x(x): return XMAX*(float(x["Location"].split(" ")[0]) - 42.1609)/0.1408

    def y(x): return YMAX - \
        (YMAX*(float(x["Location"].split(" ")[1]) - 93.1923)/.375)

    raw_data["x"] = raw_data.apply(x, axis=1)
    raw_data["y"] = raw_data.apply(y, axis=1)
    raw_data["dummy"] = 1

    data = raw_data[["x", "y", "date", "dummy"]]
    data = data.sort_values(by="date")

    return data


def make_test_data():
    x = [1000, 2000, 3000, 4000]
    y = [100, 200, 300, 400]
    date = ["2020-01-01", "2020-02-02", "2020-03-03", "2020-04-04"]
    var1 = [10, 20, 30, 40]
    var2 = [20, 40, 60, 80]
    df = pd.DataFrame(data=zip(x, y, date, var1, var2),
                      columns=["x", "y", "date", "var1", "var2"])

    return df


if __name__ == "__main__":
    render_map(load_data())
