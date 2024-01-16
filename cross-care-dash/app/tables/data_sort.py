from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import json
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the directory where this script is located
current_directory = os.path.dirname(os.path.abspath(__file__))


# Function to sort data
def sort_data(data, sort_key, sort_order):
    # Check if the sort_key is valid
    if sort_key not in data[0]:
        return data  # Return unsorted data if the key is not valid

    if sort_key == "disease":
        if sort_order == "asc":
            data.sort(key=lambda x: x.get(sort_key, "").lower())
        elif sort_order == "desc":
            data.sort(key=lambda x: x.get(sort_key, "").lower(), reverse=True)
    else:
        data.sort(key=lambda x: int(x.get(sort_key, 0)), reverse=sort_order == "desc")
    return data


@app.route("/get-sorted-data", methods=["GET"])
def get_sorted_data():
    try:
        category = request.args.get("category", "total")
        selectedWindow = request.args.get("selectedWindow", "total")
        sort_key = request.args.get("sortKey", "disease")
        sort_order = request.args.get("sortOrder", "asc")

        selectedDisease = request.args.get("selectedDisease", "pneumonia,acne,asthma")

        # Construct the path to the correct data file based on category
        if category == "total":
            data_file_path = os.path.join(
                current_directory, f"../data/total_counts.json"
            )
        else:
            data_file_path = os.path.join(
                current_directory, f"../data/{selectedWindow}_{category}_counts.json"
            )

        # Load the data from the correct file
        with open(data_file_path, "r") as file:
            category_data = json.load(file)

        logging.info(f"Data loaded successfully from {data_file_path}")

        # Sort data
        sorted_data = sort_data(category_data, sort_key, sort_order)
        print(sorted_data)

        # Filter data by selected disease
        if selectedDisease:
            sorted_data = filter_by_disease(sorted_data, selectedDisease)
            logging.debug(f"Filtered Data: {sorted_data}")

        # Pagination parameters
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))

        # Paginate data
        start = (page - 1) * per_page
        end = start + per_page
        paginated_data = sorted_data[start:end]

        return jsonify(paginated_data)
    except Exception as e:
        logging.error("An error occurred in get_sorted_data:", exc_info=True)
        return jsonify({"error": str(e)}), 500


def transform_total_counts_for_chart(data):
    chart_data = []
    for item in data:
        # Ensure 'disease' and '0' keys exist
        if "disease" in item and "0" in item:
            transformed_item = {"Disease": item["disease"], "Count": item["0"]}
            chart_data.append(transformed_item)
    return chart_data


def filter_by_disease(sorted_data, selectedDiseases):
    try:
        # Convert selected diseases to a set for efficient lookup and normalize the case
        selectedDiseasesSet = set(disease.strip().lower() for disease in selectedDiseases.split(","))

        # Define a lambda function for filtering
        filter_func = lambda item: item.get("disease", "").lower() in selectedDiseasesSet

        # Use the filter function with the lambda to filter the data
        filtered_data = list(filter(filter_func, sorted_data))

        logging.debug(f"Filtered Data: {filtered_data}")
        return filtered_data
    except Exception as e:
        logging.error("An error occurred in filter_by_disease:", exc_info=True)
        # Decide whether to return the unfiltered data or an empty list in case of an error
        return []  # or return sorted_data if that's preferable



def extract_disease_names(data_file_path):
    # Load the data from the file
    with open(data_file_path, "r") as file:
        data = json.load(file)

    # Extract and return unique disease names
    return list(set(item["disease"] for item in data))


@app.route("/get-disease-names", methods=["GET"])
def get_disease_names():
    data_file_path = os.path.join(current_directory, f"../data/total_counts.json")
    disease_names = extract_disease_names(data_file_path)
    return jsonify(disease_names)


@app.route("/get-chart-data", methods=["GET"])
def get_chart_data():
    category = request.args.get("category", "total")
    selectedWindow = request.args.get("selectedWindow", "total")
    sort_key = request.args.get("sortKey", "disease")
    sort_order = request.args.get("sortOrder", "asc")
    selectedDiseases = request.args.get(
        "selectedDiseases",
        None,
    )

    # Construct the path to the correct data file based on category
    if category == "total":
        data_file_path = os.path.join(current_directory, f"../data/total_counts.json")
    else:
        data_file_path = os.path.join(
            current_directory, f"../data/{selectedWindow}_{category}_counts.json"
        )

    # Load the data from the correct file
    with open(data_file_path, "r") as file:
        category_data = json.load(file)

    # Sort data
    sorted_data = sort_data(category_data, sort_key, sort_order)

    if category == "total_counts":
        sorted_data = transform_total_counts_for_chart(sorted_data)

    # # Check if selectedDiseases is not None and not an empty string
    # if selectedDiseases:
    #     sorted_data = filter_by_disease(sorted_data, selectedDiseases)

    return sorted_data


@app.route("/get-additional-chart-data", methods=["GET"])
def get_additional_chart_data():
    try:
        category = request.args.get("category", "racial")
        sort_key = request.args.get("sortKey", "disease")
        sort_order = request.args.get("sortOrder", "asc")

        # Construct the path to the correct data file based on category
        if category == "total":
            additonal_data_path = os.path.join(
                current_directory, f"../data/percentage_difference_gender.json"
            )
        else:
            additonal_data_path = os.path.join(
                current_directory, f"../data/percentage_difference_{category}.json"
            )

        with open(additonal_data_path, "r") as file:
            additional_data = json.load(file)

        # Sort data
        additional_data = sort_data(additional_data, sort_key, sort_order)

        return jsonify(additional_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/get-temporal-chart-data", methods=["GET"])
def get_temporal_chart_data():
    try:
        category = request.args.get("category", "racial")
        sort_key = request.args.get("sortKey", "disease")
        sort_order = request.args.get("sortOrder", "asc")
        TimeOption = request.args.get("timeOption", "total")

        # Construct the path to the correct data file based on category
        temporal_data_path = os.path.join(
            current_directory, f"../data/{category}_{TimeOption}_counts.json"
        )
        with open(temporal_data_path, "r") as file:
            temporal_data = json.load(file)

        # Sort data
        temporal_data = sort_data(temporal_data, sort_key, sort_order)

        return jsonify(temporal_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
