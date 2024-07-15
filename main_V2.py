# ローンシミュレータ

import streamlit as st
import numpy as np
import pandas as pd
import calculator

st.title('Simulating Loan Repayment')

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# 必要情報(サイドバー)
debt = st.sidebar.slider('借入金(万円)', min_value=100, max_value=15000, step=100, value=11000)
year = 35  # 固定の返済期間
actual_year = st.sidebar.slider('返済期間(年)', min_value=1, max_value=35, step=1, value=10)
rate = st.sidebar.slider('年利(%)', min_value=0.01, max_value=3.00, step=0.01, value=0.38)
deduction_year = st.sidebar.slider('住宅ローン控除期間(年)', min_value=5, max_value=13, step=1, value=13)
deduction_limit = st.sidebar.slider('住宅ローン控除限度額(万円)', min_value=3000, max_value=5000, step=500, value=4500)

# 初回手数料の計算
initial_fee = debt * (0.022) + 200

# 元利均等計算
monthly_payment, _ = calculator.montly_payment_equal_interest(rate, debt, year, 0, 0)
total_repayment = monthly_payment * actual_year * 12 + initial_fee

# 金利0だった場合の計算
minimum_repayment = debt * (actual_year / year)
self_repayment = total_repayment - minimum_repayment

# 住宅ローン控除額
chart_data_month = calculator.make_table_equal_interest(debt, rate, year, 0, 0)
total_deduction = calculator.calculate_deductions(chart_data_month, deduction_year, deduction_limit, actual_year)

# 実質負担総額
total_self_repayment = self_repayment - total_deduction

# 出力
tab1, tab2 = st.tabs(["元利均等", "元本均等"])

with tab1:
    st.write('月の返済は', '%.2f' % monthly_payment, '万円')
    st.write('初回手数料は', '%.2f' % initial_fee, '万円')
    st.write('返済総額は', '%.1f' % total_repayment, '万円')
    st.markdown('<hr style="border:1px solid #007bff">', unsafe_allow_html=True)
    
    st.write('金利＋手数料の負担は', '%.1f' % self_repayment, '万円')
    st.write('住宅ローン控除総額は', '%.1f' % total_deduction, '万円')
    st.write('実質負担総額は', '%.1f' % total_self_repayment, '万円')
    st.markdown('<hr style="border:1px solid #007bff">', unsafe_allow_html=True)

    tab1_1, tab1_2 = st.tabs(["年ごとのグラフ", "月ごとの支払い表"])
    
    with tab1_1:
        st.bar_chart(chart_data_month[['payment_year',
                                        'monthly_principal',
                                        'monthly_interest'
                                        ]]
                     .groupby(['payment_year']).sum())

    with tab1_2:
        csv = convert_df(chart_data_month)
        st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )
        st.table(chart_data_month.style.format("{:.1f}"))

with tab2:
    chart_data_month_p = calculator.make_table_equal_principal(debt, rate, year, 0, 0)
    total_deduction_p = calculator.calculate_deductions(chart_data_month_p, deduction_year, deduction_limit, actual_year)

    # 実質負担総額
    total_self_repayment_p = self_repayment - total_deduction_p
    
    st.write('月の返済は', '%.2f' % monthly_payment, '万円')
    st.write('初回手数料は', '%.2f' % initial_fee, '万円')
    st.write('返済総額は', '%.1f' % total_repayment, '万円')
    st.markdown('<hr style="border:1px solid #007bff">', unsafe_allow_html=True)

    st.write('金利＋手数料の負担は', '%.1f' % self_repayment, '万円')
    st.write('住宅ローン控除総額は', '%.1f' % total_deduction_p, '万円')
    st.write('実質負担総額は', '%.1f' % total_self_repayment_p, '万円')
    st.markdown('<hr style="border:1px solid #007bff">', unsafe_allow_html=True)

    tab2_1, tab2_2 = st.tabs(["年ごとのグラフ", "月ごとの支払い表"])
    
    with tab2_1:
        st.bar_chart(chart_data_month_p[['payment_year',
                                        'monthly_principal',
                                        'monthly_interest'
                                        ]]
                                        .groupby(['payment_year']).sum())
    with tab2_2:   
        csv = convert_df(chart_data_month_p)
        st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv-p'
        )
        st.table(chart_data_month_p.style.format("{:.1f}"))
