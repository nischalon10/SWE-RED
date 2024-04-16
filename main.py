from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator
import os
import db
import pandas as pd

def clear_screen(): 
    _ = os.system('cls') if os.name == 'nt' else os.system('clear')

def welcome():
    welcomeAction = inquirer.select(
        message="Welcome to InCollege App",
        choices=["Login", "Sign-Up", "Exit"],
        ).execute()
    print(welcomeAction)
    return welcomeAction

def create_user_account():
    firstName = inquirer.text(message="Enter your first name:").execute()
    lastName = inquirer.text(message="Enter your last name:").execute()
    username = inquirer.text(message="Enter your username:").execute()
    email = inquirer.text(message="Enter your email:").execute()
    password = inquirer.secret(
                                message="Create a new password:",
                                transformer=lambda _: "[hidden]",
                                validate=PasswordValidator(length=8, cap=True, special=True, number=True, message="Make sure to read the password requirements below"),
                                long_instruction="Password must be at least 8 characters long, contain a capital letter, a special character, and a number."
                            ).execute()
    password2 = inquirer.secret(
                                message="Re-enter password:",
                                transformer=lambda _: "[hidden]",
                                validate=lambda text: text == password,
                                long_instruction="Passwords do not match. Please try again."
                            ).execute()
    db_result = db.create_user(firstName, lastName, username, email, password2)
    if db_result == 0: # User Successfully Created
        print("User created successfully.")
    else:
        print("Unable to create user. Try again.")

def login():
    for _ in range(3):
        username = inquirer.text(message="Enter your username:").execute()
        user = db.get_user(username)
        if user is not None:
            password = inquirer.secret(
                                        message="Enter your password:",
                                        transformer=lambda _: "[hidden]",
                                    ).execute()
            if password == user[5]:
                print("Login successful.")
                return user[0]
        print("Invalid username or password. Try again.")
    print("Too many failed attempts. Please try again later.")

def accessJobs(userID):
    while True:
        clear_screen()
        jobs = db.get_jobs()
        jobs_df = pd.DataFrame(jobs, columns=["JobID", "UserID", "JobName", "JobDescription", "JobLocation", "JobSalary"])
        print(jobs_df)
        print("\n")
        action = inquirer.select(
            message="Job search/Internship",
            choices=[
                "View a job",
                "View saved jobs",
                "Post a job",
                "Remove a job",
                "Save a job",
                "Apply for a job",
                "Return to main menu"
            ],
        ).execute()
        if action == "Return to main menu":
            break
        elif action == "View a job":
            job_id = inquirer.text(message="Enter the job ID to view the job details:").execute()
            if job_id == "":
                continue
            job = jobs_df[jobs_df["JobID"] == int(job_id)]
            print("\n")
            print(job["JobName"].values[0])
            print(job["JobLocation"].values[0])
            print(job["JobSalary"].values[0])
            print("\n")
            print(job["JobDescription"].values[0])
            print("\n")
            input("Press Enter to continue...")
        elif action == "Post a job":
            jobName = inquirer.text(message="Enter the job name:").execute()
            jobDescription = inquirer.text(message="Enter the job description:").execute()
            jobLocation = inquirer.text(message="Enter the job location:").execute()
            jobSalary = inquirer.text(message="Enter the job salary:").execute()
            db.create_job(userID, jobName, jobDescription, jobLocation, jobSalary)
            print("Job posted successfully.")
            input("Press Enter to continue...")
        elif action == "Remove a job":
            job_id = inquirer.text(message="Enter the job ID to remove from listing:").execute()
            if int(job_id) > len(jobs_df):
                print("Invalid job ID.")
                continue
            job = jobs_df[jobs_df["JobID"] == int(job_id)]
            if job["UserID"].values[0] == userID:
                db.remove_job(int(job_id))
            else:
                print("You do not have permission to remove this job.")
            input("Press Enter to continue...")
        elif action == "Save a job":
            job_id = inquirer.text(message="Enter the job ID to save:").execute()
            if int(job_id) > len(jobs_df):
                print("Invalid job ID.")
                continue
            job = jobs_df[jobs_df["JobID"] == int(job_id)]
            db.save_job(userID, int(job_id))
            print("Job saved successfully.")
            input("Press Enter to continue...")
        elif action == "Apply for a job":
            job_id = inquirer.text(message="Enter the job ID to apply:").execute()
            if int(job_id) > len(jobs_df):
                print("Invalid job ID.")
                continue
            job = jobs_df[jobs_df["JobID"] == int(job_id)]
            db.apply_job(userID, int(job_id))
            print("Job applied successfully.")
            input("Press Enter to continue...")
        elif action == "View saved jobs":
            saved_jobs = db.get_saved_jobs(userID)
            saved_jobs_df = pd.DataFrame(saved_jobs, columns=["JobID", "JobName", "JobDescription", "JobLocation", "JobSalary"])
            print(saved_jobs_df)
            print("\n")
            input("Press Enter to continue...")
        else:
            continue

def accessFriends(userID):
    while True:
        clear_screen()
        action = inquirer.select(
            message="Friends",
            choices=[
                "View friends",
                "Add a friend",
                "Remove a friend",
                "Return to main menu"
            ],
        ).execute()
        if action == "Return to main menu":
            break
        elif action == "View friends":
            friends = db.get_friends(userID)
            friends_df = pd.DataFrame(friends, columns=["FirstName", "LastName", "Username", "Email"])
            print(friends_df)
            print("\n")
            input("Press Enter to continue...")
        elif action == "Add a friend":
            friend_username = inquirer.text(message="Enter the username of the friend you want to add:").execute()
            friend = db.get_user(friend_username)
            if friend is not None:
                db.add_friend(userID, friend[0])
                print("Friend added successfully.")
            else:
                print("Friend not found.")
            input("Press Enter to continue...")
        elif action == "Remove a friend":
            friend_username = inquirer.text(message="Enter the username of the friend you want to remove:").execute()
            friend = db.get_user(friend_username)
            if friend is not None:
                db.remove_friend(userID, friend[0])
                print("Friend removed successfully.")
            else:
                print("Friend not found.")
            input("Press Enter to continue...")
        else:
            continue

def accessMessages(userID):
    action = inquirer.select(
        message="Message management",
        choices=[
            "Send a message",
            "View messages",
            "Return to main menu"
        ],
    ).execute()
    if action == "Return to main menu":
        return
    elif action == "Send a message":
        friend_username = inquirer.text(message="Enter the username of the friend you want to message:").execute()
        friend = db.get_user(friend_username)
        if friend is not None:
            message = inquirer.text(message="Enter your message:").execute()
            db.send_message(userID, friend[0], message)
            print("Message sent successfully.")
        else:
            print("Friend not found.")
        input("Press Enter to continue...")
    elif action == "View messages":
        messages = db.get_messages(userID)

def use_app(userID):
    while True:
        clear_screen()
        action = inquirer.select(
            message="Main Menu",
            choices=[
                "Job search/Internship", 
                "InCollege Important Links", 
                "Friends",
                "Tier check",
                "Message management",
                "Notifications",
                "Log out"
            ],
        ).execute()
        if action == "Log out":
            break
        elif action == "Job search/Internship":
            accessJobs(userID)
        elif action == "InCollege Important Links":
            print("InCollege Important Links")
        elif action == "Friends":
            accessFriends(userID)
        elif action == "Tier check":
            print("Tier check")
        elif action == "Message management":
            accessMessages(userID)
        elif action == "Notifications":
            print("Notifications")
        else:
            continue


if __name__ == "__main__":
    while True:
        clear_screen()
        welcomeAction = welcome()
        if welcomeAction == "Login":
            user = login()
            if user is not None:
                use_app(user)
            else:
                print("Unable to login. Try again.")
                input("Press Enter to go to main menu...")
        elif welcomeAction == "Sign-Up":
            create_user_account()
            print("Select login from the main menu to login.")
            input("Press Enter to go to main menu...")
        else:
            break