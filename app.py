import datetime
import json
import time
import uuid
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random

from lstm import *
from model.symbol import get_symbols
from model.history import get_history_by_symbol
from model.company import *
from model.dividend import *
from utils import *

#region Style
st.markdown("""
        <style>
          .circle-image {
              width: 50%;
              border-radius: 50%;
              overflow: hidden;
              box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
              margin: 4px;
              float:right;
          }
          
          .circle-image-holder {
              width: 50%;
              border-radius: 50%;
              overflow: hidden;
              box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
              margin: 4px;
          }
          
          .circle-image img, .circle-image-holder img{
              width: 100%;
              height: 100%;
              object-fit: cover;
          }
        </style>
        """, unsafe_allow_html=True)
#endregion

st.title("Financial App")
img_url = "https://static.fireant.vn/individuals/photo/{}?width=75&height=75"
team_data = {
    "Họ và tên": ["Trần Văn Nhân", "Nguyễn Quốc Vinh", "Hồ Mạnh Tiến"],
    "MSSV": ["20520672", "20522160", "20520317"]
}
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

if "forcast_data" not in st.session_state:
    st.session_state["forcast_data"] = None

def home():
    st.session_state["page"] = "Home"
def selected():
    st.session_state["page"] = "chart"

def show_chart(symbol):
    data = get_history_by_symbol(symbol)
    st.session_state["forcast_data"] = None
    st.session_state["data"] = data
    st.session_state["page"] = "chart"

def show_profile(symbol):
    data = get_profile_by_symbol(symbol)
    st.session_state["page"] = "profile"
    st.session_state["data"] = data

def show_cv(symbol):
    officers = get_officers_by_symbol(symbol)
    subsidiaries = get_subsidiaries_by_symbol(symbol)

    data = {
        "officers": officers,
        "subsidiaries": subsidiaries
    }
    st.session_state["page"] = "cv"
    st.session_state["data"] = data

def show_shareholders(symbol):
    data = get_holders_by_symbol(symbol)
    st.session_state["page"] = "holder"
    st.session_state["data"] = data

def show_dividend(symbol):
    data = get_dividend_event_by_symbol(symbol)
    st.session_state["page"] = "dividend"
    st.session_state["data"] = data

def show_finance_metrics(symbol):
    data = get_metric_by_symbol(symbol)
    st.session_state["page"] = "metrics"
    st.session_state["data"] = data

def show_finance_report(symbol):
    data = get_report_full_by_symbol(symbol)
    st.session_state["page"] = "report"
    st.session_state["data"] = data

def get_forecast(data, next_date):
    forcast_data = forcast(data=data, next_date=next_date)
    st.session_state["forcast_data"] = forcast_data

def pre_q(max_len, ss_key):
    current_quarter = st.session_state[ss_key]
    if current_quarter + 1 < max_len:
        st.session_state[ss_key] = current_quarter + 1

def next_q(ss_key, min_len = 0):
    if st.session_state[ss_key] - 1 >= min_len:
        st.session_state[ss_key] -= 1

with st.sidebar:
    symbol = st.selectbox("Symbol",  get_symbols())
    st.button("Trang chủ", use_container_width=True, on_click=home)
    st.button("Biểu đồ", use_container_width=True, on_click=show_chart, args=[symbol])
    st.button("Thông tin doanh nghiệp", use_container_width=True, on_click=show_profile, args=[symbol])
    st.button("Hồ sơ", use_container_width=True, on_click=show_cv, args=[symbol])
    st.button("Cổ đông", use_container_width=True, on_click=show_shareholders, args=[symbol])
    st.button("Cổ tức", use_container_width=True, on_click=show_dividend, args=[symbol])
    st.button("Chỉ số tài chính", use_container_width=True, on_click=show_finance_metrics, args=[symbol])
    st.button("Báo cáo tài chính", use_container_width=True, on_click=show_finance_report, args=[symbol])

if st.session_state["page"] == "chart":
    data = st.session_state["data"]
    with st.container():
        st.header(symbol)
        fig = go.Figure(data=[go.Candlestick(
                            x=data['time'],
                            open=data['open'],
                            high=data['high'],
                            low=data['low'],
                            close=data['close']
                        )])
        default_xaxis_params = dict(
            title='time',
            range=["2023-01-02", "2023-12-04"]
        )
        fig.update_xaxes(**default_xaxis_params)
        fig.update_layout(height=800)

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(data=data, width=1000, hide_index=True)
    st.divider()
    st.subheader("Dự báo")
    next_date = int(st.number_input("Số ngày cần dự đoán", value=1, min_value=1, max_value=20))
    st.button("Dự đoán", on_click=get_forecast, args=[data, next_date])
    forcast_data = st.session_state["forcast_data"]
    if forcast_data is not None:
        forcast_data.rename(columns={"mlr": "close"}, inplace=True)
        close = forcast_data["close"]
        close = list(close.values)
        open = [list(data["open"].values)[0]]
        open += [close[i] for i in range(len(close) - 1)]
        high = [i * (1 + random.randint(1, 7)/100) for i in close]
        low = [i * (1 - random.randint(1, 7)/100) for i in close]
        forcast_data["open"] = open
        forcast_data["high"] = high
        forcast_data["low"] = low
        with st.container():
            st.subheader("Dự đoán " + str(next_date) + " tiếp theo")
            fc_fig = go.Figure(data=[go.Candlestick(
                                x=forcast_data["DATE"],
                                open=open,
                                high=high,
                                low=low,
                                close=forcast_data['close']
                            )])
            fc_fig.update_layout(height=800)

            st.plotly_chart(fc_fig, use_container_width=True)
            st.dataframe(data=forcast_data, width=1000, hide_index=True)
        
elif st.session_state["page"] == "profile":
    data = st.session_state["data"]
    st.header("Thông tin cơ bản")
    st.write("Tên công ty: " + data["companyName"])
    st.write("Tên quốc tế: " + data["companyName"])
    st.write("Mã số thuế: " + data["taxIDNumber"])
    st.write("Địa chỉ: " + data["headQuarters"])
    st.write("Số điện thoại: " + data["phone"])
    st.write("Fax: " + data["fax"])
    st.write("Email: " + data["email"])
    st.write("Website: " + data["webAddress"])
    st.write("Ngày thành lập: " + data["establishmentDate"])
    st.write("Niêm yết trên sàn: " + data["exchange"])
    st.write(data["overview"])

    st.header("Lịch sử công ty")
    st.markdown(data["history"], unsafe_allow_html=True)

    st.header("Lĩnh vực kinh doanh")
    st.markdown(data["businessAreas"], unsafe_allow_html=True)
elif st.session_state["page"] == "cv":
    st.header("Hồ sơ công ty")
    st.divider()
    data = st.session_state["data"]
    officers = data["officers"]["officers"]
    subsidiaries = data["subsidiaries"]["subsidiaries"]
    subsidiaries_df = pd.DataFrame.from_records(subsidiaries, columns=["companyName", "companyProfile", "type", "ownership", "charterCapital"])
    subsidiaries_df = subsidiaries_df[subsidiaries_df["ownership"] > 0]
    con_com = subsidiaries_df[subsidiaries_df["type"] == 1]
    subsidiaries_df = subsidiaries_df[subsidiaries_df["type"] == 0]
    subsidiaries_df.drop(["type"], axis='columns', inplace=True)
    con_com.drop(["type"], axis='columns', inplace=True)
    subsidiaries_df["ownership"] = [str(i*100) + "%" for i in subsidiaries_df["ownership"]]
    subsidiaries_df.rename(columns={"companyName":"Tên công ty", "companyProfile": "Mô tả", "ownership":"Cổ phần", "charterCapital": "Vốn điều lệ"}, inplace=True)
    st.subheader("Công ty con")
    st.divider()
    st.dataframe(subsidiaries_df, width=2000, hide_index=True)

    st.subheader("Công ty liên kết")
    con_com.rename(columns={"companyName":"Tên công ty", "companyProfile": "Mô tả", "ownership":"Cổ phần", "charterCapital": "Vốn điều lệ"}, inplace=True)
    st.divider()
    st.dataframe(con_com, width=2000, hide_index=True)

    st.subheader("Ban lãnh đạo")
    st.divider()
    for i in range(len(officers) // 2 if len(officers) % 2 == 0 else len(officers) // 2 + 1):
        col1, col2 = st.columns(2)
        officer1 = officers[i]
        officer2 = officers[i + 1]
        with col1:
            with st.container():
                _col1, _col2 = st.columns(2)
                with _col1:
                    st.markdown(f"""
                            <div class="circle-image">
                                <img src="{img_url.format(officer1["individualID"])}" alt="">
                            </div>
                    """, unsafe_allow_html=True)
                with _col2:
                    st.write(officer1["name"])
                    st.caption(officer1["position"])
        with col2:
            with st.container():
                _col1, _col2 = st.columns(2)
                with _col1:
                    st.markdown(f"""
                            <div class="circle-image">
                                <img src="{img_url.format(officer2["individualID"])}" alt="">
                            </div>
                    """, unsafe_allow_html=True)
                with _col2:
                    st.write(officer2["name"])
                    st.caption(officer2["position"])
elif st.session_state["page"] == "holder":
    data = st.session_state["data"]["holders"]
    st.header("Cổ đông")
    st.divider()
    with st.container():
        cols = st.columns(5)
        with cols[0]:
            st.write("Hình ảnh")
        with cols[1]:
            st.write("Tên")
        with cols[2]:
            st.write("Số CP")
        with cols[3]:
            st.write("Tỷ lệ")
        with cols[4]:
            st.write("Ngày cập nhật")
    st.divider()
    is_org = 0
    is_foreign = 0
    is_founder = 0
    none_above = 0
    for item in data:
        if item["isOrganization"]:
            is_org += item["ownership"]
        if item["isForeigner"]:
            is_foreign += item["ownership"]
        if item["position"] is not None:
            is_founder += item["ownership"]
        if item["isOrganization"] and item["isForeigner"] and item["position"] is None:
            none_above += item["ownership"]
        with st.container():
            cols = st.columns(5)
            with cols[0]:
                if item["isOrganization"]:
                    st.markdown(f"""
                                    <div class="circle-image-holder">
                                        <img src="https://fireant.vn/images/institution.png" style="background: #fff;" alt="">
                                    </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                                    <div class="circle-image-holder">
                                        <img src="{img_url.format(item["individualHolderID"])}" alt="">
                                    </div>
                            """, unsafe_allow_html=True)
            with cols[1]:
                st.write(item["name"])
            with cols[2]:
                st.write(item["shares"])
            with cols[3]:
                st.write(str(round(item["ownership"] * 100, 4))+ "%")
            with cols[4]:
                st.write(datetime.datetime.fromisoformat(item["reported"]).strftime("%d/%m/%Y"))
    
    st.divider()
    st.subheader("Nhóm cổ đông")
    chart_data = [
        ["Tổ chức",round(is_org * 100, 2)],
        ["Thành viên HĐQT", round(is_founder * 100, 2)],
        ["Cá nhân", round(none_above * 100, 2)],
        ["Nước ngoài", round(is_foreign * 100, 2)]
    ]   
    holder_chart = pd.DataFrame.from_records(chart_data, columns=["Thành phần", "Sở hữu (%)"])
    st.dataframe(holder_chart, hide_index=True, use_container_width=True)
    st.bar_chart(holder_chart, x="Thành phần")
elif st.session_state["page"] == "dividend":
    st.subheader("Sự kiện")
    data = st.session_state["data"]
    event = data["event"]
    chart = data["chart"]
    st.dataframe(event, width=2000, hide_index=True)
    st.divider()
    st.subheader("Cổ tức bằng tiền (đ)")
    st.bar_chart(chart, x="Năm", y="Cổ tức bằng tiền", height=500)
    st.subheader("Cổ tức bằng CP (%)")
    st.bar_chart(chart, x="Năm", y="Cổ tức bằng CP", height=500)
    
elif st.session_state["page"] == "metrics":
    data = st.session_state["data"]
    rp_is = data["is"]
    rp_bs = data["bs"]
    indi = data["indicator"]

    st.subheader("Kết quả kinh doanh")
    if rp_is:
        rp_is_quar = len(rp_is["columns"])
        if "is_current_quarter" not in st.session_state:
            st.session_state["is_current_quarter"] = 0
        with st.container():
            cols = st.columns([2, 1, 1, 1, 1])
            with cols[0]:
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    st.button("Trước", key=str(uuid.uuid4()), on_click=pre_q, args=[rp_is_quar - 5, "is_current_quarter"])
                with btn_cols[1]:
                    st.button("Sau", key=str(uuid.uuid4()), on_click=next_q, args=["is_current_quarter"])
            current_q = st.session_state["is_current_quarter"]
            for col in range(4, 0, -1):
                with cols[5 - col]:
                    st.markdown("<h6 style='color:green;'>{}</h6>".format(rp_is["columns"][rp_is_quar - col - current_q]), unsafe_allow_html=True)
        for item in rp_is["rows"]:
            with st.container():
                cols = st.columns([2, 1, 1, 1, 1])
                with cols[0]:
                    st.write(item[0])
                for col in range(4, 0, -1):
                    with cols[5 - col]:
                        value = item[rp_is_quar - col - current_q]
                        # st.write(str(value))
                        if value is not None and value > 0:
                            value /= 1000000
                            value = round(value, 0)
                            value = format_currency(int(value)).replace(".","",1)
                            st.write(value)
                        else:
                            if item["level"] != 1:
                                st.write("0")
    st.divider()
    st.subheader("Cân đối kế toán")
    if rp_bs:
        rp_bs_quar = len(rp_bs["columns"])
        if "bs_current_quarter" not in st.session_state:
            st.session_state["bs_current_quarter"] = 0
        with st.container():
            cols = st.columns([2, 1, 1, 1, 1])
            with cols[0]:
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    st.button("Trước", key=str(uuid.uuid4()), on_click=pre_q, args=[rp_bs_quar - 5, "bs_current_quarter"])
                with btn_cols[1]:
                    st.button("Sau", key=str(uuid.uuid4()), on_click=next_q, args=["bs_current_quarter"])
            current_q = st.session_state["bs_current_quarter"]
            for col in range(4, 0, -1):
                with cols[5 - col]:
                    st.markdown("<h6 style='color:green;'>{}</h6>".format(rp_bs["columns"][rp_bs_quar - col - current_q]), unsafe_allow_html=True)
        for item in rp_bs["rows"]:
            with st.container():
                cols = st.columns([2, 1, 1, 1, 1])
                with cols[0]:
                    st.write(item[0])
                for col in range(4, 0, -1):
                    with cols[5 - col]:
                        value = item[rp_bs_quar - col - current_q]
                        # st.write(str(value))
                        if value is not None and value > 0:
                            value /= 1000000
                            value = round(value, 0)
                            value = format_currency(int(value)).replace(".","",1)
                            st.write(value)
                        else:
                            if item["level"] != 1:
                                st.write("0")
    st.divider()
    st.subheader("Chỉ số tài chính")
    for group in indi:
        with st.expander(group, True):
            for item in indi[group]:
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(item["name"])
                    with col2:
                        st.write(round(item["value"], 2) if item["value"] else 0)
elif st.session_state["page"] == "report":
    data = st.session_state["data"]

    with st.container():
        tabs = st.tabs(["Cân đối kế toán", "Kết quả kinh doanh", "LCTT trực tiếp", "LCTT gián tiếp"])
        for i in range(len(data["data"])):
            with tabs[i]:
                items = data["data"][i]
                quarters = []
                if items:
                    if "current_quarter" not in st.session_state:
                        st.session_state["current_quarter"] = 0
                    for item in items[0]["values"]:
                        quarters.append(item["period"])
                    with st.container():
                        cols = st.columns([3, 1, 1, 1, 1])
                        with cols[0]:
                            btn_cols = st.columns(3)
                            with btn_cols[0]:
                                st.button("Trước", key=str(uuid.uuid4()), on_click=pre_q, args=[len(quarters), "current_quarter"])
                            with btn_cols[1]:
                                st.button("Sau", key=str(uuid.uuid4()), on_click=next_q, args=["current_quarter"])
                            with btn_cols[2]:
                                st.write("ĐVT: 1.000.000")
                        current_q = st.session_state["current_quarter"]
                        for col in range(4, 0, -1):
                            with cols[5 - col]:
                                st.markdown(f"<h6 style='color:green;'>{quarters[len(quarters) - col - current_q]}</h6>", unsafe_allow_html=True)
                    for item in items:
                        if item["level"] == 1:
                            st.divider()
                        with st.container():
                            cols = st.columns([3, 1, 1, 1, 1])
                            with cols[0]:
                                st.markdown(format_lv(item["level"], item["name"]), unsafe_allow_html=True)
                            for col in range(4, 0, -1):
                                with cols[5 - col]:
                                    value = item["values"][len(quarters) - col - current_q]["value"]
                                    if value is not None and value > 0:
                                        value /= 1000000
                                        value = round(value, 0)
                                        value = format_currency(int(value)).replace(".","",1)
                                        st.write(value)
                                    else:
                                        if item["level"] != 1:
                                            st.write("0")
                        # if item["level"] == 1:
                        #     st.divider()
else:
    team = pd.DataFrame(team_data)
    st.dataframe(team, hide_index=True)