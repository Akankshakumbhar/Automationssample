import pandas as pd
import streamlit as st
import duckdb
from datetime import datetime, timedelta
certin=pd.read_excel('threat.xlsx',sheet_name='CERT-In Updates')
print(certin.head())
print(certin.nunique())
certin['Date']=pd.to_datetime(certin['Date'])
st.title("certin details")

st.header("Select Date Range for Created Field")
start_date = st.date_input("Start date", value=datetime.today() - timedelta(days=30))
end_date = st.date_input("End date", value=datetime.today())


require=duckdb.query(f"select * from certin where Date BETWEEN '{start_date}' AND '{end_date}'")
Advisorycount=duckdb.query("select count(*) as AdvisoryCount from certin").df()
print(Advisorycount)
st.write(certin)