# African Natural Products Database Annotation Pipeline

Annotation of ANPDB compounds using the [Ersilia Model Hub](https://gihtub.com/ersilia-os/ersilia). This project is part of an ongoing collaboration between Prof. Ntie-Kang's Centre for Drug Discovery at the University of Buea (UB-CeDD) and the [Ersilia Open Source Initiative](https://ersilia.io).

The purpose of this pipeline is to **annotate the ANPDB** with a few **selected models from the Ersilia Model Hub**. The pipeline starts with chemical structures (SMILES strings) and it returns a table with multiple calculations properties and predictions.

At a high level, we calculate the following properties:
* Physicochemical properties
* Synthetic accessibility properties
* ADMET properties
* Bioactivity prediction against some pathogens such as _Plasmodium falciparum_ and _Mycobacterium tuberculosis_.
* Chemical space exploration components for 2D visualization

There is an **app associated with this pipeline**. Click the link below to access it:
* [ANPDB Annotation Demo App](https://anpdb-annotation.streamlit.app/)

## Installation

We recommend that you create a Conda environment to run the pipeline. A few dependencies are also necessary, such as `rdkit` and the `standardiser`.

```bash
conda create -n anpdb-annotation python=3.10
conda activate anpdb-annotation
cd anpdb-annotation
pip install -r requirements.txt
```

Then you need to make sure that the [Ersilia CLI](https://github.com/ersilia-os/ersilia) is appropriately installed. Docker should be active in your system.

Fetch the following models:
```bash
ersilia fetch
```

## How to run the the pipeline

To annotate ANPDB, simply run the following:
```bash
bash run_pipeline.sh
```

An `anpdb_annotated.tsv` file will be stored in the `results/` folder.

## How to interpret the results table
