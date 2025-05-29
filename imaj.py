import streamlit as st
from airtable import Airtable
import os

# --- Airtable Credentials from Streamlit Secrets ---
try:
    AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
    AIRTABLE_BASE_ID = st.secrets["AIRTABLE_BASE_ID"]
    AIRTABLE_TABLE_NAME = st.secrets["AIRTABLE_TABLE_NAME"]
except KeyError:
    st.error("Airtable credentials (API key, Base ID, Table Name) not found in st.secrets. Please ensure they are configured in .streamlit/secrets.toml.")
    st.stop() # Stop execution if secrets are missing
except Exception as e: # Catch any other unexpected error during secrets access
    st.error(f"An unexpected error occurred while accessing Airtable secrets: {e}")
    st.stop()

# --- Copied from airtable_visualizer.py ---
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
        return table
    except Exception as e:
        raise ValueError(f"Error connecting to Airtable: {e}")

# --- Refactored function to fetch record details including specific fields and one image URL ---
def fetch_record_details(table):
    """
    Fetches records from an Airtable table that have at least one image in 'Attachments',
    and extracts the first image URL along with specified text fields.

    Args:
        table: An Airtable table object.

    Returns:
        A list of dictionaries, where each dictionary contains details for a record:
        {'image_url': str, 'cuz_no': any, 'okunan': any, 'okuyan': any, 'durum': any}.
        Returns an empty list if no records with images are found or in case of error.
    
    Raises:
        ValueError: If the table object is invalid or data fetching fails.
    """
    if not table:
        raise ValueError("Invalid table object provided for fetching record details.")
    
    records_with_details = []
    try:
        raw_records = table.get_all()
        for record in raw_records:
            fields = record.get('fields', {})
            
            # Extract the first image URL
            first_image_url = None
            attachments_field = fields.get('Attachments')
            if attachments_field and isinstance(attachments_field, list):
                for attachment in attachments_field:
                    if isinstance(attachment, dict) and \
                       attachment.get('type', '').startswith('image/'):
                        
                        potential_url_source = attachment.get("url")
                        actual_url_str = None

                        if isinstance(potential_url_source, str) and potential_url_source.strip():
                            actual_url_str = potential_url_source
                        elif isinstance(potential_url_source, dict):
                            if 'full' in potential_url_source and isinstance(potential_url_source['full'], str) and potential_url_source['full'].strip():
                                actual_url_str = potential_url_source['full']
                            elif 'src' in potential_url_source and isinstance(potential_url_source['src'], str) and potential_url_source['src'].strip():
                                actual_url_str = potential_url_source['src']
                        
                        if actual_url_str:
                            first_image_url = actual_url_str
                            break # Found the first image, stop looking for this record
            
            # If no image URL was found for this record, skip it
            if not first_image_url:
                continue
                
            # Extract text fields
            cuz_no = fields.get('Cüz no')
            okunan = fields.get('Okunan')
            okuyan = fields.get('Okuyan')
            durum = fields.get('Durum')
            
            details = {
                'image_url': first_image_url,
                'cuz_no': cuz_no,
                'okunan': okunan,
                'okuyan': okuyan,
                'durum': durum
            }
            records_with_details.append(details)
        
        return records_with_details
    except Exception as e:
        raise ValueError(f"Error fetching or processing record details from Airtable: {e}")

# --- Main Streamlit Application UI ---
def main_app():
    """
    Main function to run the Imaj Streamlit application.
    Connects to Airtable, fetches record details (image and specific fields), and displays them.
    """
    st.set_page_config(page_title="Imaj - Airtable Image Gallery with Details", layout="wide")
    st.title("🖼️ Imaj - Airtable Image Gallery with Details")

    try:
        # The connection and fetching messages can be removed for a cleaner UI once tested
        # st.write("Connecting to Airtable...") 
        airtable_instance = connect_to_airtable(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
        # st.success(f"Successfully connected to Airtable base '{AIRTABLE_BASE_ID}', table '{AIRTABLE_TABLE_NAME}'.")
        
        # st.write("Fetching record details (image and specific fields)...")
        record_details_list = fetch_record_details(airtable_instance)
        
        if record_details_list:
            st.info(f"Found {len(record_details_list)} record(s) with images. Displaying gallery:")
            
            num_columns = 2  # Using 2 columns as requested
            cols = st.columns(num_columns)
            for i, details in enumerate(record_details_list):
                with cols[i % num_columns]:
                    # Prepare caption text, handling None values
                    cuz_no_str = details.get('cuz_no', 'N/A')
                    okunan_str = details.get('okunan', 'N/A')
                    okuyan_str = details.get('okuyan', 'N/A')
                    durum_str = details.get('durum', 'N/A')
                    
                    caption_text = (
                        f"Cüz no: {cuz_no_str} | Okunan: {okunan_str} | "
                        f"Okuyan: {okuyan_str} | Durum: {durum_str}"
                    )
                    
                    st.image(details['image_url'], caption=caption_text, width=500)
                    # The markdown display from previous step is removed as per new caption requirement
        else:
            st.info("No records with images and specified details found.") # Message updated as per requirement

    except ValueError as ve:
        st.error(f"Application Error: {ve}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main_app()
