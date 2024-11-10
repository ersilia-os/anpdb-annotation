import json
import os
import requests
import tqdm

ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, "..", "data", "models_to_run.txt"), "r") as f:
    models_to_run = f.read().splitlines()

def get_title(model_id):
    url  ="https://raw.githubusercontent.com/ersilia-os/{0}/refs/heads/main/README.md".format(model_id)
    response = requests.get(url)
    if response.status_code == 200:
        title = response.text.splitlines()[0].replace("# ", "")
    else:
        title = model_id
    return title

models_metadata = {}
for model_id in tqdm(models_to_run):
    models_metadata[model_id] = {
        "title": get_title(model_id)
    }

with open(os.path.join(ROOT, "..", "results", "models_metadata.json"), "w") as f:
    json.dump(models_metadata, f, indent=4)