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

# --- New function adapted from fetch_airtable_data ---
def fetch_all_image_urls(table):
    """
    Fetches all records from an Airtable table and extracts all image URLs 
    from 'Attachments' fields.

    Args:
        table: An Airtable table object.

    Returns:
        A list of all found image URL strings.
    
    Raises:
        ValueError: If the table object is invalid or data fetching fails.
    """
    if not table:
        raise ValueError("Invalid table object provided for fetching image URLs.")
    
    all_image_urls = []
    try:
        raw_records = table.get_all()
        for record in raw_records:
            fields = record.get('fields', {})
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
                            all_image_urls.append(actual_url_str)
        
        return all_image_urls
    except Exception as e:
        raise ValueError(f"Error fetching or processing image URLs from Airtable: {e}")

# --- Main Streamlit Application UI ---
def main_app():
    """
    Main function to run the Imaj Streamlit application.
    Connects to Airtable, fetches all image URLs, and displays them.
    """
    st.set_page_config(page_title="Imaj - Airtable Image Gallery", layout="wide")
    st.title("🖼️ Imaj - Airtable Image Gallery")

    try:
        st.write("Connecting to Airtable...")
        airtable_instance = connect_to_airtable(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
        st.success(f"Successfully connected to Airtable base '{AIRTABLE_BASE_ID}', table '{AIRTABLE_TABLE_NAME}'.")
        
        st.write("Fetching all image URLs from the 'Attachments' field...")
        image_urls = fetch_all_image_urls(airtable_instance)
        
        if image_urls:
            st.success(f"Found {len(image_urls)} image(s). Displaying gallery:")
            # Display images in columns for a gallery-like layout
            # Adjust the number of columns as desired
            num_columns = 4 
            cols = st.columns(num_columns)
            for i, url in enumerate(image_urls):
                with cols[i % num_columns]:
                    st.image(url, caption=f"Image {i+1}", use_column_width='always') # 'always' is better for responsive columns
        else:
            st.info("No images found in the 'Attachments' column of your Airtable table, or none of the attachments were valid image types with URLs.")

    except ValueError as ve:
        st.error(f"Application Error: {ve}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main_app()
