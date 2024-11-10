import os
import json
import pandas as pd
import streamlit as st

ROOT = os.path.abspath(os.path.dirname(__file__))
RESULTS_DIR = os.path.abspath(os.path.join(ROOT, "..", "results"))
DATA_DIR = os.path.abspath(os.path.join(ROOT, "..", "data"))

# Setting up Streamlit App
st.set_page_config(layout="wide")

# Loading necessary data
@st.cache_data
def load_results_data():
    return None
    df = pd.read_csv(os.path.join(RESULTS_DIR, "anpdb_annotated.tsv"), sep="\t")
    return df

@st.cache_data
def load_models_metadata():
    with open(os.path.join(RESULTS_DIR, "models_metadata.json"), "r") as f:
        data = json.load(f)
    return data

@st.cache_data
def load_model_categories():
    with open(os.path.join(DATA_DIR, "models_by_category.json"), "r") as f:
        data = json.load(f)
    return data

df = load_results_data()
models_metadata = load_models_metadata()
model_categories = load_model_categories()

# App layout

# Sidebar

st.sidebar.title("What is in this repository?")
st.sidebar.markdown("This repository contains the results of the annotation of the African Natural Products Database with the Ersilia Model Hub.")
st.sidebar.markdown("Models were selected based on the interests of the UB-CeDD at the University of Buea, Cameroon.")
st.sidebar.markdown("To reproduce this code or run the app locally, please visit Ersilia's [anpdb-annotation](https://github.com/ersilia-os/anpdb-annotation) GitHub repository.")
st.sidebar.header("About ANPDB")

st.sidebar.header("About the Ersilia Model Hub")
st.sidebar.markdown("The [Ersilia Model Hub](https://github.com/ersilia-os/ersilia) is a repository of AI/ML for drug discovery.")

st.sidebar.warning("This app contains calculations and predictions made with AI/ML models. It is possible that the predictions are not accurate. Please use the information provided with caution.")
st.sidebar.info("The Ersilia Model Hub is intended for research purposes. Please [report any issues](https://github.com/ersilia-os/anpdb-annotation/issues) to the Ersilia team.")

# Main panel

st.title("ANPDB annotated with the Ersilia Model Hub")


def create_model_checkbox(col, category, value=None):
    title = category
    model_ids = model_categories[category]
    display_options = ["[{0}](https://github.com/ersilia-os/{0}): {1}".format(model_id, models_metadata[model_id]["title"]) for model_id in model_ids]
    if value is not None:
        value = display_options[value]
    selected_options = col.pills(options=display_options, label=title, selection_mode="multi", default=value)
    return [x.split(":")[0] for x in selected_options]

st.header(":robot_face: Select models to display!")

chem_model_ids = create_model_checkbox(st, "Chemical Properties", value=0)
adme_model_ids = create_model_checkbox(st, "ADMET")
bact_model_ids = create_model_checkbox(st, "Bioactivity")
proj_model_ids = create_model_checkbox(st, "2D projections")

st.header(":herb: Explore the data")

df = pd.DataFrame()
st.dataframe(df)

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
   "Download as CSV file",
   csv,
   "anpdb_ersilia_annotation.csv",
   "text/csv",
   key='download-csv'
)

st.header(":book: Learn more about the models")
