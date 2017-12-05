import sqlite3
conn = sqlite3.connect('jackbot.db')


# user_id, user_name, command, date_received, status
def create_logs_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
        (user text, command text, date_received datetime, status text)''')
    conn.commit()
    return True


def log_event(user, text, date_received, status):
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)",
            (user, text, date_received, status))
    conn.commit()
    return True

