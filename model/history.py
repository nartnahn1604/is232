import json
from .config import db
import pandas as pd

history_coll = db.history

def get_history_by_symbol(symbol):
    data = history_coll.find({"symbol": symbol})
    time = []
    open = []
    high = []
    low = []
    close = []
    for item in data:
        time.append(item["date"])
        open.append(item["priceOpen"])
        high.append(item["priceHigh"])
        low.append(item["priceLow"])
        close.append(item["priceClose"])
    
    d = {
        'time': time,
        'open': open,
        'high': high,
        'low': low,
        'close': close
    }
    df = pd.DataFrame(d)    
    df.to_csv("test.csv", index=False)
    return df

get_history_by_symbol("FPT")