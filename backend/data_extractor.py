# data_extractor.py (FINAL STABLE VERSION)

import logging
import json # Import the json library
from typing import List, Dict, Any

import pandas as pd
# 'requests' and 'time' are no longer needed for fetching but might be for future use

# --- Configuration (Based on known valid data structure) ---
FIELD_MAPPING = {
    "bld_sq_ft": "square_footage",
    "pin": "property_identification_number",
    "latitude": "latitude",
    "longitude": "longitude",
    "age": "age",
    "class": "zoning_code"
}
REQUIRED_FIELDS = ["square_footage", "latitude", "longitude", "year_built", "zoning_code"]

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(module)s] - %(message)s',
    handlers=[
        logging.FileHandler("data_extraction.log"),
        logging.StreamHandler()
    ]
)

def _fetch_cook_county_data() -> List[Dict[str, Any]]:
    """
    Simulates an API call by reading from a local JSON file.
    This ensures the application is stable and decoupled from the unreliable external API.
    """
    local_filename = "cook_county_sample.json"
    logging.info(f"API is unstable. Reading from local file: '{local_filename}'")
    try:
        with open(local_filename, 'r') as f:
            data = json.load(f)
        logging.info(f"Successfully loaded {len(data)} records from local file.")
        return data
    except FileNotFoundError:
        logging.error(f"FATAL: Local data file not found: '{local_filename}'. Please create it.")
        return []
    except json.JSONDecodeError:
        logging.error(f"FATAL: Could not parse JSON from '{local_filename}'. Check for syntax errors.")
        return []

def _process_and_validate_data(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Processes raw data into a clean, validated DataFrame with outlier detection."""
    if not records:
        logging.warning("No records received for processing.")
        return pd.DataFrame()

    df = pd.DataFrame(records)
    df.rename(columns=FIELD_MAPPING, inplace=True)

    if 'age' in df.columns:
        current_year = pd.to_datetime('today').year
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df['year_built'] = current_year - df['age']

    validated_df = df.dropna(subset=REQUIRED_FIELDS).copy()
    num_dropped = len(df) - len(validated_df)
    if num_dropped > 0:
        logging.warning(f"Dropped {num_dropped} records due to missing required fields.")
    
    for col in ['square_footage', 'latitude', 'longitude', 'year_built']:
        validated_df[col] = pd.to_numeric(validated_df[col], errors='coerce')
    validated_df.dropna(subset=REQUIRED_FIELDS, inplace=True)

    q_low = validated_df["square_footage"].quantile(0.01)
    q_hi  = validated_df["square_footage"].quantile(0.99)
    outliers = validated_df[(validated_df["square_footage"] < q_low) | (validated_df["square_footage"] > q_hi)]
    
    if not outliers.empty:
        logging.warning(f"Flagged {len(outliers)} potential outliers based on extreme square footage.")
        logging.debug(f"Outlier PINs: {outliers['property_identification_number'].tolist()}")
    
    logging.info(f"Data validation complete. {len(validated_df)} valid records remain.")
    return validated_df[REQUIRED_FIELDS + ['property_identification_number']]

def _save_to_csv(df: pd.DataFrame, filename: str):
    """Saves the DataFrame to a CSV file."""
    if df.empty:
        logging.warning("DataFrame is empty. Nothing to save.")
        return
    try:
        df.to_csv(filename, index=False)
        logging.info(f"Clean dataset saved to '{filename}'.")
    except Exception as e:
        logging.error(f"Failed to save data to CSV: {e}")

def extract_industrial_data(output_filename: str = "cook_data.csv") -> pd.DataFrame:
    """Public function to orchestrate the data extraction process."""
    logging.info("Starting data extraction process.")
    raw_records = _fetch_cook_county_data()
    cleaned_df = _process_and_validate_data(raw_records)
    _save_to_csv(cleaned_df, output_filename)
    logging.info("Finished data extraction process.")
    return cleaned_df