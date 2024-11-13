import os
import json
import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import gaussian_kde

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

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def read_drugbank_eos9gg2_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "drugbank_smiles.csv"))
    df = pd.concat([df, pd.read_csv(os.path.join(DATA_DIR, "drugbank_eos9gg2.csv"))], axis=1)
    return df

df = load_results_data()
models_metadata = load_models_metadata()
model_categories = load_model_categories()
model_readmes = load_models_readmes()
csv = convert_df(df)
db_eos9gg2 = read_drugbank_eos9gg2_data()

available_model_ids = [x.split("_")[-1] for x in list(df.columns)[3:]]

# App layout

# Sidebar

st.sidebar.image(os.path.join(ROOT, "..", "assets", "Ersilia_Brand.png"), width=200)

st.sidebar.header("About this app")
st.sidebar.markdown("This app was developed as part of a **capacity building workshop** on AI/ML for drug discovery in **Buea, Cameroon** in November 2024. The tool is designed to help researchers explore the **African Natural Products Database** (ANPDB) annotated with predictions from the **Ersilia Model Hub**.")
st.sidebar.markdown("To reproduce this code or run the app locally, please visit the [anpdb-annotation](https://github.com/ersilia-os/anpdb-annotation) GitHub repository.")

st.sidebar.download_button(
"Download all annotations as CSV file",
csv,
"anpdb_ersilia_annotation.csv",
"text/csv",
key='download-csv'
)

st.sidebar.header("About ANPDB")
st.sidebar.markdown("The [African Natural Products Database](https://african-compounds.org/anpdb/) is a database of natural product compounds found in Africa. It is maintained by the [University of Buea Centre for Drug Discovery](https://www.ub-cedd.org/).")

st.sidebar.header("About the Ersilia Model Hub")
st.sidebar.markdown("The [Ersilia Model Hub](https://github.com/ersilia-os/ersilia) is a repository of AI/ML for drug discovery. It is maintained by the [Ersilia Open Source Initiative](https://ersilia.io).")

st.sidebar.warning("This app contains calculations and predictions made with AI/ML models. It is possible that the predictions are not accurate. Please use the information provided with caution.")
st.sidebar.info("The Ersilia Model Hub is intended for research purposes. Please [report any issues](https://github.com/ersilia-os/anpdb-annotation/issues) to the Ersilia team.")

# Main panel

st.title("ANPDB annotated with the Ersilia Model Hub")


def create_model_checkbox(col, category):
    title = "Select a model from the {0} category".format(category)
    model_ids = model_categories[category]
    display_options = ["[{0}](https://github.com/ersilia-os/{0}): {1}".format(model_id, models_metadata[model_id]["title"]) for model_id in model_ids]
    value = display_options[0]
    selected_option = col.pills(options=display_options, label=title, selection_mode="single", default=value)
    if selected_option is None:
        return None
    else:
        return selected_option.split("[")[1].split("]")[0]

st.header(":robot_face: Select models to display!")

category = st.pills("Select a category", list(model_categories.keys()), selection_mode="single", default=None)
if category is not None:

    sel_model_id = create_model_checkbox(st, category)

    if sel_model_id is not None:
        readme = model_readmes[sel_model_id]
        description = readme.split("# ")[1].split("## ")[0].split("\n")[1:]
        description = "\n".join(description).strip("\n").replace("\n", "").replace("#", "")
        publication_url = readme.split("[Publication]")[1].split("(")[1].split(")")[0]
        code_url = readme.split("[Source Code]")[1].split("(")[1].split(")")[0]
        st.markdown(description)
        st.markdown("* [Publication]({0})\n* [Code](code_url)".format(publication_url))

        st.header(":herb: Explore the data")
        
        selected_model_ids = [sel_model_id]

        columns_to_keep = list(df.columns)[:3] + [x for x in list(df.columns[3:]) if x.split("_")[-1] in selected_model_ids]
        df = df[columns_to_keep]
        st.dataframe(df)

        st.header(":eyes: Visualize the data")

        if sel_model_id != "eos9gg2":
            visualization_options = ["_".join(x.split("_")[:-1]) for x in columns_to_keep[3:]]
            plot_type = "distribution"
        else:
            visualization_options = ["UMAP", "tSNE", "PCA 1 vs 2", "PCA 3 vs 4"]
            plot_type = "scatter"

        selected_option = st.selectbox("What do you want to visualize?", visualization_options, index=0)
        if plot_type == "distribution":
            # Sample data
            data = list(df[selected_option+"_"+sel_model_id])
            # Create a Gaussian KDE
            kde = gaussian_kde(data)

            # Define a range of values where you want to evaluate the KDE
            x_values = np.linspace(min(data), max(data), 100)  # 100 points between min and max of data

            # Get density values
            density_values = kde(x_values)
            dp = pd.DataFrame({selected_option: x_values, "density": density_values})
            st.area_chart(dp, x=selected_option, y="density")
        else:
            if selected_option == "UMAP":
                xcol = "umap_1"
                ycol = "umap_2"
            elif selected_option == "tSNE":
                xcol = "tsne_1"
                ycol = "tsne_2"
            elif selected_option == "PCA 1 vs 2":
                xcol = "pca_1"
                ycol = "pca_2"
            elif selected_option == "PCA 3 vs 4":
                xcol = "pca_3"
                ycol = "pca_4"
            else:
                xcol = None
                ycol = None
            dp = pd.DataFrame({xcol: df[xcol+"_"+sel_model_id], ycol: df[ycol+"_"+sel_model_id]})
            dp["category"] = "anpdb"

            db = pd.DataFrame({xcol: db_eos9gg2[xcol.replace("_", "-")], ycol: db_eos9gg2[ycol.replace("_", "-")]})
            db["category"] = "drugbank"

            dp = pd.concat([db, dp], axis=0)

            st.scatter_chart(dp, x=xcol, y=ycol, color="category", width=1000, height=1000)
            