import pandas as pd
import streamlit as st
import duckdb
from datetime import datetime, timedelta

# Load data from the specified sheet
certin = pd.read_excel('threat.xlsx', sheet_name='CERT-In Updates')
#threat=pd.read_excel('threat.xlsx',sheet_name='Threat Intel Feeds')
# Convert 'Date' column to datetime
certin['Date'] = pd.to_datetime(certin['Date'])

# Streamlit app title
st.title("CERT-In Details")

# Date range selection
st.header("Select Date Range for Created Field")
start_date = st.date_input("Start date", value=datetime.today() - timedelta(days=30))
end_date = st.date_input("End date", value=datetime.today())

# Convert dates to string format for DuckDB query
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Filter the data using DuckDB
require = duckdb.query(f"""
    SELECT * FROM certin ,
    WHERE Date BETWEEN '{start_date_str}' AND '{end_date_str}'
""").df()


#require1=duckdb.query()

# Calculate advisory count

# Display advisory count
#st.write(f"Advisory Count: {Advisorycount['AdvisoryCount'].iloc[0]}")

# Display filtered data
if require.empty:
    st.write("No data found for the selected date range.")
else:
    st.write(require)

Advisorycount = duckdb.query("SELECT count(*) as AdvisoryCount FROM require").df()
Advisorycount = int(Advisorycount['AdvisoryCount'].iloc[0])

Applicableadvisory = duckdb.query("""
    SELECT count(*) as applicable_advisory 
    FROM require 
    WHERE "Applicable to Our environment" IN ('Yes', 'YES')
""").df()
Applicableadvisory=int(Applicableadvisory['applicable_advisory'].iloc[0])

#print(Applicableadvisory)
# threat Platform
'''threat=pd.read_excel('threat.xlsx',sheet_name='Threat Intel Feeds')
threat['Date']=pd.to_datetime(threat['Date'])
if threat['Date'].isnull().any():
    st.warning("Some date entries could not be parsed and will be ignored.")

st.title("Threat details Details")
require1 = duckdb.query(f"""
    SELECT * FROM threat ,
    WHERE Date BETWEEN '{start_date_str}' AND '{end_date_str}'
""").df()
if require1.empty:
    st.write("No data found for the selected date range.")
else:
    st.write(require1)

Advisorycount1 = duckdb.query("SELECT count(*) as AdvisoryCount FROM require1").df()
Advisorycount1 = int(Advisorycount['AdvisoryCount'].iloc[0])

Applicableadvisory1 = duckdb.query("""
    SELECT count(*) as applicable_advisory 
    FROM require1 
    WHERE "Applicable to Our environment" IN ('Yes', 'YES')
""").df()
Applicableadvisory1=int(Applicableadvisory1['applicable_advisory'].iloc[0])

'''


# cves


cves=pd.read_excel('threat.xlsx',sheet_name='CVEs')
cves['Date']=pd.to_datetime(cves['Date'])

require3 = duckdb.query(f"""
    SELECT * FROM cves ,
    WHERE Date BETWEEN '{start_date_str}' AND '{end_date_str}'
""").df()
if require3.empty:
    st.write("No data found for the selected date range.")
else:
    st.write(require3)

Advisorycount3 = duckdb.query("SELECT count(*) as AdvisoryCount FROM require3").df()
Advisorycount3 = int(Advisorycount3['AdvisoryCount'].iloc[0])

Applicableadvisory3 = duckdb.query("""
    SELECT count(*) as applicable_advisory 
    FROM require3 
    WHERE "Applicable to Our environment" IN ('Yes', 'YES')
""").df()
Applicableadvisory3=int(Applicableadvisory3['applicable_advisory'].iloc[0])






st.subheader(f"  Cert-IN Advisory Count : {Advisorycount}")
st.subheader(f" Cert-IN Applicable advisory : {Applicableadvisory}")
st.subheader(f" cves Advisory Count:{Applicableadvisory3}")
st.subheader(f" cves  Applicable advisory : {Advisorycount3}")

