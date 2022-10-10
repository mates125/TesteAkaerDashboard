import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
import yfinance as yf
import plotly.graph_objects as go

ticker = yf.Ticker("CL=F")
data = ticker.history(period="1y")
data = data.drop(columns={'Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'})
data = data.reset_index()
print(data)
data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y")
app = dash.Dash(__name__)
server = app.server

app.title = " Litro Petróleo Cru"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Petróleo Cru",),
                html.P(children="Preço do petróleo cru em reais ao longo do último ano"
                                " Os dados foram retirados da biblioteca yfinance e podem ser encontrados em: "
                                " https://br.financas.yahoo.com/quote/CL%3DF/history?p=CL%3DF",),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_charts(start_date, end_date):
    mask = (
        (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = go.Scatter(
                x = filtered_data["Date"],
                y = filtered_data["Close"],
                mode = "lines",
        )
    return go.Figure(data=price_chart_figure)

if __name__ == "__main__":
    app.run_server(debug=True)

