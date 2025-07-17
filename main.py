import argparse
from leetcode_tracker import fetch_submissions, analyse_topics, export_to_csv
from github_sync import sync_to_github
from notifier import send_reminders


def main():
    #ArgumentParser() creates a parser object.
    parser = argparse.ArgumentParser(description = "LeetSync CLI - Analyse your leetcode progress")
    parser.add_argument("--fetch", action = "store_true",help = "Fetch your Leetcode progress")
    parser.add_argument("--analyse", action = "store_true", help = "Analyse your Leetcode progress")
    parser.add_argument("--sync", action = "store_true", help = "Sync progress to github")
    parser.add_argument("--remind", action = "store_true", help = "Show weak topic reminders")
    parser.add_argument("--export", action = "store_true", help = "Export progress to csv and json file")

    #now actually read the input arguments
    args = parser.parse_args()

    if args.fetch:
        fetch_submissions()
    if args.analyse:
        analyse_topics()
    if args.sync:
        sync_to_github()
    if args.remind:
        send_reminders()
    if args.export:
        export_to_csv()
if __name__ == "__main__":
    #It makes sure your script only runs if it’s directly executed, not imported into another script.
    #runs only if this file is directly executed
    main()