import argparse
from gitlab_code_stats.main_logic import collect_stats
from gitlab_code_stats.web_api import start_web

def main():
    parser = argparse.ArgumentParser(description="GitLab Code Stats Tool")
    parser.add_argument('--web', action='store_true', help='Start web API')
    args = parser.parse_args()

    if args.web:
        start_web()
    else:
        collect_stats()

if __name__ == "__main__":
    main()
