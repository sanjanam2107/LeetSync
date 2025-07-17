import subprocess # this is to run shell commands from python scripts


def sync_to_github():
    print("[sync_to_github] Syncing progress to Github...")

    try:
        is_git_repo = subprocess.run(["git","rev-parse", "--is-inside-work-tree"],stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL,check = False).returncode == 0 #check is false means it won't raise an error if the command fails, and returncode will be 0 if the command was successful, otherwise it will be non-zero
        #rev-parse is a git command that can be used to check if the current directory is a git repository and --is-inside-work-tree returns true if it is a git repository
        if not is_git_repo:
            print("[sync_to_github] Not a git repository. Will initialise a git repo first.")
            subprocess.run(["git","init"], check = True)

        # Check if the remote origin is set
        remotes = subprocess.run(["git", "remote"], capture_output=True, text = True)
        if "origin" not in remotes.stdout:
            print("[sync_to_github] No remote origin found.")
            remote_url = input("[sync_to_github] Please enter url:")
            subprocess.run(["git", "remote", "add","origin", remote_url], check = True) 

        else:
            #origin is there but is it right?
            url = subprocess.run(["git","remote","get-url", "origin"], check = True, capture_output=True, text=True) #get-url is a git command that returns the url of the remote origin
            print("[sync_to_github] Is this your GitHub repository URL?" + url.stdout.strip())
            print("[sync_to_github] Y/N")
            answer = input("Your Choice:").strip().lower()     
            if answer != "y":
                remote_url = input("[sync_to_github] Please enter url:")
                subprocess.run(["git", "remote", "set-url", "origin", remote_url], check = True)
            else:
                print("[sync_to_github] Remote origin is already set to the correct URL.")


            
        # Run the git commands to add, commit, and push changes
        subprocess.run(["git","add","data/progress.json","data/progress.csv"], check = True) #arguments of the commands are passed as a list and check = True raises an error if the command fails
        subprocess.run(["git", "commit", "-m", "Update progress"], check = True) 
        subprocess.run(["git", "push","origin","main"], check = True)
        print("[sync_to_github] Successfully synced progress to Github.")
    except subprocess.CalledProcessError as e:
        print(f"[sync_to_github] An error occurred while syncing to GitHub: {e}")
    except Exception as e:
        print(f"[sync_to_github] An unexpected error occurred: {e}")
    
