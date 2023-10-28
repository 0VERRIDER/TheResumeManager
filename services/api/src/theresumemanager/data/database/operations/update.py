from ..connection import db_cursor, db_con

def update_data(uuid, data, callback):
    query = """
        UPDATE `job_application` SET
            `job_number` = %s,
            `employer_name` = %s,
            `job_title` = %s,
            `status` = %s,
            `generated_on` = %s,
            `application_link` = %s
        WHERE `uuid` = %s
    """

    db_cursor.execute(query, (
        data['job_number'],
        data['employer_name'],
        data['job_title'],
        data['status'],
        data['generated_on'],
        data['application_link'],
        uuid
    ))
    
    db_con.commit()
    callback(db_cursor.rowcount)

# update status and notes
def update_status_data(uuid, status, notes, callback):
    query = """
        UPDATE `job_application` SET
            `status` = %s,
            `notes` = %s
        WHERE `uuid` = %s
    """

    db_cursor.execute(query, (
        status,
        notes,
        uuid
    ))
    
    db_con.commit()
    callback(db_cursor.rowcount)