from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the directory where this script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the data file
data_file_path = os.path.join(current_directory, "../data/processed_data.json")

# Load your data
with open(data_file_path, "r") as file:
    jsonData = json.load(file)


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
    category = request.args.get("category", "total_counts")
    sort_key = request.args.get("sortKey", "disease")
    sort_order = request.args.get(
        "sortOrder", "asc"
    )  # Default to ascending if not provided

    # Extract data based on category
    extracted_data = jsonData[category]

    # Sort data
    sorted_data = sort_data(extracted_data, sort_key, sort_order)

    # Pagination parameters
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    # Paginate data
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = sorted_data[start:end]

    return jsonify(paginated_data)


def transform_for_chart(data, category):
    chart_data = []
    if category == "total_counts":
        for item in data:
            transformed_item = {"Disease": item["disease"], "Total Counts": item["0"]}
            chart_data.append(transformed_item)
    elif category in [
        "window_10_gender_subgroup_counts",
        "window_10_racial_subgroup_counts",
    ]:
        for item in data:
            transformed_item = {"Disease": item["disease"]}
            for key, value in item.items():
                if key != "disease":
                    transformed_item[key.replace("/", " ")] = value
            chart_data.append(transformed_item)
    return chart_data


@app.route("/get-chart-data", methods=["GET"])
def get_chart_data():
    category = request.args.get("category", "total_counts")
    sort_key = request.args.get("sortKey", "disease")
    sort_order = request.args.get("sortOrder", "asc")

    extracted_data = jsonData[category]
    sorted_data = sort_data(extracted_data, sort_key, sort_order)
    chart_data = transform_for_chart(sorted_data, category)
    return jsonify(chart_data)


if __name__ == "__main__":
    app.run(debug=True)
