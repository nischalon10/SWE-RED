import sqlite3

conn = sqlite3.connect('my_database.db')
c = conn.cursor()
# ____ Connection established to the database and cursor created. ____



# c.execute('''CREATE TABLE users 
#             (UserID INTEGER PRIMARY KEY, FirstName text, LastName text, Username text, Email text, Password text)''')
# conn.commit()

# c.execute('''CREATE TABLE jobs 
#             (JobID INTEGER PRIMARY KEY, UserID INTEGER, JobName text, JobDescription text, JobLocation text, JobSalary text)''')
# conn.commit()

# c.execute('''CREATE TABLE saved_jobs
#             (SavedID INTEGER PRIMARY KEY, UserID INTEGER, JobID INTEGER)''')
# conn.commit()
# c.execute('''CREATE TABLE applications
#             (ApplicationID INTEGER PRIMARY KEY, UserID INTEGER, JobID INTEGER)''')
# conn.commit()

# c.execute('''CREATE TABLE friends
#             (FriendID INTEGER PRIMARY KEY, UserID INTEGER, FriendUserID INTEGER)''')
# conn.commit()

# c.execute('''CREATE TABLE messages
#             (MessageID INTEGER PRIMARY KEY, SenderID INTEGER, ReceiverID INTEGER, MessageContent text, MessageDate text, Seen boolean)''')
# conn.commit()

# c.execute('''ALTER TABLE users
#              ADD COLUMN tier TEXT DEFAULT 'silver';''')
# conn.commit()

conn.close()