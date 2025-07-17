import time # this is to use the time() function
import datetime # this is to use the datetime() function
import json
def send_reminders():
    print("[send_reminders] Sending reminders for old problems...")
    #send reminder for problems solved more than 7 days ago or status not accepted
    with open("data/progress.json", "r") as f:
        data = json.load(f)
    count = 0
    color1 = "\033[91m" #red color for the wrong status reminder text
    color2 = "\033[93m" #yellow color for the old problem reminder text
    reset = "\033[0m" #reset color
    timestamp_threshold = time.time() - 7 * 24 * 60 * 60 #time.time() returns the current time in seconds since the epoch, and we subtract 7 days worth of seconds to get the threshold
    for submission in sorted(data, key = lambda x: x["timestamp"]): #sort the submissions by timestamp - older submissions first
        timestamp = int(submission["timestamp"]) #timestamp is in seconds since the epoch
        if timestamp < timestamp_threshold: #if the timestamp is older than the threshold whether it is accepted or not
            count+=1
            timestampstr = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d") #convert timestamp to a human-readable date format
            print(f"{color2}[send_reminders] Reminder: Problem '{submission["title"]} was solved on {timestampstr} but solved more than 7 days ago. Please review it.{reset}")
        elif submission["status"] != 10:
            count+=1
            timestampstr = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d") #convert timestamp to a human-readable date format
            print(f"{color1}[send_reminders] Reminder: Problem '{submission["title"]} was solved on {timestampstr} but not accepted. Please review it.{reset}")

    if count==0:
        print("[send_reminders] No reminders to send. All problems are either accepted or solved within the last 7 days.")



    


