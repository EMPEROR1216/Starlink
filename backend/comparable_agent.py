# comparable_agent.py

import logging
import pandas as pd
import os
import openai
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler

from data_extractor import extract_industrial_data

class ComparableAgent:
    """
    An intelligent agent responsible for finding, processing, and
    analyzing comparable industrial properties.
    """
    def __init__(self):
        self.industrial_properties_df = pd.DataFrame()
        logging.info("ComparableAgent initialized.")
        self._configure_openai()

    def _configure_openai(self):
        """Loads the API key from the .env file and configures the OpenAI client."""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logging.error("OPENAI_API_KEY not found in .env file. AI features will fail.")
            return
        openai.api_key = api_key
        logging.info("OpenAI client configured successfully.")

    def find_and_process_data(self) -> pd.DataFrame:
        """Main workflow for extracting and processing data."""
        logging.info("Agent starting task: Find and Process Data.")
        self.industrial_properties_df = extract_industrial_data(output_filename="cook_data.csv")
        return self.industrial_properties_df

    def find_comparables(self, target_pin: str, properties_df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """
        Finds the most similar properties to a target property using a weighted model.
        (Fulfills Phase 3 of the challenge).
        """
        if target_pin not in properties_df['property_identification_number'].values:
            logging.error(f"Target PIN {target_pin} not found in the dataset.")
            return pd.DataFrame()

        target_property = properties_df[properties_df['property_identification_number'] == target_pin].iloc[0]
        
        # Create a copy to avoid modifying the original dataframe
        df = properties_df[properties_df['property_identification_number'] != target_pin].copy()

        # Define features for comparison and their weights
        features = ['square_footage', 'year_built', 'latitude', 'longitude']
        weights = {'square_footage': 0.4, 'year_built': 0.2, 'latitude': 0.2, 'longitude': 0.2}

        # Normalize features to a 0-1 scale so they can be compared fairly
        scaler = MinMaxScaler()
        df_normalized = pd.DataFrame(scaler.fit_transform(df[features]), columns=features, index=df.index)
        target_normalized = scaler.transform(target_property[features].values.reshape(1, -1))[0]

        # Calculate weighted Euclidean distance to find similarity
        distances = df_normalized.apply(
            lambda row: sum(
                weights[feat] * (row[feat] - target_normalized[i])**2 for i, feat in enumerate(features)
            )**0.5,
            axis=1
        )
        
        # Convert distance to a "confidence score" (higher is better)
        df['confidence_score'] = 1 / (1 + distances)
        
        # Return Top N Comparables
        comparables = df.sort_values(by='confidence_score', ascending=False).head(top_n)
        return comparables