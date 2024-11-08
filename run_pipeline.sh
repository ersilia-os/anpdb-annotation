echo "Fetching molecules from ANPDB"
python scripts/00_fetch_anpdb_data.sh

echo "Assembling input"
python scripts/01_assemble_input.py

echo "Running Ersilia Models. This will take a while!"
bash scripts/02_run_ersilia_models.sh

echo "Done! Merging results"
python scripts/03_merge_results.py