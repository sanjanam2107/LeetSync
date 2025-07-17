
import requests #used to send http requests to graphql API endpoint of Leetcode
import json #to handle saving and loading data in .json format
import os #to handle file paths and directories
import collections
from collections import defaultdict
import csv #to export data to CSV format

with open("config.json") as f:#default is read mode
    config = json.load(f) #load the JSON data from the file into a Python dictionary
    session_cookie = config["leetcode_session"] #get the session cookie from the config
    #session_cookie is used to authenticate the requests to Leetcode API
    leetcode_username = config["leetcode_username"]

with open("data/progress.json", "r") as f:
    data = json.load(f)

def fetch_submissions():
    print("[fetch_submissions] Fetching submissions from Leetcode...")
    #[] to show where the output is coming from
    headers = {
        "Content-Type": "application/json", #to specify the type of data being sent through the post request
        "Cookie": f"LEETCODE_SESSION={session_cookie}"
    }

    query = {
        "operationName": "recentSubmissionList",
        "variables" : {
            "username" : leetcode_username,
            "limit":20, #number of submissions to fetch
        },
        "query": """ #3 quotes means multi-line string in Python
        query recentSubmissionList($username: String!, $limit: Int!) { #query operationName with variables
            recentSubmissionList(username: $username, limit: $limit) { #actual query to fetch recent submissions
                status
                lang
                timestamp
                title
                titleSlug                                      #slug means a URL-friendly version of the title for example, "two-sum" for "Two Sum"
            }
        }
       """
    }

    response = requests.post("https://leetcode.com/graphql", headers=headers, json=query) #send a POST request to the GraphQL endpoint with headers and query

    if response.status_code != 200:
        print(f"[fetch_submissions] Error fetching submissions: {response.status_code} - {response.text}")
        return
    submissions = response.json()["data"]["recentSubmissionList"] 
    os.makedirs("data", exist_ok = True) #create a directory named "data" if it doesn't exist
    with open("data/progress.json","w") as f:
        json.dump(submissions, f, indent = 4) #json.dump() writes the submissions data to a file named "progress.json" in the "data" directory with an indentation of 4 spaces for better readability

    print(f"[fetch_submissions] Fetched {len(submissions)} submissions!")

def analyse_topics():
    print("[analyse_topics] Analysing submissions...")
    topics = defaultdict(int) #defaultdict is a subclass of dict that returns a default value for non-existent keys, here it returns 0 for int
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={session_cookie}"
    }
    unique_submissions = {} #to store unique submissions by titleSlug

    for submission in data:
        slug = submission["titleSlug"]
        if slug not in unique_submissions and submission["status"]== 10: #status 10 means accepted
            unique_submissions[slug] = submission

    for submission in unique_submissions.values():
        query = {
            "operationName": "getQuestionTags",
            "variables": {
                "titleSlug": submission["titleSlug"]
            },
            "query": """ #multi-line string for the GraphQL query
            query getQuestionTags($titleSlug: String!) {
                question(titleSlug: $titleSlug) { #fetching question details by titleSlug where question is the name of the backend resolver
                    topicTags { #topicTags is a field in the question object that contains the tags for the question
                        name    #name of the topic tag
                    }
                }
            }
            """
        }
        response = requests.post("https://leetcode.com/graphql", headers = headers, json = query) #send a POST request to the GraphQL endpoint with headers and query
        if response.status_code!=200:
            print(f"[analyse_topics] Error fetching tags for {submission['title']}: {response.status_code} - {response.text}")
            continue
        tags = response.json()["data"]["question"]["topicTags"] #extracting the topic tags
        submission["tags"] = [tag["name"] for tag in tags] #adding the tags to the submission dictionary but wont be saved to progress.json file
        for tag in tags:
            topics[tag["name"]] += 1

    print(f"[analyse_topics] Most solved topics:")
    for topic,count in sorted(topics.items(), key = lambda x: x[1], reverse = True)[:5]:# sort the topics by count in descending order and take the top 5. also: lambda x: -x[1] would also work
        print(f"{topic}: {count} solved")
    
    print("\n[analyse_topics] Weakest topics (solved < 5 times):")
    for topic,count in sorted(topics.items(), key = lambda x: x[1]):
        if count < 5:
            print(f"{topic}: {count} solved")
    print("[analyse_topics] Analysis complete!")
    
    with open("data/progress_accepted.json", "w") as f:
        json.dump(list(unique_submissions.values()),f, indent = 4) #save the updated progress.json file with the tags added to each submission



def export_to_csv():
    print("[export_to_csv] Exporting progress to CSV...")
    os.makedirs("data", exist_ok=True) #create a directory named "data" if it doesn't exist
    with open("data/progress_accepted.json", "r") as f:
        data = json.load(f) #load the JSON data from the file into a Python dictionary

    with open("data/progress.csv", "w", newline = "") as f: # open the CSV file in write mode with newline = "" to avoid extra blank lines
        writer = csv.writer(f) #.writer() creates a writer object that converts the data into a delimited string. 
        #delimited string means that the data is separated by a delimiter, which is a comma in this case
        writer.writerow(["Title", "Slug", "Language", "Status", "Timestamp", "Tags"])
        for submission in data:
            writer.writerow(
                [
                    submission["title"],
                    submission["titleSlug"],
                    submission["lang"],
                    submission["status"],
                    submission["timestamp"],
                    ",".join(submission["tags"] if "tags" in submission else []) #join the tags with a comma if they exist, otherwise an empty list
                ]
            )
        print("[export_to_csv] Exported progress to data/progress.csv")


    
        


