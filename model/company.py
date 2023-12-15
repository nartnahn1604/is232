from .config import db
import pandas as pd

company_coll = db.profile
subsidiaries_coll = db.subsidiaries
officers_coll = db.officers
holders_coll = db.holders
report_bs_coll = db.report_bs
report_is_coll = db.report_is
report_full_coll = db.report_full
indicator_coll = db.indicators

def get_profile_by_symbol(symbol):
    data = company_coll.find_one({"symbol": symbol})
    
    return data

def get_subsidiaries_by_symbol(symbol):
    data = subsidiaries_coll.find_one({"symbol": symbol})

    return data

def get_officers_by_symbol(symbol):
    data = officers_coll.find_one({"symbol": symbol})

    return data

def get_holders_by_symbol(symbol):
    data = holders_coll.find_one({"symbol": symbol})

    return data

def get_indicator_by_symbol(symbol):
    data = indicator_coll.find_one({"symbol": symbol})

    return data

def get_report_bs_by_symbol(symbol):
    data = report_bs_coll.find_one({"symbol": symbol})

    return data

def get_report_is_by_symbol(symbol):
    data = report_is_coll.find_one({"symbol": symbol})

    return data

def get_report_full_by_symbol(symbol):
    data = report_full_coll.find_one({"symbol": symbol})

    return data