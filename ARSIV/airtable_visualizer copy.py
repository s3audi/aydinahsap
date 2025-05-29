import os
from airtable import Airtable
import streamlit as st
import pandas as pd

def connect_to_airtable(api_key, base_id, table_name):
    """
    Connects to Airtable and returns a table object.

    Args:
        api_key: Your Airtable API key.
        base_id: Your Airtable Base ID.
        table_name: The name of the table to connect to.

    Returns:
        An Airtable table object.
    
    Raises:
        ValueError: If connection to Airtable fails.
    """
    try:
        table = Airtable(base_id, table_name, api_key)
        # Verify the connection by trying to get the first record
        table.get_all(max_records=1) 
        # print(f"Successfully connected to Airtable base '{base_id}', table '{table_name}'.") # Logging for CLI, not needed for Streamlit
        return table
    except Exception as e:
        # print(f"Error connecting to Airtable: {e}") # Logging for CLI
        raise ValueError(f"Error connecting to Airtable: {e}")

def fetch_airtable_data(table):
    """
    Fetches all records from an Airtable table.

    Args:
        table: An Airtable table object.

    Returns:
        A list of dictionaries representing records.
    
    Raises:
        ValueError: If fetching data fails or table object is invalid.
    """
    if not table:
        # print("Error: Invalid table object provided for fetching data.") # Logging for CLI
        raise ValueError("Invalid table object provided for fetching data.")
    try:
        records = table.get_all()
        processed_records = [record['fields'] for record in records if 'fields' in record]
        # print(f"Successfully fetched {len(processed_records)} records.") # Logging for CLI
        return processed_records
    except Exception as e:
        # print(f"Error fetching data from Airtable: {e}") # Logging for CLI
        raise ValueError(f"Error fetching data from Airtable: {e}")

def color_evet_hayir(val):
    if str(val).lower() == "evet":
        return "background-color: #22c55e; color: white;"
    elif str(val).lower() == "hayır" or str(val).lower() == "hayir":
        return "background-color: #ef4444; color: white;"
    return ""

def main_app():
    """
    Main function to run the Streamlit application.
    """
    st.title("Airtable Data Visualizer")

    try:
        # Attempt to retrieve credentials from st.secrets
        api_key = st.secrets["AIRTABLE_API_KEY"]
        base_id = st.secrets["AIRTABLE_BASE_ID"]
        table_name = st.secrets["AIRTABLE_TABLE_NAME"]

        if not all([api_key, base_id, table_name]):
            st.error("Airtable credentials (API Key, Base ID, Table Name) are not fully configured in st.secrets. Please check your .streamlit/secrets.toml file.")
            return

    except KeyError:
        st.error("Airtable credentials not found in st.secrets. Please create or check your .streamlit/secrets.toml file with AIRTABLE_API_KEY, AIRTABLE_BASE_ID, and AIRTABLE_TABLE_NAME.")
        return
    except Exception as e: # Catch any other unexpected errors during secrets access
        st.error(f"An unexpected error occurred while accessing secrets: {e}")
        return

    try:
        st.write("Connecting to Airtable...")
        airtable_instance = connect_to_airtable(api_key, base_id, table_name)
        st.success(f"Successfully connected to Airtable base '{base_id}', table '{table_name}'.")
        
        st.write("Fetching data from Airtable...")
        data = fetch_airtable_data(airtable_instance)
        
        if data:
            st.success(f"Successfully fetched {len(data)} records.")
            df = pd.DataFrame(data)
            # "Evet" ve "Hayır" olan sütunu bul
            evet_hayir_cols = [col for col in df.columns if df[col].astype(str).str.lower().isin(["evet", "hayır", "hayir"]).any()]
            if evet_hayir_cols:
                st.dataframe(df.style.applymap(color_evet_hayir, subset=evet_hayir_cols))
            else:
                st.dataframe(df)
        else:
            st.info("No data found in the table or the 'fields' key was missing in records.")
            st.dataframe([]) # Show an empty dataframe

    except ValueError as ve: # Catch custom ValueErrors from our functions
        st.error(f"An error occurred: {ve}")
    except Exception as e: # Catch any other unexpected errors
        st.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # This part is for running the Streamlit app directly
    # To run: streamlit run airtable_visualizer.py
    # The old CLI example is removed as the primary interface is now Streamlit.
    main_app()
