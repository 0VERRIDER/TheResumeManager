from mysql.connector import connect
from ...resources.config import env

import time  # Import time for retry delays

max_retries = 3  # Set maximum number of retries
retry_delay = 5  # Set retry delay in seconds

for attempt in range(max_retries):
    try:
        db_con = connect(
            host=env.DATABASE_HOST,
            port=env.DATABASE_PORT,
            user=env.DATABASE_USER,
            password=env.DATABASE_PASSWORD,
            database=env.DATABASE_NAME
        )

        db_cursor = db_con.cursor()

        # Create table using prepared statement for security
        query = """
            CREATE TABLE IF NOT EXISTS `job_application` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `uuid` varchar(225) NOT NULL,
                `job_number` varchar(225) NOT NULL,
                `employer_name` varchar(225) NOT NULL,
                `job_title` varchar(225) NOT NULL,
                `status` enum('PENDING','REJECTED','ACCEPTED') NOT NULL,
                `generated_on` date NOT NULL,
                `application_link` varchar(225) NOT NULL,
                `notes` varchar(225),
                PRIMARY KEY (`id`),
                UNIQUE(`uuid`)
            );
        """
        db_cursor.execute(query)

        print("Table created successfully!")
        break  # Exit the loop if connection and table creation succeed

    except Exception as e:
        print(f"Connection attempt {attempt+1} failed: {e}")

        if attempt < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    finally:
        if db_con:  # Close the connection if it was established
            db_cursor.close()
            db_con.close()

if attempt == max_retries - 1:
    print("All connection attempts failed.")

