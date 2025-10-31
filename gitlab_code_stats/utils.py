import json
import os
import sys

def load_config(filename="config.json"):
    """Load configuration and validate."""
    if not os.path.exists(filename):
        print(f"❌ Config file '{filename}' not found.")
        sys.exit(1)

    with open(filename, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            print("❌ Config file contains invalid JSON.")
            sys.exit(1)

    # Required fields
    for key in ["api_url", "private_token", "start_date", "end_date", "users"]:
        if key not in config:
            print(f"❌ Config missing required field: {key}")
            sys.exit(1)

    # Remove blank users
    config["users"] = [u for u in config.get("users", []) if u.strip()]
    if not config["users"]:
        print("❌ User list is empty or contains only blank entries.")
        print("Please add at least one valid GitLab username in 'users' in config.json.")
        sys.exit(1)

    # Max lines per commit
    config["max_lines_per_commit"] = config.get("max_lines_per_commit", 1000)

    # CSV output file
    config["output_filename"] = config.get("output_filename", "gitlab_code_stats.csv")

    return config
