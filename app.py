from binance.client import Client
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

client = Client()


@st.cache_data(ttl=60)
def get_historical_klines(
    symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, start_str="1 day UTC"
):
    candles = client.get_historical_klines(symbol, interval, start_str)

    df = pd.DataFrame(
        candles,
        columns=[
            "Open Time",
            "Open Price",
            "High Price",
            "Low Price",
            "Close Price",
            "Volume",
            "Close Time",
            "Quote Asset Volume",
            "Number of Trades",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore",
        ],
    )

    df = df[
        ["Open Time", "Open Price", "High Price", "Low Price", "Close Price", "Volume"]
    ]

    df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")

    df.set_index("Open Time", inplace=True)

    df = df.astype(float)
    return df


st.set_page_config(page_title="Crypto Estácio", page_icon="🪙", layout="wide")

st.sidebar.title("Crypto Estácio")
image_sidebar = Image.open("./images/estacio.png")
st.sidebar.image(image=image_sidebar, use_container_width=True)

symbol = st.sidebar.text_input(label="Símbolo", value="BTCUSDT")
interval = st.sidebar.selectbox(
    label="Intervalo de Tempo",
    options=[
        client.KLINE_INTERVAL_1MINUTE,
        client.KLINE_INTERVAL_5MINUTE,
        client.KLINE_INTERVAL_1HOUR,
        client.KLINE_INTERVAL_4HOUR,
        client.KLINE_INTERVAL_1DAY,
    ],
    index=2,
)
date = st.sidebar.selectbox(
    label="Período de Análise",
    options=[
        "1 day ago UTC",
        "5 days ago UTC",
        "1 month ago UTC",
        "6 months ago UTC",
        "1 year ago UTC",
    ],
)


df = get_historical_klines(symbol, interval, date)

fig = go.Figure(
    go.Candlestick(
        x=df.index,
        open=df["Open Price"],
        high=df["High Price"],
        low=df["Low Price"],
        close=df["Close Price"],
    )
)

fig.update_layout(
    xaxis_title="Data e Hora",
    yaxis_title="Preço",
    xaxis_rangeslider_visible=False,
)

st.markdown(body=f"<h1>Gráfico de Velas - {symbol}</h1>", unsafe_allow_html=True)

st.plotly_chart(figure_or_data=fig)
