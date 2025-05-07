# streamlit_app.py

import streamlit as st
import pandas as pd
import glob
import os
import json

st.title("Orders Dashboard")

# Parquet output folder (same as used in Spark)
parquet_dir = "data/streaming_parquet_output"

# Find the most recent Parquet files
files = sorted(glob.glob(os.path.join(parquet_dir, "*.parquet")), reverse=True)

if not files:
    st.warning("No Parquet files found yet.")
else:
    # Read a subset or latest
    latest_files = files[:20]  # Adjust as needed
    df = pd.concat([pd.read_parquet(f) for f in latest_files], ignore_index=True)

    if not df.empty:
        # Convert the JSON string into structured columns
        decoded_df = pd.json_normalize(df['decoded'].dropna().apply(json.loads))
        st.dataframe(decoded_df)
    else:
        st.info("Waiting for data...")
