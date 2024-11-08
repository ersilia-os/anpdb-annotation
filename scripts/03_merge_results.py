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
        v = c.lower()
        v = v.replace(" ", "_")
        v = model_id + "_" + model_id
        rename[c] = v
    return rename

def load_model_results_file(model_id):
    df = pd.read_csv(os.path.join(ROOT, "..", "results", "intermediate", "{0}.csv".format(model_id)))
    columns = list(df.columns)[2:]
    # filter for the admet model
    columns = [c for c in columns if "drugbank_percentile" not in c]
    df = df[columns]
    df = df.rename(columns=columns_renamer(columns, model_id), inplace=False)
    return df

for model_id in model_ids:
    df = pd.concat([df, load_model_results_file(model_id)])

df.to_csv(os.path.join(ROOT, "..", "results", "anpdb_annotated.tsv"), sep="\t")