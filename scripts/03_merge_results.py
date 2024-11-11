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
        v = None
        if c == "value" and model_id == "eos3nn9":
            v = "pic50"
        if v is None:
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
    columns = [c for c in columns if "drugbank_approved_percentile" not in c]
    if model_id == "eos7kpb":
        print("Skipping some columns for the H3D model")
        columns = [c for c in columns if "_norm" not in c]
        columns = [c for c in columns if c.startswith("pf") or c.startswith("mtb")]
    df = df[columns]
    df = df.rename(columns=columns_renamer(columns, model_id), inplace=False)
    return df

for model_id in model_ids:
    df_ = load_model_results_file(model_id)
    if df_ is None:
        continue
    df = pd.concat([df, df_], axis=1)

df.to_csv(os.path.join(ROOT, "..", "results", "anpdb_annotated.tsv"), sep="\t", index=False)

print("Saving individual results")
columns = list(df.columns)

for model_id in model_ids:
    subcols = [x for x in columns if x.endswith(model_id)]
    if len(subcols) == 0:
        continue
    subcols = columns[:3] + subcols
    df[subcols].to_csv(os.path.join(ROOT, "..", "results", "by_model", "{0}.csv".format(model_id)), index=False)