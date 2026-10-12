
TMRWCAP
Company Setup
asda

Tomorrow Capital Research
Market making
Algorithmic trading - HFT
Algorithmic trading - MFT
Systematic investing - LFT
Tomorrow Archive
Walk-through on topics: Market making, algorithmic trading, derivatives…
Competitions available
Setups
Connections and resources
Hardware setup
Setup for algorithmic trading of 25 assets.
𝗘𝘅𝗲𝗰𝘂𝘁𝗶𝗼𝗻 𝘀𝗲𝘁𝘂𝗽 𝗯𝗮𝘀𝗲𝗹𝗶𝗻𝗲:
• Modern 8-core high-clock CPU
• 32 GB RAM
• 1 TB NVMe SSD
• Integrated graphics / no dedicated GPU
• Minimal Linux installation
• Wired Ethernet
• Good router
• Low-latency VPS where broker proximity requires it \

Download:      ~160 Mbps
Upload:        ~165 Mbps
Idle ping:     4 ms
Download ping: 14 ms
Upload ping:   39 ms
Provider:      Hyperoptic, London
Connection:    Wi-Fi
4ms idle ping is good. 14ms under download is also fine. 39 ms under upload is okay and can be fixed with ethernet

average 11ms

Research station.
Software Setup
Python to do the start setup

C++ for actual setup SQL for database setup

Data access
Data storage
Exchange connections
Data setup
IBKR - FX + Equities + multi-asset

Historical FX data

Kraken, Coinbase, Binance, CCXT, Gemini - Crypto.

minute by minute from Yahoo, 7 past days

import yfinance as yf
import pandas as pd


tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "SPY","EURUSD=X", "GBPUSD=X", "GC=F", "BTC-USD", "ETH-USD", "^GSPC"]

df = yf.download(
    tickers=tickers,
    period="7d",
    interval="1m",
    auto_adjust=False,
    prepost=False,
    group_by="ticker",
    threads=True
)

parquet + zstd/snappy

pandas.to_parquet
format
timestamp        int64/datetime
symbol           category/string
open             float32 or float64
high             float32 or float64
low              float32 or float64
close            float32 or float64
volume           float32/int64
vwap             float32, optional
trade_count      int32, optional
source           string, optional
raw/ vendor original files, untouched

processed/ clean Parquet minute bars

research/ derived features, signals, backtest outputs

SoMe
Linkedin - Mark Brezina
Linkedin - Mark Brezina \

Post schedule

 28/05/26 - I've gotten a job, Recruiters do not contact me.

 29/05/26 - Hardware setup, execution stack, data stack

 03/06/26 - I've gotten a job, Recruiters do not contact me.

 05/06/26 - Hardware setup, execution stack, data stack

[] 07/06/26 - Research TCR

 10/06/26 - I've gotten a job, Recruiters do not contact me.

 12/06/26 - Hardware setup, execution stack, data stack

[] 14/06/26 - Research TCR

 17/06/26 - I've gotten a job, Recruiters do not contact me.

 19/06/26 - Hardware setup, execution stack, data stack

[] 21/06/26 - Research TCR

Linkedin - TCR
Tomorrow Capital Research Linkedin \

Post schedule

[]

[]

[]

[]

[]

[]

[]

Websites. Tomorrow Capital Tomorrow Archive

Finances/accounting
Hardware costs
Data costs
Standard Capital
Profits


```
import yfinance as yf
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/yahoo_minute")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_symbol(symbol: str):
    df = yf.download(
        tickers=symbol,
        period="7d",
        interval="1m",
        auto_adjust=False,
        prepost=False,
        progress=False
    )

    if df.empty:
        print(f"No data for {symbol}")
        return None

    df = df.reset_index()

    # yfinance usually gives Datetime column for intraday
    if "Datetime" in df.columns:
        df = df.rename(columns={"Datetime": "timestamp"})
    elif "Date" in df.columns:
        df = df.rename(columns={"Date": "timestamp"})

    df["symbol"] = symbol
    df["source"] = "yahoo"

    # Standardise column names
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume"
    })

    cols = [
        "timestamp", "symbol", "open", "high", "low",
        "close", "adj_close", "volume", "source"
    ]

    return df[[c for c in cols if c in df.columns]]


symbols = ["AAPL", "MSFT", "NVDA", "TSLA", "SPY","EURUSD=X", "GBPUSD=X", "GC=F", "BTC-USD", "ETH-USD", "^GSPC"]

all_data = []

for symbol in symbols:
    df_symbol = download_symbol(symbol)
    if df_symbol is not None:
        all_data.append(df_symbol)

df_all = pd.concat(all_data, ignore_index=True)

output_path = DATA_DIR / "minute_equities_latest.parquet"

df_all.to_parquet(
    output_path,
    engine="pyarrow",
    compression="zstd",
    index=False
)

print(f"Saved {len(df_all):,} rows to {output_path}")
```


```
import yfinance as yf
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/yahoo_minute")
DATA_DIR.mkdir(parents=True, exist_ok=True)

symbols = ["AAPL", "MSFT", "NVDA", "TSLA", "SPY","EURUSD=X", "GBPUSD=X", "GC=F", "BTC-USD", "ETH-USD", "^GSPC"]

def fetch_1m(symbol: str) -> pd.DataFrame:
    try:
        df = yf.download(
            tickers=symbol,
            period="7d",
            interval="1m",
            auto_adjust=False,
            prepost=False,
            progress=False,
            group_by="column",
            multi_level_index=False,
        )
    except TypeError:
        # Fallback for older yfinance versions
        df = yf.download(
            tickers=symbol,
            period="7d",
            interval="1m",
            auto_adjust=False,
            prepost=False,
            progress=False,
            group_by="column",
        )

    if df is None or df.empty:
        return pd.DataFrame()

    # Handle MultiIndex columns if yfinance still returns them
    if isinstance(df.columns, pd.MultiIndex):
        # Common case: columns are like ("Close", "AAPL")
        if symbol in df.columns.get_level_values(-1):
            df = df.xs(symbol, axis=1, level=-1)

        # Other case: columns are like ("AAPL", "Close")
        elif symbol in df.columns.get_level_values(0):
            df = df[symbol]

        # Fallback: if one column level has only one value, drop it
        else:
            for level in range(df.columns.nlevels):
                if len(df.columns.get_level_values(level).unique()) == 1:
                    df.columns = df.columns.droplevel(level)
                    break

    df = df.reset_index()

    # Standardise column names
    df.columns = [
        str(c).strip().lower().replace(" ", "_")
        for c in df.columns
    ]

    # yfinance usually gives "datetime" for intraday
    rename_map = {
        "datetime": "timestamp",
        "date": "timestamp",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "adj_close": "adj_close",
        "volume": "volume",
    }

    df = df.rename(columns=rename_map)

    if "timestamp" not in df.columns:
        print(f"{symbol}: columns returned were {list(df.columns)}")
        raise KeyError(f"{symbol}: no timestamp column found")

    df["symbol"] = symbol
    df["source"] = "yahoo"

    keep_cols = [
        "timestamp", "symbol", "open", "high", "low",
        "close", "adj_close", "volume", "source"
    ]

    existing_cols = [c for c in keep_cols if c in df.columns]
    df = df[existing_cols]

    return df


def update_symbol(symbol: str):
    path = DATA_DIR / f"{symbol}.parquet"

    new_df = fetch_1m(symbol)

    if new_df.empty:
        print(f"{symbol}: no new data")
        return

    required = {"timestamp", "symbol"}

    if not required.issubset(new_df.columns):
        print(f"{symbol}: bad new dataframe columns: {list(new_df.columns)}")
        return

    if path.exists():
        old_df = pd.read_parquet(path)

        # If an old file was saved in the wrong format, back it up and start clean
        if not required.issubset(old_df.columns):
            backup_path = DATA_DIR / f"{symbol}_bad_backup.parquet"
            path.rename(backup_path)
            print(f"{symbol}: old file had bad columns. Backed up to {backup_path}")
            combined = new_df
        else:
            combined = pd.concat([old_df, new_df], ignore_index=True)
    else:
        combined = new_df

    combined = combined.drop_duplicates(
        subset=["timestamp", "symbol"],
        keep="last"
    )

    combined = combined.sort_values(["symbol", "timestamp"])

    combined.to_parquet(
        path,
        engine="pyarrow",
        compression="zstd",
        index=False
    )

    print(f"{symbol}: saved {len(combined):,} rows to {path}")


for symbol in symbols:
    update_symbol(symbol)

```
