import os
import json
import pandas as pd
import streamlit as st

ROOT = os.path.abspath(os.path.dirname(__file__))
RESULTS_DIR = os.path.abspath(os.path.join(ROOT, "..", "results"))
DATA_DIR = os.path.abspath(os.path.join(ROOT, "..", "data"))

# Setting up Streamlit App
st.set_page_config(layout="wide", page_title="ANPDB Ersilia Model Hub Annotation")

# Loading necessary data
@st.cache_data
def load_results_data():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "anpdb_annotated.tsv"), sep="\t")
    return df

@st.cache_data
def load_models_metadata():
    with open(os.path.join(RESULTS_DIR, "models_metadata.json"), "r") as f:
        data = json.load(f)
    return data

@st.cache_data
def load_models_readmes():
    with open(os.path.join(RESULTS_DIR, "models_readmes.json"), "r") as f:
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
model_readmes = load_models_readmes()

available_model_ids = [x.split("_")[-1] for x in list(df.columns)[3:]]

# App layout

# Sidebar

st.sidebar.header("About this app")
st.sidebar.markdown("This app was developed as part of a **capacity building workshop** on AI/ML for drug discovery in **Buea, Cameroon** in November 2024. The tool is designed to help researchers explore the **African Natural Products Database** (ANPDB) annotated with predictions from the **Ersilia Model Hub**.")
st.sidebar.markdown("To reproduce this code or run the app locally, please visit the [anpdb-annotation](https://github.com/ersilia-os/anpdb-annotation) GitHub repository.")
st.sidebar.header("About ANPDB")
st.sidebar.markdown("The [African Natural Products Database](https://african-compounds.org/anpdb/) is a database of natural product compounds found in Africa. It is maintained by the [University of Buea Centre for Drug Discovery](https://www.ub-cedd.org/).")

st.sidebar.header("About the Ersilia Model Hub")
st.sidebar.markdown("The [Ersilia Model Hub](https://github.com/ersilia-os/ersilia) is a repository of AI/ML for drug discovery. It is maintained by the [Ersilia Open Source Initiative](https://ersilia.io).")

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
    return [x.split("[")[1].split("]")[0] for x in selected_options]

st.header(":robot_face: Select models to display!")

chem_model_ids = create_model_checkbox(st, "Chemical Properties")
adme_model_ids = create_model_checkbox(st, "ADMET")
bact_model_ids = create_model_checkbox(st, "Bioactivity")
proj_model_ids = create_model_checkbox(st, "2D projections")

selected_model_ids = chem_model_ids + adme_model_ids + bact_model_ids + proj_model_ids
selected_model_ids = [x for x in selected_model_ids if x in available_model_ids]

st.header(":herb: Explore the data")

columns_to_keep = list(df.columns)[:3] + [x for x in list(df.columns[3:]) if x.split("_")[-1] in selected_model_ids]
df = df[columns_to_keep]
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
models = [x for k,v in model_categories.items() for x in v]
options = ["{0}: {1}".format(model, models_metadata[model]["title"]) for model in models]
selected_option = st.selectbox("Select a model", options, index=None)
if selected_option is not None:
    selected_model_id = selected_option.split(":")[0]
else:
    selected_model_id = None

if selected_model_id is not None:
    readme = model_readmes[selected_model_id]
    description = readme.split("# ")[1].split("## ")[0].split("\n")[1:]
    description = "\n".join(description).strip("\n").replace("\n", "").replace("#", "")
    publication_url = readme.split("[Publication]")[1].split("(")[1].split(")")[0]
    code_url = readme.split("[Source Code]")[1].split("(")[1].split(")")[0]
    st.markdown(description)
    st.markdown("* [Publication]({0})\n* [Code](code_url)".format(publication_url))