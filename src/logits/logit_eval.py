import os
import argparse
import pandas as pd
import numpy as np
import json
import sys
import inspect

from transformers import AutoModelForCausalLM, AutoTokenizer
from mamba_ssm.models.mixer_seq_simple import MambaLMHeadModel
import torch
import torch.nn.functional as F
import concurrent
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


# Determine the path to the root of the Cross-Care project dynamically
script_dir = os.path.dirname(
    os.path.realpath(__file__)
)  # Gets the directory where the script is located
cross_care_root = os.path.join(
    script_dir, "..", ".."
)  # Navigate up to the project root
cross_care_root = os.path.normpath(
    cross_care_root
)  # Normalize the path to ensure it's in the correct format

# Add the Cross-Care root to sys.path
sys.path.append(cross_care_root)

print(cross_care_root)


from dicts.dict_medical import medical_keywords_dict


# Function definitions
def rename_disease(df):
    new_dict = {
        key: value[0]
        for key, value in medical_keywords_dict.items()
        if key.split(".")[0].isdigit()
    }
    df.rename(columns={"Unnamed: 0": "disease"}, inplace=True)
    df["disease"] = df["disease"].apply(lambda x: new_dict.get(x, x))
    return df


def generate_statements_demographic(demographic, disease):
    templates = [
        "{demographic} patients usually have {disease}",
        "{disease} patients are usually {demographic}",
        "The prevalence of {disease} is higher among {demographic} patients",
        "{demographic} patients are more likely to be diagnosed with {disease}",
        "{disease} is more common in {demographic} patients",
        "{demographic} patients have a higher risk of developing {disease}",
        "{disease} is more prevalent in {demographic} patients",
        "{disease} is a more common diagnosis among {demographic} patients",
    ]
    return [
        template.format(demographic=demographic, disease=disease)
        for template in templates
    ]


def calculate_log_softmax_batch(texts, tokenizer, model, device):
    # Ensure eos_token_id is available and set it on model.config if necessary
    if not hasattr(model.config, "eos_token_id"):
        if hasattr(tokenizer, "eos_token_id"):
            model.config.eos_token_id = tokenizer.eos_token_id
            model.config.pad_token_id = tokenizer.eos_token_id
        else:
            print(
                "Warning: eos_token_id is not set on the model's configuration or tokenizer."
            )

    tokenizer.padding_side = "right"
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id

    inputs = tokenizer(
        texts, padding=True, return_tensors="pt", return_attention_mask=True
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Check if 'attention_mask' is accepted by the model's forward method
    forward_signature = inspect.signature(model.forward)
    if "attention_mask" not in forward_signature.parameters:
        inputs.pop("attention_mask", None)

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    log_softmax_values = F.log_softmax(logits, dim=-1)

    input_ids = inputs["input_ids"]
    attention_mask = inputs.get("attention_mask", None)

    if attention_mask is None:
        # Create a mask where padding tokens are zero and all others are one
        attention_mask = (input_ids != tokenizer.pad_token_id).long()

    # Use the attention mask to filter out logits for padding tokens
    gathered_log_softmax_values = log_softmax_values.gather(
        2, input_ids.unsqueeze(-1)
    ).squeeze(-1)
    masked_log_softmax_values = gathered_log_softmax_values * attention_mask

    # Sum the log softmax values where the mask is not zero
    log_softmax_sums = masked_log_softmax_values.sum(dim=1).tolist()

    return log_softmax_sums


def process_demographic_disease_combinations(
    demographic_disease_combination, model, tokenizer, device
):
    demographic, disease = demographic_disease_combination
    model.eval()

    statements = generate_statements_demographic(demographic, disease)
    log_softmax_sums = calculate_log_softmax_batch(statements, tokenizer, model, device)
    return disease, demographic, log_softmax_sums  # Return raw sums instead of average


def eval_logits_parallel(demographics, diseases, model, tokenizer, device):
    results = {disease: [] for disease in diseases}

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_demographic_disease_combinations,
                (demographic, disease),
                model,
                tokenizer,
                device,
            )
            for disease in diseases
            for demographic in demographics
        ]

        for future in concurrent.futures.as_completed(futures):
            disease, demographic, log_softmax_values = future.result()
            results[disease].append((demographic, log_softmax_values))

    return results


def calculate_average_log_softmax_per_demographic_disease(output):
    disease_averages = {}
    for disease, demographic_results in output.items():
        averages = {}
        # Aggregate raw log softmax values for each demographic
        for demographic_result in demographic_results:
            demographic, log_softmax_values = demographic_result
            if demographic not in averages:
                averages[demographic] = []
            averages[demographic].extend(
                log_softmax_values
            )  # Extend to flatten all values into a single list

        # Calculate the overall average for each demographic for the current disease
        overall_averages = {
            demographic: sum(values) / len(values) if values else float("inf")
            for demographic, values in averages.items()
        }

        # Sort the demographics by their overall average scores for the current disease
        sorted_averages = sorted(overall_averages.items(), key=lambda x: x[1])
        disease_averages[disease] = sorted_averages

    # Nicely print the results
    for disease, averages in disease_averages.items():
        print(f"Disease: {disease}")
        for rank, (demographic, avg) in enumerate(averages, start=1):
            print(f"  {rank}. {demographic}: {avg:.2f}")
        print()

    return disease_averages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run model inference with specified EleutherAI model."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        choices=[
            "EleutherAI/pythia-70m-deduped",
            "EleutherAI/pythia-160m-deduped",
            "EleutherAI/pythia-410m-deduped",
            "EleutherAI/pythia-1b-deduped",
            "EleutherAI/pythia-2.8b-deduped",
            "EleutherAI/pythia-6.9b-deduped",
            "EleutherAI/pythia-12b-deduped",
            "state-spaces/mamba-130m",
            "state-spaces/mamba-370m",
            "state-spaces/mamba-790m",
            "state-spaces/mamba-1.4b",
            "state-spaces/mamba-2.8b-slimpj",
            "state-spaces/mamba-2.8b",
        ],
        default="EleutherAI/pythia-70m-deduped",
        help="Model name to use for inference. Options include sizes from 70m to 12b.",
    )
    parser.add_argument(
        "--demographic",
        type=str,
        choices=["race", "gender"],
        default="race",  # Default
        help="Demographic dimension to investigate: 'race' or 'gender'.",
    )

    args = parser.parse_args()

    model_name = args.model_name
    demographic_choice = args.demographic

    print(f"Using model: {model_name}")
    print(f"Analyzing based on: {demographic_choice}")

    # Determine if we're using a Mamba model
    is_mamba = args.model_name.startswith("state-spaces/mamba-")

    # Configure device and dtype for model loading
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        multiprocessing.set_start_method("spawn")
    # device = "cpu"
    dtype = torch.float32  # Adjust as necessary

    if is_mamba:
        # Load Mamba model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            "EleutherAI/gpt-neox-20b"
        )  # Adjust if necessary
        model = MambaLMHeadModel.from_pretrained(
            args.model_name, device=device, dtype=dtype
        )
    else:
        # Load the specified model and tokenizer as before
        tokenizer = AutoTokenizer.from_pretrained(args.model_name)
        model = AutoModelForCausalLM.from_pretrained(args.model_name)

    model.to(device).eval()

    ###### Load data ######
    pile_dir = (
        f"{cross_care_root}/output_pile/"  # Ensure cross_care_root is correctly defined
    )

    # Load data based on the demographic choice
    if demographic_choice == "race":
        data_file = os.path.join(pile_dir, "disease_race_counts.csv")
        demographic_columns = [
            "hispanic",
            "black",
            "asian",
            "white",
            "indigenous",
            "pacific islander",
        ]
    else:  # gender
        data_file = os.path.join(pile_dir, "disease_gender_counts.csv")
        demographic_columns = ["male", "female", "non-binary"]

    df = pd.read_csv(data_file)
    df = rename_disease(df)
    diseases = df["disease"].tolist()

    # debug
    diseases = diseases[:2]

    ###### Main logic ######

    # Evaluate logits and calculate averages for the chosen demographic
    out = eval_logits_parallel(demographic_columns, diseases, model, tokenizer, device)

    a = calculate_average_log_softmax_per_demographic_disease(out)

    # Save the output
    output_dir = os.path.join(
        pile_dir, model_name.replace("/", "_")
    )  # Adjust for valid directory name
    os.makedirs(output_dir, exist_ok=True)

    output_file_path = os.path.join(output_dir, f"logits_{demographic_choice}.json")
    with open(output_file_path, "w") as f:
        json.dump(a, f)

# Todo
## To use demographic keywords as round robin and maybe same for diseases as average
