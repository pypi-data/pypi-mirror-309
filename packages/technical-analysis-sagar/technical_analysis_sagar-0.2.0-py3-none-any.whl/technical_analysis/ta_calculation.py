import ta.wrapper
import yfinance as yf
import pandas as pd
import numpy as np
import ta
from ta.momentum import WilliamsRIndicator, UltimateOscillator, RSIIndicator, AwesomeOscillatorIndicator
from ta.trend import EMAIndicator, IchimokuIndicator
#import technical 
from .technicals import Compute

def calculation(symbol, interval):
    # Fetch historical data for a symbol (e.g., 'AAPL')
    try:
        data = yf.download(symbol, period="2y", interval=interval)
    except Exception as e:
        return {"error": "Invalid symbol or interval"}
    # Ensure data is correctly formatted for indicator calculations
    data = data.dropna()  # Drop any missing values for accuracy
    # Initialize an empty DataFrame to store indicator values
    indicators = pd.DataFrame(index=data.index)
    #Reverrse the data
    Oscillators = {}
    # Ensure columns are 1D (squeeze any 2D data that might be passed)
    close = data["Close"].squeeze()  # Ensures that it's 1D
    high = data["High"].squeeze()  # Ensures that it's 1D
    low = data["Low"].squeeze()  # Ensures that it's 1D
    volume = data["Volume"].squeeze()  # Ensures that it's 1D

    # Calculate RSI (Relative Strength Index)
    indicators["RSI"] = RSIIndicator(close).rsi()
    current_indicators = indicators.iloc[-1]
    Oscillators["RSI"] = current_indicators["RSI"]
    Oscillators["RSI1"] = indicators["RSI"].iloc[-2]

    # Calculate Stoch.K and Stoch.D and Stoch.K[1] and Stoch.D[1]
    highest_high = high.rolling(window=14).max()
    lowest_low = low.rolling(window=14).min()
    stochastic_k = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    stochastic_k = stochastic_k.rolling(window=3).mean()
    stochastic_d = stochastic_k.rolling(window=3).mean()
    Oscillators["Stoch.K"] = stochastic_k.iloc[-1]
    #Stock d caluclated above
    Oscillators["Stoch.D"] = stochastic_d.iloc[-1]
    stochastic_k1 = stochastic_k.shift(1)
    Oscillators["Stoch.K1"] = stochastic_k.rolling(window=3).mean().iloc[-1]
    Oscillators["Stoch.D1"] = stochastic_d.rolling(window=3).mean().iloc[-1]


    #Calculate CCI20 and CCI201
    indicators["CCI20"] = ta.trend.CCIIndicator(high, low, close, window=20).cci()
    current_indicators = indicators.iloc[-1]
    Oscillators["CCI20"] = current_indicators["CCI20"]
    indicators["CCI201"] = indicators["CCI20"].shift(1)
    Oscillators["CCI201"] = indicators["CCI201"].iloc[-1]

    # Calculate ADX
    adx = ta.trend.ADXIndicator(high, low, close)
    indicators["ADX"] = adx.adx()
    current_indicators = indicators.iloc[-1]
    Oscillators["ADX"] = current_indicators["ADX"]
    Oscillators["ADX+DI"] = adx.adx_pos().iloc[-1]
    Oscillators["ADX-DI"] = adx.adx_neg().iloc[-1]
    Oscillators["ADX+DI1"] = adx.adx_pos().shift(1).iloc[-1]
    Oscillators["ADX-DI1"] = adx.adx_neg().shift(1).iloc[-1]

    # Calculate AO (Awesome Oscillator) 
    indicators["AO"] = AwesomeOscillatorIndicator(high, low).awesome_oscillator()
    current_indicators = indicators.iloc[-1]
    Oscillators["AO"] = current_indicators["AO"]
    Oscillators["AO1"] = indicators["AO"].shift(1).iloc[-1]
    Oscillators["AO2"] = indicators["AO"].shift(2).iloc[-1]

    # Calculate Mom (Momentum) 
    Oscillators["Mom"] = close.iloc[-1] - close.iloc[-11]
    Oscillators["Mom1"] = close.iloc[-2] - close.iloc[-12]

    # Calculate MACD.macd
    macd = ta.trend.MACD(close)
    indicators["MACD.macd"] = macd.macd()
    current_indicators = indicators.iloc[-1]
    Oscillators["MACD.macd"] = current_indicators["MACD.macd"]
    Oscillators["MACD.signal"] = macd.macd_signal().iloc[-1]

    #Calculate Stoch.RSI.K
    rsi = RSIIndicator(close).rsi()
    lowest_rsi = rsi.rolling(window=14).min()
    highest_rsi = rsi.rolling(window=14).max()

    stoch_rsi = ((rsi - lowest_rsi) / (highest_rsi - lowest_rsi)) * 100
    stoch_rsi = stoch_rsi.rolling(window=3).mean()
    Oscillators["Stoch.RSI.K"] = stoch_rsi.iloc[-1]

    # Calculate Rec.WR and W.R
    wr = WilliamsRIndicator(high, low, close)
    indicators["W.R"] = wr.williams_r()
    current_indicators = indicators.iloc[-1]
    Oscillators["W.R"] = current_indicators["W.R"]#

    ## Calculate Bull Power and Bear Power
    ema_13 = EMAIndicator(close, window=13).ema_indicator()
    bull_power = high - ema_13
    bear_power = low - ema_13
    Oscillators["BBPower"] = (bull_power.iloc[-1]) + (bear_power.iloc[-1])

    # Calulate UO
    uo = UltimateOscillator(high, low, close)
    indicators["UO"] = uo.ultimate_oscillator()
    current_indicators = indicators.iloc[-1]
    Oscillators["UO"] = current_indicators["UO"]

    moving_average = {}
    # Calculate SMA 10 to 200 and EMA 10 to 200

    moving_average["SMA10"] = close.rolling(window=10).mean().iloc[-1]
    moving_average["SMA20"] = close.rolling(window=20).mean().iloc[-1]
    moving_average["SMA30"] = close.rolling(window=30).mean().iloc[-1]
    moving_average["SMA50"] = close.rolling(window=50).mean().iloc[-1]
    moving_average["SMA100"] = close.rolling(window=100).mean().iloc[-1]
    moving_average["SMA200"] = close.rolling(window=200).mean().iloc[-1]

    moving_average["EMA10"] = close.ewm(span=10, adjust=False).mean().iloc[-1]
    moving_average["EMA20"] = close.ewm(span=20, adjust=False).mean().iloc[-1]
    moving_average["EMA30"] = close.ewm(span=30, adjust=False).mean().iloc[-1]
    moving_average["EMA50"] = close.ewm(span=50, adjust=False).mean().iloc[-1]
    moving_average["EMA100"] = close.ewm(span=100, adjust=False).mean().iloc[-1]
    moving_average["EMA200"] = close.ewm(span=200, adjust=False).mean().iloc[-1]

    #Calculate Ichimoku.BLine
    moving_average["Ichimoku.BLine"] = IchimokuIndicator(high, low).ichimoku_base_line().iloc[-1]

    #Calculate VWMA value custom formula
    weighted_price = close * volume
    vwma = weighted_price.rolling(window=20).sum() / volume.rolling(window=20).sum()
    moving_average["VWMA"] = vwma.iloc[-1]

    # Assume 'close' is a pandas Series with closing prices
    # Calculate Weighted Moving Averages (WMA)
    weights_4 = np.arange(1, 5)  # Weights for period = 4 (n/2)
    weights_9 = np.arange(1, 10)  # Weights for period = 9 (n)
    weights_3 = np.arange(1, 4)  # Weights for period = 3 (sqrt(n))

    # Step 1: WMA for half the period (9/2 = 4.5, approximate to 4)
    wma_half = close.rolling(window=4).apply(lambda x: np.dot(x, weights_4) / weights_4.sum(), raw=True)

    # Step 2: WMA for the full period (9)
    wma_full = close.rolling(window=9).apply(lambda x: np.dot(x, weights_9) / weights_9.sum(), raw=True)

    # Step 3: Double the WMA_half and subtract WMA_full
    wma_diff = 2 * wma_half - wma_full

    # Step 4: WMA of the difference using sqrt(9) = 3
    hma_9 = wma_diff.rolling(window=3).apply(lambda x: np.dot(x, weights_3) / weights_3.sum(), raw=True)

    # Assign the result to a DataFrame or Series
    close_data = pd.DataFrame(close, columns=["Close"])
    close_data["HullMA9"] = hma_9

    # Fetch the latest HMA9 value
    latest_hma9 = close_data["HullMA9"].iloc[-1]
    moving_average["HullMA9"] = latest_hma9

    osc = []
    ans = Compute.RSI_CALCULATION(Oscillators["RSI"], Oscillators["RSI1"])
    osc.append({"rsi":{"value": Oscillators["RSI"], "signal": ans}})
    ans = Compute.Stoch_CALCULATION(Oscillators["Stoch.K"], Oscillators["Stoch.D"], Oscillators["Stoch.K1"], Oscillators["Stoch.D1"])
    osc.append({"stochk":{"value": Oscillators["Stoch.K"], "signal": ans}})
    ans = Compute.CCI20_CALCULATION(Oscillators["CCI20"], Oscillators["CCI201"])
    osc.append({"cci":{"value": Oscillators["CCI20"], "signal": ans}})
    ans = Compute.ADX_CALCULATION(Oscillators["ADX"], Oscillators["ADX+DI"], Oscillators["ADX-DI"], Oscillators["ADX+DI1"], Oscillators["ADX-DI1"])
    osc.append({"adx":{"value": Oscillators["ADX"], "signal": ans}})
    ans = Compute.AO_CALCULATION(Oscillators["AO"], Oscillators["AO1"], Oscillators["AO2"])
    osc.append({"ao":{"value": Oscillators["AO"], "signal": ans}})
    ans = Compute.Mom_CALCULATION(Oscillators["Mom"], Oscillators["Mom1"])
    osc.append({"mom":{"value": Oscillators["Mom"], "signal": ans}})
    ans = Compute.MACD_CALCULATION(Oscillators["MACD.macd"], Oscillators["MACD.signal"])
    osc.append({"macd":{"value": Oscillators["MACD.macd"], "signal": ans}})
    ans = Compute.Default_CALCULATION(Oscillators["Stoch.RSI.K"])
    osc.append({"stochrsi":{"value": Oscillators["Stoch.RSI.K"], "signal": ans}})
    ans = Compute.Default_CALCULATION(Oscillators["W.R"])
    osc.append({"wr":{"value": Oscillators["W.R"], "signal": ans}})
    ans = Compute.Default_CALCULATION(Oscillators["BBPower"])
    osc.append({"bbpower":{"value": Oscillators["BBPower"], "signal": ans}})
    ans = Compute.Default_CALCULATION(Oscillators["UO"])
    osc.append({"uo":{"value": Oscillators["UO"], "signal": ans}})
    #Only 1 to 10
    ma = []
    ans= Compute.MA_CALCULATION(moving_average["SMA10"],close.iloc[-1])
    ma.append({"sma10":{"value": moving_average["SMA10"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["SMA20"],close.iloc[-1])
    ma.append({"sma20":{"value": moving_average["SMA20"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["SMA30"],close.iloc[-1])
    ma.append({"sma30":{"value": moving_average["SMA30"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["SMA50"],close.iloc[-1])
    ma.append({"sma50":{"value": moving_average["SMA50"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["SMA100"],close.iloc[-1])
    ma.append({"sma100":{"value": moving_average["SMA100"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["SMA200"],close.iloc[-1])
    ma.append({"sma200":{"value": moving_average["SMA200"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["EMA10"],close.iloc[-1])
    ma.append({"ema10":{"value": moving_average["EMA10"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["EMA20"],close.iloc[-1])
    ma.append({"ema20":{"value": moving_average["EMA20"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["EMA30"],close.iloc[-1])
    ma.append({"ema30":{"value": moving_average["EMA30"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["EMA50"],close.iloc[-1])
    ma.append({"ema50":{"value": moving_average["EMA50"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["EMA100"],close.iloc[-1])
    ma.append({"ema100":{"value": moving_average["EMA100"], "signal": ans}})
    ans= Compute.MA_CALCULATION(moving_average["EMA200"],close.iloc[-1])
    ma.append({"ema200":{"value": moving_average["EMA200"], "signal": ans}})
    ans= Compute.Default_CALCULATION(moving_average["Ichimoku.BLine"])
    ma.append({"ichimoku":{"value": moving_average["Ichimoku.BLine"], "signal": ans}})
    ans= Compute.Default_CALCULATION(moving_average["VWMA"])
    ma.append({"vwma":{"value": moving_average["VWMA"], "signal": ans}})
    ans= Compute.Default_CALCULATION(moving_average["HullMA9"])
    ma.append({"hullma9":{"value": moving_average["HullMA9"], "signal": ans}})

    #Recommendation
    buy = 0
    sell = 0
    neutral = 0
    for i in ma:
        for key, value in i.items():
            if value["signal"] == "BUY":
                buy += 1
            elif value["signal"] == "SELL":
                sell += 1
            else:
                neutral += 1

    for i in osc:
        for key, value in i.items():
            if value["signal"] == "BUY":
                buy += 1
            elif value["signal"] == "SELL":
                sell += 1
            else:
                neutral += 1

    return {"oscillators": osc, "moving_averages": ma, "recommendation": {"buy": buy, "sell": sell, "neutral": neutral}}
