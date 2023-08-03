import psycopg2
import config


def get_connection():
    """
    Get a connection to the PostgreSQL database using the configuration settings.

    Returns:
        psycopg2.extensions.connection: The PostgreSQL database connection object.

    Raises:
        Exception: If there is an error while connecting to the database.
    """
    try:
        connection = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        return connection
    except psycopg2.Error as e:
        raise Exception("Error: Unable to connect to the database.") from e


def check_table_exists(table_name):
    """
    Check if the given table exists in the PostgreSQL database.

    Args:
        table_name (str): The name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.

    Raises:
        Exception: If there is an error while checking the table existence.
    """
    try:
        with get_connection() as connection, connection.cursor() as cursor:
            query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
            cursor.execute(query)
            return cursor.fetchone()[0]
    except psycopg2.Error as e:
        raise Exception("Error while checking table existence.") from e


def create_user_logins_table():
    """
    Create the 'user_logins' table in the PostgreSQL database if it does not exist.

    Raises:
        Exception: If there is an error while creating the table.
    """
    table_name = 'user_logins'
    if not check_table_exists(table_name):
        try:
            with get_connection() as connection, connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_logins(
                        user_id varchar(128),
                        device_type varchar(32),
                        masked_ip varchar(256),
                        masked_device_id varchar(256),
                        locale varchar(32),
                        app_version integer,
                        create_date date
                    );
                """)
                connection.commit()
        except psycopg2.Error as e:
            raise Exception("Error while creating user_logins table.") from e


def write_to_postgres(data):
    """
    Write data to the 'user_logins' table in the PostgreSQL database.

    Args:
        data (list of dict): List of records to insert into the table.

    Raises:
        Exception: If there is an error while writing to the database.
    """
    try:
        with get_connection() as connection, connection.cursor() as cursor:
            for record in data:
                record['create_date'] = record['create_date'].strftime('%Y-%m-%d')
                cursor.execute("""
                    INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    record['user_id'],
                    record['device_type'],
                    record['masked_ip'],
                    record['masked_device_id'],
                    record['locale'],
                    record['app_version'],
                    record['create_date']
                ))
            connection.commit()
    except Exception as e:
        raise Exception(f"Error while writing to Postgres: {str(e)}") from e
