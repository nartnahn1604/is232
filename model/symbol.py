from .config import db

symbol_coll = db.symbols

def get_symbols():
    data = symbol_coll.find()
    symbols = []
    for item in data:
        symbols.append(item["symbol"])
    
    return symbols