#!/bin/bash

# Define an array of model names
declare -a model_names=(
    "EleutherAI/pythia-70m-deduped"
    "EleutherAI/pythia-160m-deduped"
    "EleutherAI/pythia-410m-deduped"
    "EleutherAI/pythia-1b-deduped"
    "EleutherAI/pythia-2.8b-deduped"
    "EleutherAI/pythia-6.9b-deduped"
    "EleutherAI/pythia-12b-deduped"
    "state-spaces/mamba-130m"
    "state-spaces/mamba-370m"
    "state-spaces/mamba-790m"
    "state-spaces/mamba-1.4b"
    "state-spaces/mamba-2.8b-slimpj"
    "state-spaces/mamba-2.8b"
)

# Define an array of demographic choices
declare -a demographics=("race" "gender")

# Loop through each model name
for model_name in "${model_names[@]}"
do
    # Determine the device based on model type
    if [[ "$model_name" == "state-spaces/mamba-"* ]]; then
        device="cuda"
    else
        device="cpu"
    fi

    # Loop through each demographic
    for demographic in "${demographics[@]}"
    do
        echo "Running model inference for: $model_name, Demographic: $demographic, Device: $device"
        conda run --name in_biased_learning python logit_eval.py --model_name "$model_name" --demographic "$demographic" --device "$device"
        echo "Completed: $model_name, Demographic: $demographic"
    done
done
