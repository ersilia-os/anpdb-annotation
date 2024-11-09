filename="../data/models_to_run.txt"

ersilia -v fetch eos2r5a --from_dockerhub
ersilia -v fetch eos7d58 --from_dockerhub
ersilia -v fetch eos2ta5 --from_dockerhub
ersilia -v fetch eos9f6t --from_dockerhub
ersilia -v fetch eos3nn9 --from_dockerhub
ersilia -v fetch eos4e40 --from_dockerhub
ersilia -v fetch eos7kpb --from_dockerhub
ersilia -v fetch eos4zfy --from_dockerhub

while IFS= read -r MODEL_ID; do
    echo "$MODEL_ID"
    ersilia serve "$MODEL_ID"
    ersilia run -i ../data/all_smiles.csv -o ../results/anpdb_intermediate/"$MODEL_ID".csv
    ersilia close
done < "$filename"