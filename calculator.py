import numpy as np
import pandas as pd

def montly_payment_equal_interest(rate, debt, year, bonus, bonus_number): 
    rate_month = rate / 12.0 / 100
    monthly_payment =  rate_month*np.power(1+rate_month,year*12)/(np.power(1+rate_month, year*12)-1)*(debt-bonus)
    if bonus_number <= 0:
        bonus_payment = 0
    else:
        rate_bonus = rate_month * 12 / bonus_number
        bonus_payment =  rate_bonus*np.power(1+rate_bonus,year*bonus_number)/(np.power(1+rate_bonus, year*bonus_number)-1)*bonus
    return monthly_payment, bonus_payment

def make_table_equal_interest(debt, rate, year, bonus, bonus_number):
    payment_number = range(year*12)
    payment_year = [0]*year*12
    payment_principal = [0]*year*12
    payment_interest = [0]*year*12
    payment_bonus_principal = [0]*year*12
    payment_bonus_interest = [0]*year*12
    monthly_payment, bonus_payment = montly_payment_equal_interest(rate, debt, year, bonus, bonus_number)

    residual_debt = [0] * year * 12
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
        'balance': residual_debt,  # balanceを追加
        'residual_debt_bonus': residual_debt_bonus
    })
    
    return chart_data_month

def make_table_equal_principal(debt, rate, year, bonus, bonus_number):
    payment_number_p = range(year*12)
    payment_year_p = [0]*year*12
    payment_principal_p = [0]*year*12
    payment_interest_p = [0]*year*12
    payment_bonus_principal_p = [0]*year*12
    payment_bonus_interest_p = [0]*year*12
    residual_debt_p = [0]*year*12
    residual_debt_bonus_p = [0]*year*12
    montly_principal = (debt - bonus) / year / 12
    if bonus_number != 0:
        bonus_principal = bonus / year / bonus_number
    else:
        bonus_principal = 0

    if type(rate) == float:
        rate_p = [rate] * year * 12

    for i in range(year*12):
        payment_year_p[i] = i // 12 + 1
        if i == 0:
            payment_principal_p[i] = montly_principal
            payment_interest_p[i] = (debt - bonus)* rate_p[i] / 12 / 100
            residual_debt_p[i] = (debt - bonus) - montly_principal
        else:
            payment_principal_p[i] = montly_principal
            payment_interest_p[i] = residual_debt_p[i-1]* rate_p[i] / 12 / 100
            residual_debt_p[i] = residual_debt_p[i-1] - montly_principal

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
        'balance': residual_debt_p,  # balanceを追加
        'residual_debt_bonus': residual_debt_bonus_p
    })
    
    return chart_data_month_p

def calculate_deductions(chart_data, deduction_period, deduction_limit, year):
    total_deduction = 0
    for i in range(1, min(year, deduction_period) + 1):
        remaining_debt = chart_data[chart_data['payment_year'] == i]['balance'].values[-1]
        annual_deduction = min(remaining_debt, deduction_limit) * 0.007
        total_deduction += annual_deduction
    return total_deduction
