import sqlite3

# Create a connection and a cursor for SQLite
conn = sqlite3.connect('balances.db')
cursor = conn.cursor()

# Execute a SELECT statement to retrieve data
cursor.execute('SELECT * FROM accounts')
data = cursor.fetchall()

# Print the data
for row in data:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()