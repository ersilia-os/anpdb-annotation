import os
import csv
import collections
from tqdm import tqdm
from rdkit import Chem
from standardiser import standardise


ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "..", "data", "SMILES")

input_filenames = [
    "smiles_unique_all.smi",
    "smiles_unique_EANPDB.smi",
    "smiles_unique_NANPDB.smi"
]

for input_filename in input_filenames:
    molecules = []
    with open(os.path.join(DATA_DIR, input_filename), "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for r in reader:
            if len(r) == 2:
                molecules += [(r[0], r[1])]
    molecules = list(set(molecules))

smi2names = collections.defaultdict(list)
for m in tqdm(molecules):
    mol = Chem.MolFromSmiles(m[0])
    name = m[1].strip()
    if mol is None:
        continue
    try:
        mol = standardise.run(mol)
        if mol is None:
            continue
    except:
        continue
    smi = Chem.MolToSmiles(mol)
    smi2names[smi] += [name]

smi2name = dict((k, " | ".join(sorted(set(v)))) for k,v in smi2names.items())

output_filename = os.path.join(DATA_DIR, "..", "all_molecules.tsv")
with open(output_filename, "w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["inchikey", "smiles", "name"])
    smiles = sorted([k for k, _ in smi2name.items()])
    for smi in tqdm(smiles):
        mol = Chem.MolFromSmiles(smi)
        name = smi2name[smi]
        inchikey = Chem.MolToInchiKey(mol)
        writer.writerow([inchikey, smi, name])

output_smiles_filename = os.path.join(DATA_DIR, "..", "all_smiles.csv")
with open(output_smiles_filename, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["smiles"])
    for smi in smiles:
        writer.writerow([smi])