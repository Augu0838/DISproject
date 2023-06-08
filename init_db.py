import os
import psycopg2

# current_directory  = os.getcwd()
# path = os.path.join(current_directory, 'data')

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS Stations;')
cur.execute('CREATE TABLE IF NOT EXISTS Stations(stationId integer PRIMARY KEY,'
    'stationName varchar(60));'
)

cur.execute('DROP TABLE IF EXISTS Users;')
cur.execute('CREATE TABLE IF NOT EXISTS Users(userId SERIAL PRIMARY KEY,'
	'username varchar(60),'
	'password varchar(120),'
	'favoriteStation varchar(60));'
)

cur.execute('DROP TABLE IF EXISTS Measurements;')
cur.execute('CREATE TABLE IF NOT EXISTS Measurements(measurementId SERIAL PRIMARY KEY,'
    'measurementDate date,'
	'stationId integer,'
    'temperature integer);' 
)


cur.execute('COPY Users(username, password, favoriteStation)' 
            'FROM \'/Applications/PostgreSQL 15/data/users.csv\' CSV HEADER;'
            )

cur.execute('COPY Stations(stationId, stationName)' 
            'FROM \'/Applications/PostgreSQL 15/data/stations.csv\' CSV HEADER;')

cur.execute('COPY Measurements(measurementDate, stationId, temperature)'
            'FROM \'/Applications/PostgreSQL 15/data/tw.csv\' CSV HEADER;')

conn.commit()

cur.close()
conn.close()
