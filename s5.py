import sqlite3
import re 
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')

fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox.txt'
fh = open(fname)
pattern = re.compile(r'^From: .\S+@(\S+)')
for line in fh:
    # Your code there
    if pattern.findall(line):
        org = pattern.findall(line)[0]
    # Get domain name - org variable
        print org
        cur.execute('SELECT count FROM Counts WHERE email = ? ', (org, ))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO Counts (email, count) 
                    VALUES ( ?, 1 )''', ( org, ) )
        else : 
            cur.execute('UPDATE Counts SET count=count+1 WHERE email = ?', 
                (org, ))
        # This statement commits outstanding changes to disk each 
        # time through the loop - the program can be made faster 
        # by moving the commit so it runs only after the loop completes
        conn.commit()

# https://www.sqlite.org/lang_select.html
# Your code there
# Make your sql request - get top 10 rows ordered by count
# sqlstr = 'SELECT ... '
sqlstr = 'SELECT * FROM Counts ORDER BY Counts.count DESC LIMIT 10'

print
print "Counts:"
for row in cur.execute(sqlstr) :
    print row[0], row[1]
    # Your code there
    # Print domain and count

cur.close()

