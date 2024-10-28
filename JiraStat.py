# run by streamlit (streamlit run JIRATicketStastic.py)
import pandas as pd
import numpy as np
import  streamlit as st
import duckdb
from datetime import datetime, timedelta

file1=pd.read_csv(r"C:\Users\Star\Automate tasks samples\jirasample.csv")
#print(file1)
file1['Created']=pd.to_datetime(file1['Created'])
print(file1)
today = datetime.today()
start_of_week = today - timedelta(days=today.weekday())  # Monday
end_of_week = start_of_week + timedelta(days=6)  # Sunday

#print(file1.info())
#requiredfield=duckdb.query("select Issuekey,Summary , Status ,Reporter,Creator ,Created from file1").df()
#print(requiredfield)
'''requiredfield = duckdb.query("""
    SELECT Issuekey, Summary, Status, Reporter, Creator, Created 
    FROM file1 
    WHERE Created BETWEEN '2023-10-13' AND '2023-10-19'
""").df()'''
# Print the filtered data
requiredfield = duckdb.query("""
    SELECT Issuekey, Summary, Status, Reporter, Creator, Created 
    FROM file1 limit 13 offset 1
""").df()
print(requiredfield)
st.write(f"Report for the week: {start_of_week.date()} to {end_of_week.date()}")

def highlight_status(s):
    return [
        'background-color: green' if v == 'Closed' else
        'background-color: red' if v == 'L1 Assigned' else
        '' for v in s
    ]
styled_df = requiredfield.style.apply(highlight_status, subset=['Status'])


st.dataframe(styled_df)
#JIRA Ticket Statistics

TicketCount=duckdb.query("select count(*) as TotalIncidentsLogged from requiredfield ").df()
total_incidents_logged = int(TicketCount['TotalIncidentsLogged'].iloc[0])

#print(total_incidents_logged)


ResolvedIncidents=duckdb.query("select count(Status)as ResolvedIncidents from requiredfield where Status='Closed'").df()
#print(ResolvedIncidents)
ResolvedIncidents = int(ResolvedIncidents['ResolvedIncidents'].iloc[0])

#print(ResolvedIncidents)
#Total Incidents Logged	13
#Resolved Incidents	11
IncidentsunderInvestigation=duckdb.query("select count(Status) as IncidentsunderInvestigation  from requiredfield where  Status ='L1 Assigned'").df()
IncidentsunderInvestigation=int(IncidentsunderInvestigation['IncidentsunderInvestigation'].iloc[0])
print(IncidentsunderInvestigation)


current_week=42
nextweek=current_week=current_week+1
Detailedstatistics=f"Week {nextweek} SOC Review Report Ticket Status"
#print(Detailedstatistics)
st.title("JIRA Ticket Statistics")

# Display counts
st.write(f"Total Incidents Logged: {total_incidents_logged}")
st.write(f"Resolved Incidents: {ResolvedIncidents}")
st.write(f"Incidents Under Investigation: {IncidentsunderInvestigation}")
st.write(f"Detailed statics :{Detailedstatistics}")





