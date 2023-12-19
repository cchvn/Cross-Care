import os
import pandas as pd
import numpy as np
import json
import sys

sys.path.append("/home/wsl_legion/Cross-Care/")
from dicts.dict_medical import medical_keywords_dict
from dicts.dict_census_est import census_dict

# paths
count_dir = "output_arxiv"
plot_dir = "plots/arxiv"

if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# window sizes
window_sizes = [10, 50, 100]
demo_cat = ["gender", "racial"]


#### Helper functions ####
# Code to Disease
def replace_disease_codes(df, medical_keywords_dict):
    """
    Replace disease codes with names in a DataFrame.

    :param df: DataFrame with disease names/codes.
    :param code_to_name_dict: Dictionary mapping codes to lists of names.
    :return: DataFrame with updated disease names.
    """
    for index, row in df.iterrows():
        disease = row["disease"]
        # Check if the last two characters are '.0'
        if isinstance(disease, str) and disease.endswith(".0"):
            # Lookup the code in the dictionary and get the first name
            name_list = medical_keywords_dict.get(disease)
            if name_list:
                df.at[index, "disease"] = name_list[0]
    return df


def calculate_percentage_deviation(df, group_columns, census_dict):
    # Calculate the total counts
    total_counts = df[group_columns].sum(axis=1).to_numpy()

    # Prepare expected counts based on census percentages
    expected_counts = np.array(
        [total_counts * (census_dict[group] / 100) for group in group_columns]
    ).T

    # Calculate percentage deviation
    percentage_deviation = (
        (df[group_columns].to_numpy() - expected_counts) / expected_counts
    ) * 100
    return pd.DataFrame(percentage_deviation, columns=group_columns)


#### Data Processing Functions ####


def process_total_counts(csv_path, medical_keywords_dict):
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"Unnamed: 0": "disease"})
    df = replace_disease_codes(df, medical_keywords_dict)
    df = df.sort_values(by=df.columns[1], ascending=False)
    df = df.head(20)
    return df.to_dict(orient="records")


def process_subgroup_counts(csv_path, medical_keywords_dict, groups):
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"Unnamed: 0": "disease"})
    df = replace_disease_codes(df, medical_keywords_dict)
    df = df.head(20)
    return df.to_dict(orient="records")


def process_percentage_difference(csv_path, medical_keywords_dict, groups, census_dict):
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"Unnamed: 0": "disease"})
    df = replace_disease_codes(df, medical_keywords_dict)
    df = df.head(20)
    percentage_deviation_df = calculate_percentage_deviation(df, groups, census_dict)
    return percentage_deviation_df.to_dict(orient="records")


#### Main ####

if __name__ == "__main__":
    # Process total counts
    total_counts_data = process_total_counts(
        csv_path=f"{count_dir}/total_disease_counts.csv",
        medical_keywords_dict=medical_keywords_dict,
    )

    output_data = {"total_counts": total_counts_data}
    print(output_data)

    for window_size in window_sizes:
        for demo in demo_cat:
            filename = f"{count_dir}/window_{window_size}/co_occurrence_{demo}.csv"

            # read csv
            df = pd.read_csv(filename)
            df = df.rename(columns={"Unnamed: 0": "disease"})
            df = replace_disease_codes(df, medical_keywords_dict)

            # Prepare the data for subgroup counts
            if demo == "gender":
                groups = ["male", "female"]
                census_demo_dict = census_dict["gender"]
            else:  # For 'racial'
                groups = df.columns[1:]
                census_demo_dict = census_dict["racial"]

            # Process subgroup counts
            subgroup_counts_data = process_subgroup_counts(
                csv_path=filename,
                medical_keywords_dict=medical_keywords_dict,
                groups=groups,
            )

            # Process percentage difference
            percentage_difference_data = process_percentage_difference(
                csv_path=filename,
                medical_keywords_dict=medical_keywords_dict,
                groups=groups,
                census_dict=census_demo_dict,
            )

            output_data[
                f"window_{window_size}_{demo}_subgroup_counts"
            ] = subgroup_counts_data
            output_data[
                f"window_{window_size}_{demo}_percentage_difference"
            ] = percentage_difference_data

    # Output the data as JSON
    with open("output_arxiv/processed_data.json", "w") as outfile:
        json.dump(output_data, outfile)
