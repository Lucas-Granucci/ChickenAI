import os
import json
import requests

api_key = os.environ.get("TBA_API_KEY")

def extract_team_names(api_key: str, year: int, page_num: int):

    base_url = "https://www.thebluealliance.com/api/v3"

    endpoint = f"/teams/{year}/{page_num}/simple"

    headers = {
        "X-TBA-Auth-Key": api_key
    }

    request_url = base_url + endpoint
    response = requests.get(request_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    cleaned_data = {team['nickname']:team["team_number"] for team in data}

    return cleaned_data

def main():

    combined_team_data = {}

    i = 0
    total_count = 0

    print("Extracting team names and numbers from The Blue Alliance API...")
    while True:
        team_num_data = extract_team_names(api_key=api_key, year=2024, page_num=i)

        if team_num_data == {}:
            break
        else:
            combined_team_data.update(team_num_data)
            total_count += len(team_num_data)
            print(f"Page {i} done. Total count: {total_count}")
            i += 1

    with open('name_to_number.json', 'w') as f:
        json.dump(combined_team_data, f, indent=4)

if __name__ == "__main__":
    main()