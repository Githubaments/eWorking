import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math
import sys
import os
import requests


st.set_page_config(page_title='eWorking Calculator', page_icon="https://raw.githubusercontent.com/Githubaments/Images/main/favicon.ico")

st.subheader("How to calculate eWorking relief")

expander = st.beta_expander('To calculate your electricity and heat eWorking relief:')
with expander:
    st.markdown("> * multiply your allowable utility bills by the number of eWorking days")
    st.markdown("> * divided by 365")
    st.markdown("> * multiply by 10%")
    st.markdown("To calculate your broadband eWorking cost:")
    st.markdown("> * multiply your bill by the number of eWorking days")
    st.markdown("> * divided by 365")
    st.markdown("> * multiply by 30%")
    st.markdown("If the cost is shared between two or more people, it can be apportioned based on the amount each paid.")


days = st.number_input('Number of days worked at home over the year', min_value=0, value=0, max_value=365, format="%i")
utility = st.number_input('Utility Bill (electricty and heating)', min_value=0.00, value=0.00, max_value=9999.00, format="%f")
bill_freq = st.radio("Bill Frequency", ("Monthly","Bi-Monthly","Annual"), index=1)
bb = st.number_input('Montly Broadband Bill', min_value=0.00, value=0.00, max_value=999.99, format="%f",step=0.01)
household = st.number_input('Number of members in the household', min_value=1, value=1, max_value=99, format="%i")
tax_rate = st.radio("Do you pay tax at the higher rate? (40%)", ("Yes","No"), index=0)

if tax_rate == 'Yes':
    rate = 40
else:
    rate = 20

if bill_freq == 'Monthly':
    utility = utility * 12
elif bill_freq == 'Bi-Monthly':
    utility = utility * 6


days_c = days / 365
bb_c = bb * 0.3 * days_c
utility_c = utility * 0.1 * days_c

employer = days * 3.2
days = float(days)

#d = {'Description': ["" , 2], 'Calculation': ["", ""], 'Amount': [utility, 4]}
d = {'Annual': [utility, bb * 12, bb+utility], 'Deductible': [utility_c, bb_c,utility_c + bb_c]}
df = pd.DataFrame(data=d, index=['Utility Bills', 'Broadband','Total'],
                        columns=['Annual','Deductible'])

st.subheader("Total Household")
st.table(df.style.format('{:7,.2f}'))

if household > 1:
    st.subheader("Per Member of Household")
    df = df / household
    st.table(df.style.format('{:7,.2f}'))

dect = df.at['Total','Deductible']
total = dect * rate / 100


expander_employer = st.beta_expander('Tax relief given through your employer')
with expander_employer:
    st.write("If you are an eWorker, your employer may pay you up to €3.20 per day without deducting:")
    st.markdown("> PAYE")
    st.markdown("> PRSI")
    st.markdown("> USC")
    st.write("This is to cover the additional costs of working from home, such as electricity, heat and broadband.")
    st.write("Your additional costs might be higher than €3.20. Your employer may pay these higher costs. Any amount more than €3.20 per day paid by your employer will be taxed.")
    st.write(f"€3.20 per day you worked at home is worth €{employer}")

expander_you= st.beta_expander('Tax relief claimed by you')
with expander_you:
    st.write("If your employer does not make the payment you can instead claim for allowable costs")
    st.write(f"€{dect:.2f} is allowable costs. As you pay tax at the {rate}% rate you will recieve €{total:.2f} as tax relief.")

expander_claim = st.beta_expander('How to claim')
with expander_claim:
    st.markdown("Complete an Income Tax return at the end of the year, sign into myAccount:")
    st.markdown("> click on ‘Review your tax’ link in PAYE Services")
    st.markdown(">select the Income Tax return for the relevant tax year")
    st.markdown("> in ‘Tax Credits & Reliefs’, select ‘Other PAYE Expenses’")
    st.markdown("> insert the amount of eWorking expense in Amount Claimed.")

