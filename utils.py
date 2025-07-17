def json_to_csv(json_file, csv_file):
    import json
    import csv

    with open(json_file, 'r') as jf:
        data = json.load(jf)

    with open(csv_file, 'w', newline='') as cf:
        writer = csv.writer(cf)

        # Write header
        writer.writerow(data[0].keys())

        # Write data
        for entry in data:
            writer.writerow(entry.values())

def format_submission_data(submission):
    return {
        "title": submission.get("title"),
        "status": submission.get("status"),
        "date": submission.get("date"),
        "topic": submission.get("topic"),
        "difficulty": submission.get("difficulty"),
    }