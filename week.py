import pandas as pd
import numpy as np
import streamlit as st
import duckdb
from datetime import datetime, timedelta

# Load the CSV file
file1 = pd.read_csv(r"C:\Users\Star\Automate tasks samples\jirasample.csv")
file1['Created'] = pd.to_datetime(file1['Created'])

# Streamlit application title
st.title("JIRA Ticket Statistics")

# Date range selection
st.header("Select Date Range for Created Field")
start_date = st.date_input("Start date", value=datetime.today() - timedelta(days=30))
end_date = st.date_input("End date", value=datetime.today())

# Query to filter all fields based on the selected date range
requiredfield = duckdb.query(f"""
    SELECT Issuekey, Summary, Status, Reporter, Creator, Created 
    FROM file1 
    WHERE Created BETWEEN '{start_date}' AND '{end_date}'
""").df()

# Check if the DataFrame is empty
if requiredfield.empty:
    st.write("No tickets found for the selected date range.")
else:
    # Display the filtered data
    st.write(f"Report for the period: {start_date} to {end_date}")


    # Function to highlight status in the DataFrame
    def highlight_status(s):
        return [
            'background-color: green' if v == 'Closed' else
            'background-color: red' if v == 'L1 Assigned' else
            '' for v in s
        ]


    # Apply the highlighting to the DataFrame
    styled_df = requiredfield.style.apply(highlight_status, subset=['Status'])
    st.dataframe(styled_df)

    # Statistics calculation
    TicketCount = duckdb.query("SELECT count(*) as TotalIncidentsLogged FROM requiredfield").df()
    total_incidents_logged = int(TicketCount['TotalIncidentsLogged'].iloc[0])

    ResolvedIncidents = duckdb.query(
        "SELECT count(Status) as ResolvedIncidents FROM requiredfield WHERE Status='Closed'").df()
    ResolvedIncidents = int(ResolvedIncidents['ResolvedIncidents'].iloc[0])

    IncidentsunderInvestigation = duckdb.query(
        "SELECT count(Status) as IncidentsunderInvestigation FROM requiredfield WHERE Status='L1 Assigned'").df()
    IncidentsunderInvestigation = int(IncidentsunderInvestigation['IncidentsunderInvestigation'].iloc[0])

    # Calculate the week number based on the start date
    week_number = start_date.isocalendar()[1]

    # Display counts
    st.write(f"Total Incidents Logged: {total_incidents_logged}")
    st.write(f"Resolved Incidents: {ResolvedIncidents}")
    st.write(f"Incidents Under Investigation: {IncidentsunderInvestigation}")

    # Detailed statistics
    Detailedstatistics = f"Week {week_number} SOC Review Report Ticket Status"
    st.write(f"Detailed statistics: {Detailedstatistics}")
    if start_date and end_date:
        start_week = start_date.isocalendar()[1]
        end_week = end_date.isocalendar()[1]

       
