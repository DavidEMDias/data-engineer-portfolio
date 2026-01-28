import psycopg2
from api_request import fetch_data

def connect_to_db():
    print("Connecting to the PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            host="db", #Use docker postgres service configs
            port=5432,
            dbname="db",
            user="db_user",
            password="db_password"
        )
        return conn #<connection object at 0x781b8896bb00; dsn: 'user=db_user password=xxx dbname=db host=localhost port=5000', closed: 0>
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise

def check_if_table_exists(cursor):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'dev'
              AND table_name = 'raw_weather_data'
        );
    """)
    return cursor.fetchone()[0]


def create_table(conn):
    print("Ensuring table exists...")

    try:
        cursor = conn.cursor()

        if check_if_table_exists(cursor):
            print("Table already exists. Skipping creation.")
            return

        print("Creating table...")
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_description TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT,
                CONSTRAINT unique_city_time UNIQUE (city, time)
            );
        """)

        conn.commit()
        print("Table was created.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Failed to create table: {e}")
        raise



def insert_records(conn, data):
    print("Inserting weather data into the database...")
    try:
        weather = data['current']
        location = data['location']

        cursor = conn.cursor()
        
        #ID is inserted by postgres
        cursor.execute("""
            INSERT INTO dev.raw_weather_data(
                city,
                temperature,
                weather_description,
                wind_speed,
                time,
                inserted_at,
                utc_offset
            ) VALUES (%s, %s, %s, %s, %s, NOW(), %s)
            ON CONFLICT (city, time) DO NOTHING;
        """,(
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            location['localtime'],
            location['utc_offset']
        ))

        if cursor.rowcount == 0:
            print(
                f"[IDEMPOTENT] Record already exists for "
                f"city='{location['name']}', time='{location['localtime']}'. Skipping insert."
            )
        else:
            print(
                f"[INSERTED] Weather data inserted for "
                f"city='{location['name']}', time='{location['localtime']}'."
            )

        conn.commit()
        #print("Data successfully inserted.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error inserting data into the database: {e}")
        raise

def main():
    try:
        #data = mock_fetch_data()
        data = fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn, data)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally: #Regardless of wether it successed or not. Always executes.
        if 'conn' in locals(): #This checks whether the variable conn exists in the local scope.
            conn.close()
            print("Database connection closed.")

