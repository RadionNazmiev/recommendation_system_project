import time
import psycopg2

def wait_for_postgres(host, port, user, password, database, max_attempts=60):
    attempts = 0
    print(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    while attempts < max_attempts:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            conn.close()
            print("PostgreSQL is ready!")
            return
        except psycopg2.OperationalError:
            attempts += 1
            time.sleep(1)
    print("Couldn't connect to PostgreSQL. Exiting.")
    exit(1)

if __name__ == "__main__":
    from config.config import PG_USER, PG_PASS, PG_HOST, PG_PORT, PG_DB

    wait_for_postgres(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASS,
        database=PG_DB
    )
