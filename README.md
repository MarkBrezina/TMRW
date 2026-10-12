
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
