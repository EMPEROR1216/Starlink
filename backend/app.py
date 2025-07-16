import streamlit as st
import pandas as pd
from comparable_agent import ComparableAgent

# --- Page Configuration (Sets the browser tab title and icon) ---
st.set_page_config(page_title="Starboard AI Agent", page_icon="⭐", layout="wide")

# --- Agent and Data Loading ---
# Use Streamlit's session state to initialize the agent only once.
if 'agent' not in st.session_state:
    st.session_state.agent = ComparableAgent()

# Use caching to load data only once. This function will only re-run if its code changes.
@st.cache_data
def load_data():
    """Cached function to run the agent's data extraction workflow."""
    # We use _agent here because it's a cached function
    df = st.session_state.agent.find_and_process_data()
    return df

# --- Main Application UI ---
st.title("⭐ Starboard AI Comparable Property Agent")
st.markdown("This agent extracts industrial property data and finds the most relevant comparables based on a weighted similarity model.")

# Load the data and show a status message
with st.spinner("Agent is loading property data..."):
    industrial_data = load_data()

if industrial_data.empty:
    st.error("The agent could not retrieve any data. Check logs ('data_extraction.log') for details.")
else:
    st.success(f"Agent successfully processed {len(industrial_data)} industrial properties.")
    
    st.subheader("Property Data Viewer")
    st.dataframe(industrial_data)

    # --- Comparable Analysis Section ---
    st.subheader("Find Comparable Properties")
    
    selected_pin = st.selectbox(
        'Select a Property by its Identification Number (PIN) to analyze:',
        options=industrial_data['property_identification_number'].unique()
    )

    if st.button("Find Comparables"):
        if selected_pin:
            with st.spinner("Agent is performing analysis..."):
                comparables_df = st.session_state.agent.find_comparables(selected_pin, industrial_data)
                
                st.subheader(f"Top 5 Comparables for PIN {selected_pin}")
                display_cols = ['property_identification_number', 'square_footage', 'year_built', 'confidence_score']
                st.dataframe(comparables_df[display_cols])
        else:
            st.warning("Please select a PIN.")