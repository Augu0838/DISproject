import os
import psycopg2

# current_directory  = os.getcwd()
# path = os.path.join(current_directory, 'data')

path = '/Applications/PostgreSQL 15/'

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Comment in if database does not exist
##cur.execute('CREATE DATABASE flash_db;')

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS Stations;')
cur.execute('CREATE TABLE IF NOT EXISTS Stations(stationId integer PRIMARY KEY,'
    'stationName varchar(60));'
)

cur.execute('DROP TABLE IF EXISTS Users;')
cur.execute('CREATE TABLE IF NOT EXISTS Users(userId SERIAL PRIMARY KEY,'
	'username varchar(60),'
	'password varchar(120),'
	'favoriteStation integer);'
)

cur.execute('DROP TABLE IF EXISTS Measurements;')
cur.execute('CREATE TABLE IF NOT EXISTS Measurements(measurementId SERIAL PRIMARY KEY,'
    'measurementDate date,'
	'stationId integer,'
    'temperature integer);' 
)


cur.execute('COPY Users(username, password, favoriteStation)' 
            f'FROM \'{path}/data/users.csv\' CSV HEADER;'
            )

cur.execute('COPY Stations(stationId, stationName)' 
            f'FROM \'{path}/data/stations.csv\' CSV HEADER;')

cur.execute('COPY Measurements(measurementDate, stationId, temperature)'
            f'FROM \'{path}/data/tw.csv\' CSV HEADER;')

conn.commit()

cur.close()
conn.close()

