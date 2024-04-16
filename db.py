import sqlite3

conn = sqlite3.connect('my_database.db')
c = conn.cursor()
# ____ Connection established to the database and cursor created. ____

def create_user(first_name, last_name, username, email, password):
    c.execute("INSERT INTO users (FirstName, LastName, Username, Email, Password) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, username, email, password))
    conn.commit()
    return 0

def get_user(username):
    c.execute("SELECT FirstName, LastName, Username, Email FROM users WHERE Username = ?", (username,))
    return c.fetchone()

def get_userID(username):
    c.execute("SELECT UserID FROM users WHERE Username = ?", (username,))
    return c.fetchone()

def get_users():
    c.execute("SELECT UserID, FirstName, LastName, Username, Email FROM users")
    return c.fetchall()

def create_job(userID, jobName, jobDescription, jobLocation, jobSalary):
    c.execute("INSERT INTO jobs (UserID, JobName, JobDescription, JobLocation, JobSalary) VALUES (?, ?, ?, ?, ?)", (userID, jobName, jobDescription, jobLocation, jobSalary))
    conn.commit()

def get_jobs_display():
    c.execute("SELECT JobID, JobName, JobLocation, JobSalary FROM jobs")
    return c.fetchall() 

def get_jobs():
    c.execute("SELECT * FROM jobs")
    return c.fetchall() 

def get_job(jobID):
    c.execute("SELECT JobID FROM jobs WHERE JobID = ?", (jobID,))
    return c.fetchall() 

def remove_job(jobID):
    c.execute("DELETE FROM jobs WHERE JobID = ?", (jobID,))
    conn.commit()
    
def save_job(userID, jobID):
    c.execute("INSERT INTO saved_jobs (UserID, JobID) VALUES (?, ?)", (userID, jobID))
    conn.commit()
    
def get_saved_jobs(userID):
    c.execute("SELECT j.JobID, j.JobName, j.JobLocation, j.JobSalary FROM saved_jobs sj JOIN jobs j ON sj.JobID = j.JobID WHERE sj.UserID = ?", (userID,))
    return c.fetchall()

def remove_saved_job(userID, jobID):
    c.execute("DELETE FROM saved_jobs WHERE UserID = ? AND JobID = ?", (userID, jobID))
    conn.commit()

def apply_job(userID, jobID):
    c.execute("INSERT INTO applications (UserID, JobID) VALUES (?, ?)", (userID, jobID))
    conn.commit()
    
def get_friends(userID):
    c.execute("SELECT DISTINCT u.firstname, u.LastName, u.username, u.email FROM friends f JOIN users u ON f.friendUserID = u.UserID WHERE f.UserID = ?", (userID,))
    return c.fetchall()

def add_friend(userID, friendUserID):
    c.execute("INSERT INTO friends (UserID, FriendUserID) VALUES (?, ?)", (userID, friendUserID))
    conn.commit()
    
def remove_friend(userID, friendUserID):
    c.execute("DELETE FROM friends WHERE UserID = ? AND FriendUserID = ?", (userID, friendUserID))
    conn.commit()
    
    
def get_messages(userID):
    c.execute("""
        SELECT m.MessageID, m.MessageDate, u.Username as Sender, m.MessageContent as 'Message Content', m.Seen 
        FROM messages m 
        JOIN users u ON m.SenderID = u.UserID 
        WHERE m.ReceiverID = ?
    """, (userID,))
    return c.fetchall()

def get_unread_messages(userID):
    c.execute("""
        SELECT m.MessageID, m.MessageDate, u.Username as Sender, m.MessageContent as 'Message Content'
        FROM messages m 
        JOIN users u ON m.SenderID = u.UserID 
        WHERE m.ReceiverID = ? AND m.Seen = 0
    """, (userID,))
    return c.fetchall()

def get_user(friend_username):
    c.execute("SELECT * FROM users WHERE Username = ?", (friend_username,))
    return c.fetchone()

def send_message(userID, reciverID, message):
    c.execute("INSERT INTO messages (SenderID, ReceiverID, MessageContent, MessageDate, Seen) VALUES (?, ?, ?, datetime('now'), 0)", (userID, reciverID, message))
    conn.commit()
    
def mark_message_as_seen(userID, messageID):
    c.execute("UPDATE messages SET Seen = 1 WHERE ReceiverID = ? AND MessageID = ?", (userID, messageID))
    conn.commit()