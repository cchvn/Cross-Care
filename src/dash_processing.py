import os
import pandas as pd
import numpy as np
import json
import sys

sys.path.append("/home/wsl_legion/Cross-Care/")
from dicts.dict_medical import medical_keywords_dict
from dicts.dict_census_est import census_dict


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


# Write to JSON
def write_to_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as outfile:
        json.dump(data, outfile)


def calculate_percentage_deviation(df, group_columns, census_dict):
    # Keep 'disease' column for reference
    diseases = df["disease"]

    # Calculate the total counts
    total_counts = df[group_columns].sum(axis=1)

    # Prepare expected counts based on census percentages
    expected_counts = np.array(
        [total_counts * (census_dict[group] / 100) for group in group_columns]
    ).T

    # Initialize percentage deviation array
    percentage_deviation = np.zeros_like(expected_counts, dtype=float)

    # Compute percentage deviation only for non-zero total counts
    non_zero_mask = total_counts > 0
    percentage_deviation[non_zero_mask] = (
        (df[group_columns].to_numpy()[non_zero_mask] - expected_counts[non_zero_mask])
        / expected_counts[non_zero_mask]
    ) * 100

    # Return DataFrame with 'disease' column included
    percentage_deviation_df = pd.DataFrame(percentage_deviation, columns=group_columns)
    percentage_deviation_df["disease"] = diseases.values
    return percentage_deviation_df


#### Data Processing Functions ####


def process_total_counts(csv_path, medical_keywords_dict):
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"Unnamed: 0": "disease"})
    df = replace_disease_codes(df, medical_keywords_dict)
    df = df.sort_values(by=df.columns[1], ascending=False)
    return df.to_dict(orient="records")


def process_demo_counts(count_dir, medical_keywords_dict, demo_cat):
    if demo_cat != "racial":  # BUG: with racial naming convention
        csv_path = f"{count_dir}/disease_{demo_cat}_counts.csv"
    else:
        csv_path = f"{count_dir}/disease_race_counts.csv"

    df = pd.read_csv(csv_path)
    df = df.rename(columns={"Unnamed: 0": "disease"})

    df = replace_disease_codes(df, medical_keywords_dict)
    df = df.sort_values(by=df.columns[1], ascending=False)
    return df.to_dict(orient="records")


def process_temporal_counts(csv_path, medical_keywords_dict):
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Assuming all other columns except 'timestamp' are count data
    count_columns = df.columns.drop("timestamp")

    # Counts
    monthly_counts = df.groupby(pd.Grouper(key="timestamp", freq="M"))[
        count_columns
    ].sum()
    yearly_counts = df.groupby(pd.Grouper(key="timestamp", freq="Y"))[
        count_columns
    ].sum()

    # For five-yearly counts, first calculate the 5-year intervals
    df["five_year_interval"] = (df["timestamp"].dt.year // 5) * 5
    five_yearly_counts = df.groupby("five_year_interval")[count_columns].sum()

    # Pivot and process
    def pivot_and_process(df_counts, freq):
        df_counts = df_counts.T.reset_index()
        df_counts.rename(columns={"index": "disease"}, inplace=True)
        df_counts = replace_disease_codes(df_counts, medical_keywords_dict)
        df_counts["freq"] = freq
        return df_counts

    # Pivoting each DataFrame
    monthly_pivot = pivot_and_process(monthly_counts, "M")
    yearly_pivot = pivot_and_process(yearly_counts, "Y")
    five_yearly_pivot = pivot_and_process(five_yearly_counts, "5Y")

    # Ensure all column headers are strings
    monthly_pivot.columns = monthly_pivot.columns.astype(str)
    yearly_pivot.columns = yearly_pivot.columns.astype(str)
    five_yearly_pivot.columns = five_yearly_pivot.columns.astype(str)

    # Convert to dictionaries
    monthly_data = monthly_pivot.to_dict(orient="records")
    yearly_data = yearly_pivot.to_dict(orient="records")
    five_yearly_data = five_yearly_pivot.to_dict(orient="records")

    # Combine all data into a single dictionary
    all_data = {
        "monthly": monthly_data,
        "yearly": yearly_data,
        "five_yearly": five_yearly_data,
    }

    return all_data


# process subgroups
def process_subgroup_counts(csv_path, medical_keywords_dict):
    df = pd.read_csv(csv_path, names=["disease", "subgroup", "count"])
    df = replace_disease_codes(df, medical_keywords_dict)
    pivoted_df = df.pivot_table(
        index="disease", columns="subgroup", values="count", aggfunc="sum", fill_value=0
    )
    pivoted_df = pivoted_df.reset_index()
    pivoted_dict = pivoted_df.to_dict(orient="records")
    return pivoted_dict


def process_percentage_difference(out_dir, demo_cat, census_dict):
    # Prepare the data for subgroup counts
    if demo_cat == "gender":
        groups = ["male", "female"]
        census_demo_dict = census_dict["gender"]
    else:
        groups = [
            "white/caucasian",
            "black/african american",
            "native american/indigenous",
            "asian",
            "pacific islander",
            "hispanic/latino",
        ]
        census_demo_dict = census_dict["racial"]

    # read in json file
    json_path = out_dir + f"/total_{demo_cat}_counts.json"
    with open(json_path) as f:
        total_counts = json.load(f)

    # convert to dataframe
    df = pd.DataFrame(total_counts)
    print(df.head())

    # Calculate percentage deviation
    percentage_deviation_df = calculate_percentage_deviation(
        df, groups, census_demo_dict
    )
    print(percentage_deviation_df.head())

    # Reset index if necessary
    percentage_deviation_df = percentage_deviation_df.reset_index(drop=True)
    print(percentage_deviation_df.head())

    # Convert to dictionary for output
    deviation_dict = percentage_deviation_df.to_dict(orient="records")
    return deviation_dict


#### Main ####

if __name__ == "__main__":
    # paths
    count_dir = "output_arxiv"
    out_dir = "cross-care-dash/app/data"

    # window sizes
    window_sizes = [10, 50, 100, 250]
    demo_cat = ["gender", "racial", "drug"]

    #### TOTAL COUNTS ####

    # Process total counts
    total_counts_data = process_total_counts(
        csv_path=f"{count_dir}/total_disease_counts.csv",
        medical_keywords_dict=medical_keywords_dict,
    )
    write_to_json(total_counts_data, f"{out_dir}/total_counts.json")

    # Process demographic co-occurrence counts
    total_counts_dict = (
        {}
    )  # Dictionary to store the counts for each demographic category

    for demo in demo_cat:
        total_counts_dict[demo] = process_demo_counts(
            count_dir=count_dir,
            medical_keywords_dict=medical_keywords_dict,
            demo_cat=demo,
        )
        write_to_json(total_counts_dict[demo], f"{out_dir}/total_{demo}_counts.json")

    # Process date co-occurrence counts
    total_dates_data = process_temporal_counts(
        csv_path=f"{count_dir}/disease_date_counts.csv",
        medical_keywords_dict=medical_keywords_dict,
    )
    write_to_json(total_dates_data["monthly"], f"{out_dir}/monthly_counts.json")
    write_to_json(total_dates_data["yearly"], f"{out_dir}/yearly_counts.json")
    write_to_json(
        total_dates_data["five_yearly"],
        f"{out_dir}/five_yearly_counts.json",
    )

    # #### SUBGROUP COUNTS ####

    # Process subgroup counts and percentage difference
    window_subgroup_dict = {}

    for window_size in window_sizes:
        for demo in demo_cat:
            filename = f"{count_dir}/window_{window_size}/co_occurrence_{demo}.csv"

            # Process subgroup counts
            subgroup_counts_data = process_subgroup_counts(
                csv_path=filename, medical_keywords_dict=medical_keywords_dict
            )

            write_to_json(
                subgroup_counts_data,
                f"{out_dir}/window_{window_size}_{demo}_counts.json",
            )

    #### PERCENTAGE DIFFERENCE ####

    for demo in demo_cat[:2]:
        percentage_difference_data = process_percentage_difference(
            out_dir=out_dir,
            demo_cat=demo,
            census_dict=census_dict,
        )
        write_to_json(
            percentage_difference_data,
            f"{out_dir}/percentage_difference_{demo}.json",
        )

    print("Done!")
