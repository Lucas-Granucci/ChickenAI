import os
import json
import requests

api_key = os.environ.get("TBA_API_KEY")

def extract_district_codes(api_key: str, year: int):

    base_url = "https://www.thebluealliance.com/api/v3"

    endpoint = f"/districts/{year}"

    headers = {
        "X-TBA-Auth-Key": api_key
    }

    request_url = base_url + endpoint
    response = requests.get(request_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    cleaned_data = {district['display_name']:district["key"] for district in data}

    return cleaned_data

def main():

    combined_district_data = {}

    print("Extracting district names and codes from The Blue Alliance API...")

    for year in range(2012, 2026):
        district_name_to_code = extract_district_codes(api_key=api_key, year=year)
        combined_district_data[year] = district_name_to_code

    with open('name_to_code.json', 'w') as f:
        json.dump(combined_district_data, f, indent=4)

if __name__ == "__main__":
    main()