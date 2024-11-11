filename="../data/models_to_run2.txt"

while IFS= read -r MODEL_ID; do
    echo "$MODEL_ID"
    ersilia serve "$MODEL_ID"
    ersilia run -i ../data/all_smiles.csv -o ../results/anpdb_intermediate/"$MODEL_ID".csv
    ersilia close
done < "$filename"
