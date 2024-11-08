import os
import json
import pandas as pd
import streamlit as st

ROOT = os.path.abspath(os.path.dirname(__file__))
RESULTS_DIR = os.path.abspath(os.path.join(ROOT, "..", "results"))

# Loading necessary data
@st.cache_data
def load_results_data():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "anpdb_annotated.tsv"), sep="\t")
    return df

@st.cache_data
def load_models_metadata():
    with open(os.path.join(RESULTS_DIR, "models_metadata.json"), "f") as f:
        data = json.load(f)
    return data

df = load_results_data()
models_metadata = load_models_metadata()

# App layout

st.title("African Natural Products Database annotated with the Ersilia Model Hub")
