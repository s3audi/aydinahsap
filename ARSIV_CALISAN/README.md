# Airtable Data Visualizer

This Streamlit application fetches data from an Airtable table and displays it.

## Setup

1.  **Clone the repository.**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Airtable Credentials:**
    Create a file named `.streamlit/secrets.toml` in the project root directory with your Airtable credentials:
    ```toml
    AIRTABLE_API_KEY = "your_airtable_api_key"
    AIRTABLE_BASE_ID = "your_airtable_base_id"
    AIRTABLE_TABLE_NAME = "your_airtable_table_name"
    ```
    Replace the placeholder values with your actual Airtable API key, Base ID, and Table Name.

## Running the Application

1.  Ensure your Airtable credentials are correctly set up in `.streamlit/secrets.toml`.
2.  Run the Streamlit application using the following command:
    ```bash
    streamlit run airtable_visualizer.py
    ```
3.  Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).
