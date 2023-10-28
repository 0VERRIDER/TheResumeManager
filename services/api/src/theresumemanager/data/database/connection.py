from mysql.connector import connect
from ...resources.config import env

db_con = connect(
    host=env.DATABASE_HOST,
    port=env.DATABASE_PORT,
    user=env.DATABASE_USER,
    password=env.DATABASE_PASSWORD,
    database=env.DATABASE_NAME
)

db_cursor = db_con.cursor()

# create table
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
