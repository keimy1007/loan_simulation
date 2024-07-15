"""
# ローンシミュレータ
"""

import streamlit as st
import numpy as np
import pandas as pd
import calculator

st.title('ローン返済シミュレータ')

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

# 必要情報(サイドバー)
debt = st.sidebar.slider('借入金(万円)', min_value=50, max_value=10000, step=50)
bonus = st.sidebar.slider('ボーナス分(万円)', min_value=0, max_value=10000) # TODO 借入金を超えないようにするにはどうするか検討
bonus_number = st.sidebar.slider('ボーナスの支払回数(/年)', min_value=0, max_value=4)# TODO ゼロ除算を防ぐにはどうすべきか検討
year = st.sidebar.slider('返済期間(年)', min_value=1, max_value=60, step=1)
rate = st.sidebar.slider('年利(%)', min_value=0.01, max_value=10.000,step = 0.01)

# 記入チェック
if bonus > 0 and bonus_number == 0:
    st.warning('ボーナス支払い回数が0回ですがボーナス支払いが存在します。')
if debt < bonus:
    st.warning('ボーナス支払いが借入金を超えています。')

# 出力
tab1, tab2 = st.tabs(["元利均等", "元本均等"])

with tab1:
    monthly_payment, bonus_payment = calculator.montly_payment_equal_interest(rate,debt, year, bonus, bonus_number)
    st.write('月の返済は', '%.2f' % monthly_payment, '万円')
    st.write('ボーナスごとに', '%.2f' % bonus_payment, '万円')
    st.write('返済総額は', '%.1f' % (monthly_payment*year*12 + bonus_payment * year * bonus_number) ,'万円')

    chart_data_month = calculator.make_table_equal_interest(debt, rate, year, bonus, bonus_number)

    # TODO 月ごとの支払い表を別タブで作成するようにする。
    tab1_1, tab1_2 = st.tabs(["年ごとのグラフ", "月ごとの支払い表"])
    
    with tab1_1:
        st.bar_chart(chart_data_month[['payment_year',
                                        'monthly_principal',
                                        'monthly_interest',
                                        'bonus_principal',
                                        'bonus_interest'
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

    chart_data_month_p = calculator.make_table_equal_principal(debt, rate, year, bonus, bonus_number)
    
    tab2_1, tab2_2 = st.tabs(["年ごとのグラフ", "月ごとの支払い表"])
    with tab2_1:
        st.bar_chart(chart_data_month_p[['payment_year',
                                        'monthly_principal',
                                        'monthly_interest',
                                        'bonus_principal',
                                        'bonus_interest'
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
