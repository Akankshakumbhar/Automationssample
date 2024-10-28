import pandas as pd
import numpy as np
import streamlit as st
import duckdb
from datetime import datetime, timedelta

# Streamlit application title
st.title("JIRA Ticket Statistics")

# File uploader to allow users to upload a CSV file
uploaded_file = st.file_uploader("Upload your JIRA CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the CSV file
    file1 = pd.read_csv(uploaded_file)
    file1['Created'] = pd.to_datetime(file1['Created'])

    # Check column names
    #st.write("Columns in the uploaded file:", file1.columns)

    # Date range selection
    st.header("Select Date Range for Created Field")
    start_date = st.date_input("Start date", value=datetime.today() - timedelta(days=30))
    end_date = st.date_input("End date", value=datetime.today())

    # Register the DataFrame with DuckDB
    duckdb.sql("CREATE OR REPLACE TABLE file1 AS SELECT * FROM file1")

    # Query to filter all fields based on the selected date range
    requiredfield = duckdb.query(f"""
        SELECT "Issue key", Summary, Status, Reporter, Creator, Created 
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
        start_week_number = start_date.isocalendar()[1]
        end_week_number = end_date.isocalendar()[1]
        year = start_date.isocalendar()[0]

        # Display counts
        st.write(f"Total Incidents Logged: {total_incidents_logged}")
        st.write(f"Resolved Incidents: {ResolvedIncidents}")
        st.write(f"Incidents Under Investigation: {IncidentsunderInvestigation}")

        # Detailed statistics
        if start_week_number == end_week_number:
            Detailedstatistics = f"Week {start_week_number} of {year} SOC Review Report Ticket Status"
        else:
            Detailedstatistics = f"Weeks {start_week_number} to {end_week_number} of {year} SOC Review Report Ticket Status"

        st.write(f"Detailed statistics: {Detailedstatistics}")
