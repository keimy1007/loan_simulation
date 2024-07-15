import numpy as np
import pandas as pd

def montly_payment_equal_interest(rate, debt, year, bonus, bonus_number): 
    rate_month = rate / 12.0 / 100
    # return rate_month*np.power(1+rate_month,year*12)/(np.power(1+rate_month, year*12)-1)*debt
    monthly_payment =  rate_month*np.power(1+rate_month,year*12)/(np.power(1+rate_month, year*12)-1)*(debt-bonus)
    #FIXME bonus_number = 1の時にゼロ除算が起きるので回避策を検討する
    if bonus_number <= 0:
        bonus_payment = 0
    else:
        rate_bonus = rate_month * 12 / bonus_number
        bonus_payment =  rate_bonus*np.power(1+rate_bonus,year*bonus_number)/(np.power(1+rate_bonus, year*bonus_number)-1)*bonus
    return monthly_payment, bonus_payment

# 元利均等返済方式のテーブル作成
def make_table_equal_interest(
        debt:int, 
        rate:float|list, 
        year:int, 
        bonus:int, 
        bonus_number:int):

    payment_number = range(year*12) # 返済回数のリスト
    payment_year = [0]*year*12 # 返済年
    payment_principal = [0]*year*12 # 返済のうち元本
    payment_interest = [0]*year*12 # 月ごとの利率
    payment_bonus_principal = [0]*year*12 #ボーナスの金額のうち元本
    payment_bonus_interest = [0]*year*12 #ボーナスの支払いのうち利子分
    monthly_payment, bonus_payment = montly_payment_equal_interest(rate, debt, year, bonus, bonus_number)

    residual_debt = [0] * year * 12 #残債
    residual_debt_bonus = [0] * year * 12
    if type(rate) == float:
        rate = [rate] * year * 12

    for i in range(year*12):

        payment_year[i] = i // 12 + 1
        if i == 0:
            payment_interest[i] = (debt-bonus) * rate[i] / 12 / 100
            payment_principal[i] = monthly_payment - payment_interest[i]
            residual_debt[i] = (debt-bonus) - payment_principal[i]
        else:
            payment_interest[i] = residual_debt[i-1] * rate[i] / 12 / 100
            payment_principal[i] = monthly_payment - payment_interest[i]
            residual_debt[i] = residual_debt[i-1] - payment_principal[i]
        
        # ボーナス支払いの処理
        if bonus_number > 0 and i%(12/bonus_number) == 0:
            if i == 0:
                payment_bonus_interest[i] = bonus * rate[i] / bonus_number / 100
                payment_bonus_principal[i] = bonus_payment - payment_bonus_interest[i]
                residual_debt_bonus[i] = bonus - payment_bonus_principal[i]
            else:
                payment_bonus_interest[i] = residual_debt_bonus[i-1] * rate[i] / bonus_number / 100
                payment_bonus_principal[i] = bonus_payment - payment_bonus_interest[i]
                residual_debt_bonus[i] = residual_debt_bonus[i-1] - payment_bonus_principal[i]
        else:
            residual_debt_bonus[i] = residual_debt_bonus[i-1]

    chart_data_month = pd.DataFrame({
                                'payment_number': payment_number,
                                'payment_year': payment_year,
                                'rate': rate,
                                'monthly_principal': payment_principal, 
                                'monthly_interest': payment_interest,
                                'bonus_principal': payment_bonus_principal,
                                'bonus_interest': payment_bonus_interest,
                                'residual_debt': residual_debt,
                                'residual_debt_bonus': residual_debt_bonus
                                })
    
    return chart_data_month


def make_table_equal_principal(
        debt:int, 
        rate:float|list, 
        year:int, 
        bonus:int, 
        bonus_number:int):
    
    # rate_month_p = rate / 12.0 / 100 #月の利率
    payment_number_p = range(year*12) # 返済回数のリスト
    payment_year_p = [0]*year*12 # 返済年
    payment_principal_p = [0]*year*12 # 返済のうち元本が占める率
    payment_interest_p = [0]*year*12 # 月ごとの利率
    payment_bonus_principal_p = [0]*year*12 #ボーナスの金額のうち元本
    payment_bonus_interest_p = [0]*year*12 #ボーナスの支払いのうち利子分
    residual_debt_p = [0]*year*12 #月ごとの支払い分の残債
    residual_debt_bonus_p = [0]*year*12 #ボーナス分の残債
    montly_principal = (debt - bonus) / year / 12 # 月ごとの元本
    if bonus_number != 0:
        bonus_principal = bonus / year / bonus_number # ボーナスごとの元本
    else:
        bonus_principal = 0

    #年利のリスト処理
    if type(rate) == float:
        rate_p = [rate] * year * 12

    for i in range(year*12):
        payment_year_p[i] = i // 12 + 1
        #元本
        if i == 0:
            payment_principal_p[i] = montly_principal
            payment_interest_p[i] = (debt - bonus)* rate_p[i] / 12 / 100
            residual_debt_p[i] = (debt - bonus) - montly_principal
        else:
            payment_principal_p[i] = montly_principal
            payment_interest_p[i] = residual_debt_p[i-1]* rate_p[i] / 12 / 100
            residual_debt_p[i] = residual_debt_p[i-1] - montly_principal
        #利息
        if bonus_number > 0 and i%(12/bonus_number) == 0:
            if i == 0:
                payment_bonus_principal_p[i] = bonus_principal
                payment_bonus_interest_p[i] = bonus * rate_p[i] / bonus_number / 100
                residual_debt_bonus_p[i] = bonus - bonus_principal
            else:
                payment_bonus_principal_p[i] = bonus_principal
                payment_bonus_interest_p[i] = residual_debt_bonus_p[i-1] * rate_p[i] / bonus_number / 100
                residual_debt_bonus_p[i] = residual_debt_bonus_p[i-1] - bonus_principal     
        else:
            residual_debt_bonus_p[i] = residual_debt_bonus_p[i-1]

    
    chart_data_month_p = pd.DataFrame({
                                'payment_number': payment_number_p,
                                'payment_year': payment_year_p,
                                'rate': rate,
                                'monthly_principal': payment_principal_p, 
                                'monthly_interest': payment_interest_p,
                                'bonus_principal': payment_bonus_principal_p,
                                'bonus_interest': payment_bonus_interest_p,
                                'residual_debt': residual_debt_p,
                                'residual_debt_bonus': residual_debt_bonus_p
                                })
    
    return chart_data_month_p