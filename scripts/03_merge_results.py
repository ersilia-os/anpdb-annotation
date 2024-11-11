import os
import pandas as pd

ROOT = os.path.abspath(os.path.dirname(__file__))

model_ids = []
with open(os.path.join(ROOT, "..", "data", "models_to_run.txt"), "r") as f:
    for l in f:
        l = l.strip()
        if not l.startswith("eos"):
            continue
        model_ids += [l]

df = pd.read_csv(os.path.join(ROOT, "..", "data", "all_molecules.tsv"), sep="\t")

def columns_renamer(columns, model_id):
    rename = {}
    for c in columns:
        if c == "value" and model_id == "eos3nn9":
            v = "pic50"
        else:
            v = c.lower()
            v = v.replace(" ", "_")
            v = v.replace("-", "_")
        v = v + "_" + model_id
        if model_id == "eos3nn9":
            print(c, v)
        rename[c] = v
    return rename

def load_model_results_file(model_id):
    file_name = os.path.join(ROOT, "..", "results", "anpdb_intermediate", "{0}.csv".format(model_id))
    if not os.path.exists(file_name):
        return None
    df = pd.read_csv(file_name)
    columns = list(df.columns)[2:]
    # filter for the admet model
    columns = [c for c in columns if "drugbank_approved_percentile" not in c]
    df = df[columns]
    df = df.rename(columns=columns_renamer(columns, model_id), inplace=False)
    return df

for model_id in model_ids:
    if model_id in ["eos4e40"]:
        continue
    df_ = load_model_results_file(model_id)
    if df_ is None:
        continue
    df = pd.concat([df, df_], axis=1)

df.to_csv(os.path.join(ROOT, "..", "results", "anpdb_annotated.tsv"), sep="\t", index=False)