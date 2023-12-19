from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import json
import os

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
    category = request.args.get("category", "total")
    selectedWindow = request.args.get("selectedWindow", "total")
    sort_key = request.args.get("sortKey", "disease")
    sort_order = request.args.get("sortOrder", "asc")

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

    # Pagination parameters
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    # Paginate data
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = sorted_data[start:end]

    return jsonify(paginated_data)


def transform_total_counts_for_chart(data):
    chart_data = []
    for item in data:
        # Ensure 'disease' and '0' keys exist
        if "disease" in item and "0" in item:
            transformed_item = {"Disease": item["disease"], "Count": item["0"]}
            chart_data.append(transformed_item)
    return chart_data


@app.route("/get-chart-data", methods=["GET"])
def get_chart_data():
    category = request.args.get("category", "total")
    selectedWindow = request.args.get("selectedWindow", "total")
    sort_key = request.args.get("sortKey", "disease")
    sort_order = request.args.get("sortOrder", "asc")

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


if __name__ == "__main__":
    app.run(debug=True)
