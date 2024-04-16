import sqlite3

conn = sqlite3.connect('my_database.db')
c = conn.cursor()
# ____ Connection established to the database and cursor created. ____

def create_user(first_name, last_name, username, email, password):
    c.execute("INSERT INTO users (FirstName, LastName, Username, Email, Password) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, username, email, password))
    conn.commit()
    return 0

def get_user(username):
    c.execute("SELECT * FROM users WHERE Username = ?", (username,))
    # print(c.fetchone())
    return c.fetchone()

def create_job(userID, jobName, jobDescription, jobLocation, jobSalary):
    c.execute("INSERT INTO jobs (UserID, JobName, JobDescription, JobLocation, JobSalary) VALUES (?, ?, ?, ?, ?)", (userID, jobName, jobDescription, jobLocation, jobSalary))
    conn.commit()

def get_jobs():
    c.execute("SELECT * FROM jobs")
    return c.fetchall() 

def remove_job(jobID):
    c.execute("DELETE FROM jobs WHERE JobID = ?", (jobID,))
    conn.commit()
    
def save_job(userID, jobID):
    c.execute("INSERT INTO saved_jobs (UserID, JobID) VALUES (?, ?)", (userID, jobID))
    conn.commit()
    
def get_saved_jobs(userID):
    c.execute("SELECT j.JobID, j.JobName, j.JobDescription, j.JobLocation, j.JobSalary FROM saved_jobs sj JOIN jobs j ON sj.JobID = j.JobID WHERE sj.UserID = ?", (userID,))
    return c.fetchall()

def remove_saved_job(userID, jobID):
    c.execute("DELETE FROM saved_jobs WHERE UserID = ? AND JobID = ?", (userID, jobID))
    conn.commit()

def apply_job(userID, jobID):
    c.execute("INSERT INTO applications (UserID, JobID) VALUES (?, ?)", (userID, jobID))
    conn.commit()
    
def get_friends(userID):
    c.execute("SELECT u.firstname, u.LastName, u.username, u.email FROM friends f JOIN users u ON f.friendID = u.UserID WHERE f.UserID = ?", (userID,))
    return c.fetchall()

def add_friend(userID, friendUserID):
    c.execute("INSERT INTO friends (UserID, FriendUserID) VALUES (?, ?)", (userID, friendUserID))
    conn.commit()
    
def remove_friend(userID, friendUserID):
    c.execute("DELETE FROM friends WHERE UserID = ? AND FriendUserID = ?", (userID, friendUserID))
    conn.commit()
    
    
def get_messages(userID):
    c.execute("SELECT * FROM messages WHERE ReceiverID = ?", (userID,))
    return c.fetchall()
