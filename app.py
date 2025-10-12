from binance.client import Client
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)

TOP_10_COINS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "DOGEUSDT",
    "ADAUSDT",
    "SHIBUSDT",
    "AVAXUSDT",
    "DOTUSDT",
]


@st.cache_data(ttl=30)
def get_market_data(symbols: list[str]):
    all_tickers = client.get_ticker()

    market_data = [ticker for ticker in all_tickers if ticker["symbol"] in symbols]

    df = pd.DataFrame(market_data)

    df = df[
        [
            "symbol",
            "lastPrice",
            "priceChangePercent",
            "highPrice",
            "lowPrice",
            "quoteVolume",
        ]
    ]
    df.columns = [
        "Símbolo",
        "Preço (USDT)",
        "Variação % (24h)",
        "Máxima (24h)",
        "Mínima (24h)",
        "Volume (USDT)",
    ]

    numeric_cols = [
        "Preço (USDT)",
        "Variação % (24h)",
        "Máxima (24h)",
        "Mínima (24h)",
        "Volume (USDT)",
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    return df


if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = "BTCUSDT"
if "selected_interval" not in st.session_state:
    st.session_state.selected_interval = Client.KLINE_INTERVAL_1HOUR
if "selected_date" not in st.session_state:
    st.session_state.selected_date = "1 day ago UTC"


@st.cache_data(ttl=60)
def get_historical_klines(symbol, interval, start_str):
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


# --- Configuração da Página e Sidebar ---
st.set_page_config(page_title="Crypto Estácio", page_icon="🪙", layout="wide")

st.sidebar.title("Crypto Estácio")
image_sidebar = Image.open("./images/estacio.png")
st.sidebar.image(image=image_sidebar)

st.session_state.selected_symbol = st.sidebar.text_input(
    label="Símbolo", value=st.session_state.selected_symbol
)
st.session_state.selected_interval = st.sidebar.selectbox(
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
st.session_state.selected_date = st.sidebar.selectbox(
    label="Período de Análise",
    options=[
        "1 day ago UTC",
        "5 days ago UTC",
        "1 month ago UTC",
        "6 months ago UTC",
        "1 year ago UTC",
    ],
)

# --- Renderização do Gráfico ---

df = get_historical_klines(
    st.session_state.selected_symbol,
    st.session_state.selected_interval,
    st.session_state.selected_date,
)

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
    yaxis_title="Preço (USDT)",
    xaxis_rangeslider_visible=False,
)

st.markdown(
    f"<h1>{st.session_state.selected_symbol.split('USDT')[0]} em relação ao dólar</h1>",
    unsafe_allow_html=True,
)

st.plotly_chart(figure_or_data=fig, use_container_width=True)

# --- Tabela de Criptomoedas ---

st.markdown("---")
st.header("Principais Moedas")

market_df = get_market_data(TOP_10_COINS)

cols = st.columns((0.5, 1.5, 1.5, 1.5, 1.5, 2))

headers = ["#", "Ativo", "Preço", "Variação (24h)", "Máxima (24h)", "Volume (USDT)"]
for col, header in zip(cols, headers):
    col.markdown(f"**{header}**")

for index, row in market_df.iterrows():
    cols = st.columns((0.5, 1.5, 1.5, 1.5, 1.5, 2))

    cols[0].write(f"{index + 1}")

    if cols[1].button(row["Símbolo"], key=f"btn_{row['Símbolo']}"):
        st.session_state.selected_symbol = row["Símbolo"]
        st.session_state.selected_interval = Client.KLINE_INTERVAL_1HOUR
        st.session_state.selected_date = "1 day ago UTC"
        st.rerun()

    cols[2].write(f"${row['Preço (USDT)']:,.4f}")

    change = row["Variação % (24h)"]
    color = "green" if change >= 0 else "red"
    cols[3].markdown(
        f"<span style='color:{color};'>{change:+.2f}%</span>", unsafe_allow_html=True
    )

    cols[4].write(f"${row['Máxima (24h)']:,.4f}")

    cols[5].write(f"${row['Volume (USDT)']:,.2f}")
