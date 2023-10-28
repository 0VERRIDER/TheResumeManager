from ..connection import db_cursor, db_con

def create_data(data, callback):
    query = """
        INSERT INTO `job_application` (
            `uuid`,
            `job_number`,
            `employer_name`,
            `job_title`,
            `status`,
            `generated_on`,
            `application_link`
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        db_cursor.execute(query, (
            data['uuid'],
            data['job_number'],
            data['employer_name'],
            data['job_title'],
            data['status'],
            data['generated_on'],
            data['application_link']
        ))

        db_con.commit()
        callback(db_cursor.lastrowid)
    except Exception as e:
        print(e)
        callback(None)