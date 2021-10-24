import sqlite3

conn = sqlite3.connect('test1.db')
cursor = conn.cursor()

cursor.execute('CREATE VIRTUAL TABLE vtest1 using fts5(name, uri, duration_ms, artists, album)')
cursor.execute('INSERT INTO test1 VALUES (?, ?, ?, ?, ?)', ("testSong", "testURI", 180000, "artist1", "album1"))

cursor.execute('SELECT * FROM vtest1 WHERE name=:name', {'name': 'testSong'})
print(cursor.fetchall())

conn.close()