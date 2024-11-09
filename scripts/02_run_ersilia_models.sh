filename="data/models_to_run.txt"

while IFS= read -r MODEL_ID; do
    echo "$MODEL_ID"
    ersilia serve "$MODEL_ID"
    ersilia run -i data/all_smiles.csv -o results/intermediate/"$MODEL_ID".csv
    ersilia close
done < "$filename"