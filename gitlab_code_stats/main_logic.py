import requests
import csv
from dateutil.parser import parse
from .utils import load_config


def collect_stats(
    start_date=None, end_date=None, users=None, config_path="config.json"
):
    """Collect GitLab commit stats and save to CSV"""
    config = load_config(config_path)
    START_DATE = start_date or config["start_date"]
    END_DATE = end_date or config["end_date"]
    USERS = users or config["users"]
    OUTPUT_FILE = config["output_filename"]
    MAX_LINES = config["max_lines_per_commit"]
    API_URL = config["api_url"]
    TOKEN = config["private_token"]
    HEADERS = {"PRIVATE-TOKEN": TOKEN}

    result_data = {}

    def fetch_paginated_data(url, params=None):
        data_list, page = [], 1
        params = params or {}
        while True:
            resp = requests.get(
                url, headers=HEADERS, params={**params, "page": page, "per_page": 100}
            )
            if resp.status_code != 200:
                print(f"Request failed: {url}, {resp.text}")
                return []
            data = resp.json()
            if not data:
                break
            data_list.extend(data)
            page += 1
        return data_list

    if USERS is None or len(USERS) == 0 :
        users_list = fetch_paginated_data(f"{API_URL}/users")
        USERS = [user["username"] for user in users_list]
    for username in USERS:
        commit_count = total_additions = total_deletions = total_lines = 0
        users_info = fetch_paginated_data(f"{API_URL}/users", {"username": username})
        if not users_info:
            print(f"⚠ User '{username}' not found in GitLab.")
            continue
        user_id = users_info[0]["id"]

        events = fetch_paginated_data(
            f"{API_URL}/users/{user_id}/events",
            {"after": START_DATE, "before": END_DATE, "action": "pushed"},
        )

        for event in events:
            project_id = event.get("project_id")
            push_data = event.get("push_data", {})
            commit_to = push_data.get("commit_to")
            commit_shas = [commit_to] if commit_to else []

            for sha in commit_shas:
                # Get commit stats
                resp = requests.get(
                    f"{API_URL}/projects/{project_id}/repository/commits/{sha}",
                    headers=HEADERS,
                )
                if resp.status_code != 200:
                    continue
                stats = resp.json().get("stats", {})
                additions = min(stats.get("additions", 0), MAX_LINES)
                deletions = min(stats.get("deletions", 0), MAX_LINES)
                total = min(stats.get("total", 0), MAX_LINES)

                total_additions += additions
                total_deletions += deletions
                total_lines += total
                commit_count += 1

        if commit_count > 0:
            result_data[username] = [
                username,
                username,
                commit_count,
                total_lines,
                total_additions,
                total_deletions,
            ]

    if result_data:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Username",
                    "Name",
                    "CommitCount",
                    "TotalLines",
                    "Additions",
                    "Deletions",
                ]
            )
            for row in result_data.values():
                writer.writerow(row)
        print(f"✅ Stats saved to {OUTPUT_FILE}")
