from .config import db
import pandas as pd

dividend_coll = db.dividend
dividend_event_coll = db.dividend_event

def get_dividend_event_by_symbol(symbol):
    #event
    data = list(dividend_event_coll.find({"symbol": symbol}, {"_id": 0}))
    df = pd.DataFrame(data, columns=["recordDate", "title", "executionDate"])
    df["recordDate"] = pd.to_datetime(df["recordDate"]).dt.strftime("%d-%m-%Y")
    df["executionDate"] = pd.to_datetime(df["executionDate"]).dt.strftime("%d-%m-%Y")
    df = df.rename(columns={"recordDate": "Ngày ghi nhận", "title": "Sự kiện", "executionDate": "Ngày thực hiện"})
    #chart
    data = list(dividend_coll.find({"symbol": symbol}, {"_id": 0}))

    df1 = pd.DataFrame(data[0]["data"], columns=["year", "stockDividend", "cashDividend"])
    df1 = df1.rename(columns={"year": "Năm", "stockDividend": "Cổ tức bằng CP", "cashDividend": "Cổ tức bằng tiền"})

    result = {
        "event": df,
        "chart": df1
    }

    return result