import json
import requests
import zipfile
import io


def download_and_extract_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            for zipinfo in thezip.infolist():
                with thezip.open(zipinfo) as thefile:
                    return json.load(thefile)
    else:
        print("Failed to download file")
        return None


def extract_brand_and_generic_names(data):
    brand_and_generic_names = []
    for item in data["results"]:
        brand_name = item.get("brand_name", "Unknown")
        generic_name = item.get("generic_name", "Unknown")
        brand_and_generic_names.append((brand_name, generic_name))
    return brand_and_generic_names


if __name__ == "__main__":
    # URL of the ZIP file
    url = "https://download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip"

    # Download and extract JSON data
    data = download_and_extract_json(url)

    if data:
        # Extract brand and generic names
        extracted_data = extract_brand_and_generic_names(data)

        # Save the extracted data to a tsv
        with open("Debug_Data/extracted_data.tsv", "w") as file:
            for brand, generic in extracted_data:
                file.write(f"{brand}\t{generic}\n")

        # Print the first extracted data as a sample
        for brand, generic in extracted_data:
            print(f"Brand Name: {brand}, Generic Name: {generic}")
            break
    else:
        print("No data was extracted.")
