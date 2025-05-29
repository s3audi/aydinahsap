import os
from airtable import Airtable
import streamlit as st

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
        raise ValueError("Invalid table object provided for fetching data.")
    try:
        raw_records = table.get_all()
        processed_records = []
        for record in raw_records:
            if 'fields' not in record:
                continue

            fields = record['fields']
            attachment_url = None  # Default to None

            if "Attachments" in fields and isinstance(fields["Attachments"], list):
                for attachment in fields["Attachments"]:
                    if isinstance(attachment, dict) and \
                       attachment.get("type") and \
                       attachment.get("type").startswith("image/"):
                        
                        potential_url_source = attachment.get("url")
                        actual_url_str = None

                        if isinstance(potential_url_source, str):
                            actual_url_str = potential_url_source
                        elif isinstance(potential_url_source, dict):
                            # Attempt to get URL from a dict structure like {'full': 'url_string'} or common variations
                            # This is based on the prompt's example: "{'full': 'url_string', ...}"
                            # Common keys for URLs in such objects could be 'full', 'src', 'url' itself.
                            # Prioritizing 'full' as per example.
                            if 'full' in potential_url_source and isinstance(potential_url_source['full'], str):
                                actual_url_str = potential_url_source['full']
                            elif 'src' in potential_url_source and isinstance(potential_url_source['src'], str):
                                actual_url_str = potential_url_source['src']
                            # Add more fallbacks if other nested structures are common for Airtable or suspected
                        
                        if actual_url_str:
                            attachment_url = actual_url_str
                            break  # Found the first valid image URL string, stop looking
            
            fields["Attachments"] = attachment_url # Set to URL string or None
            processed_records.append(fields)
            
        # Ensure all records have 'Attachments' key for consistent dataframe columns
        # This might be redundant if all incoming records already have it or if pandas handles it.
        # However, explicit is often better.
        # If 'Attachments' was never present in any record, it won't be added here.
        # This logic assumes 'Attachments' is a field we want to ensure exists if *any* record had it.
        # A more robust way for dataframes is to let pandas handle missing columns or ensure it post-conversion.

        return processed_records
    except Exception as e:
        raise ValueError(f"Error fetching data from Airtable: {e}")

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
            
            # Check if there's any data and if 'Attachments' column could exist
            # For a list of dicts, we check if the first item has 'Attachments' as a key.
            # This is a heuristic; a more robust check would be to convert to DataFrame first
            # or iterate through all dicts to see if 'Attachments' is ever present.
            column_config = {}
            if data and "Attachments" in data[0]: # Check if the key exists in the first record
                column_config["Attachments"] = st.column_config.ImageColumn(
                    "Attachments", help="Shows the first image from attachments"
                )
            
            st.dataframe(data, column_config=column_config if column_config else None)

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
