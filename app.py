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
    "BTC",
    "ETH",
    "BNB",
    "SOL",
    "XRP",
    "DOGE",
    "ADA",
    "SHIB",
    "AVAX",
    "DOT",
]

COIN_INFO = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "BNB": "BNB",
    "SOL": "Solana",
    "XRP": "XRP",
    "DOGE": "Dogecoin",
    "ADA": "Cardano",
    "SHIB": "Shiba Inu",
    "AVAX": "Avalanche",
    "DOT": "Polkadot",
}
# ------------------------------------------------------------------

DATE_OPTIONS_VALUES = [
    "1 day ago UTC",
    "5 days ago UTC",
    "1 month ago UTC",
    "6 months ago UTC",
    "1 year ago UTC",
]

DATE_OPTIONS_DISPLAY = {
    "1 day ago UTC": "Último dia",
    "5 days ago UTC": "Últimos 5 dias",
    "1 month ago UTC": "Último mês",
    "6 months ago UTC": "Últimos 6 meses",
    "1 year ago UTC": "Último ano",
}


def format_date_option(option_value):
    return DATE_OPTIONS_DISPLAY.get(option_value, option_value)


ema_periods = [21, 50, 200]


@st.cache_data(ttl=30)
def get_market_data(symbols: list[str]):
    all_tickers = client.get_ticker()
    symbols_with_usdt = list(map(lambda coin: f"{coin}USDT", symbols))

    market_data = [
        ticker for ticker in all_tickers if ticker["symbol"] in symbols_with_usdt
    ]

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
    df["Símbolo"] = df["Símbolo"].apply(lambda x: x.split("USDT")[0])

    df["Nome Completo"] = df["Símbolo"].map(COIN_INFO).fillna(df["Símbolo"])

    df["Icon URL"] = df["Símbolo"].apply(
        lambda x: f"https://assets.coincap.io/assets/icons/{x.lower()}@2x.png"
    )
    # ------------------------------------------------------------------

    return df


if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = "BTC"
if "selected_interval" not in st.session_state:
    st.session_state.selected_interval = Client.KLINE_INTERVAL_1HOUR
if "selected_date" not in st.session_state:
    st.session_state.selected_date = "1 day ago UTC"


@st.cache_data(ttl=60)
def get_historical_klines(symbol, interval, start_str):

    candles = client.get_historical_klines(f"{symbol}USDT", interval, start_str)

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

    for period in ema_periods:
        df[f"EMA_{period}"] = df["Close Price"].ewm(span=period, adjust=False).mean()

    df.set_index("Open Time", inplace=True)
    df = df.astype(float)

    return df


# --- Configuração da Página e Sidebar ---
st.set_page_config(page_title="Crypto Estácio", page_icon="🪙", layout="wide")

st.sidebar.title("Crypto Estácio")
image_sidebar = Image.open("./images/estacio.png")
st.sidebar.image(image=image_sidebar)

try:
    default_symbol_index = TOP_10_COINS.index(st.session_state.selected_symbol)
except ValueError:
    default_symbol_index = 0

st.session_state.selected_symbol = st.sidebar.selectbox(
    label="Símbolo",
    options=TOP_10_COINS,
    index=default_symbol_index,
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
    options=DATE_OPTIONS_VALUES,
    format_func=format_date_option,
)

# --- Renderização do Gráfico ---


df = get_historical_klines(
    st.session_state.selected_symbol,
    st.session_state.selected_interval,
    st.session_state.selected_date,
)

fig = go.Figure()

# Gráfico de velas
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open Price"],
        high=df["High Price"],
        low=df["Low Price"],
        close=df["Close Price"],
        name="Candlesticks",
    )
)

# Adicionando EMAs ao gráfico
for ema_period in ema_periods:
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[f"EMA_{ema_period}"],
            mode="lines",
            name=f"EMA {ema_period}",
        )
    )

fig.update_layout(
    xaxis_title="Data e Hora",
    yaxis_title="Preço (USDT)",
    xaxis_rangeslider_visible=False,
)

selected_symbol_str = st.session_state.selected_symbol
coin_full_name = COIN_INFO.get(selected_symbol_str, selected_symbol_str)

selected_coin_icon_url = (
    f"https://assets.coincap.io/assets/icons/{selected_symbol_str.lower()}@2x.png"
)
img_width = 55
img_margin_right = 10

title_html = f"""
<div style="display: flex; align-items: center;">
    <img src="{selected_coin_icon_url}" width="{img_width}" style="margin-right: {img_margin_right}px;">
    <div style="font-size: 2.5em; font-weight: 600; margin: 0;">
        {coin_full_name} ({selected_symbol_str})
    </div>
</div>
"""

st.markdown(title_html, unsafe_allow_html=True)

st.plotly_chart(figure_or_data=fig, use_container_width=True)

# --- Tabela de Criptomoedas ---

st.markdown("---")
st.header("🪙 Principais Moedas")

market_df = get_market_data(TOP_10_COINS)

for index, row in market_df.iterrows():
    icon_url = row["Icon URL"]
    full_name = row["Nome Completo"]
    symbol = row["Símbolo"]

    expander_label = f"**{index + 1}. {full_name}** `{symbol}`"

    with st.expander(label=expander_label):
        col_img_inside, col1, col2, col3 = st.columns([0.5, 1.5, 1.5, 1.5])

        with col_img_inside:
            st.image(icon_url, width=40)

        with col1:
            if st.button("Ver Gráfico 📈", key=f"btn_{symbol}"):
                st.session_state.selected_symbol = symbol
                st.session_state.selected_interval = Client.KLINE_INTERVAL_1HOUR
                st.session_state.selected_date = "1 day ago UTC"
                st.rerun()

        with col2:
            st.metric(label="Preço (USDT)", value=f"${row['Preço (USDT)']:,.4f}")

        with col3:
            st.metric(
                label="Variação (24h)",
                value=f"{row['Variação % (24h)']:+.2f}%",
                delta=(
                    f"{row['Variação % (24h)']:+.2f}%"
                    if row["Variação % (24h)"] < 0
                    else None
                ),
            )

        st.markdown("---")

        col_max, col_min, col_vol = st.columns(3)
        col_max.markdown(f"**Máxima (24h):**\n${row['Máxima (24h)']:,.4f}")
        col_min.markdown(f"**Mínima (24h):**\n${row['Mínima (24h)']:,.4f}")
        col_vol.markdown(f"**Volume (USDT):**\n${row['Volume (USDT)']:,.2f}")
