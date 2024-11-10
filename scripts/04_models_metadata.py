import json
import os
import requests
from tqdm import tqdm

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

def get_readmes(model_id):
    url  ="https://raw.githubusercontent.com/ersilia-os/{0}/refs/heads/main/README.md".format(model_id)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

models_metadata = {}
for model_id in tqdm(models_to_run):
    models_metadata[model_id] = {
        "title": get_title(model_id)
    }

models_readmes = {}
for model_id in tqdm(models_to_run):
    models_readmes[model_id] = get_readmes(model_id)

with open(os.path.join(ROOT, "..", "results", "models_metadata.json"), "w") as f:
    json.dump(models_metadata, f, indent=4)

with open(os.path.join(ROOT, "..", "results", "models_readmes.json"), "w") as f:
    json.dump(models_readmes, f, indent=4)