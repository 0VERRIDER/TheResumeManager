from ..connection import db_cursor, db_con

def delete_data(uuid, callback):
    query = """
        DELETE FROM `job_application` WHERE `uuid` = %s
    """

    db_cursor.execute(query, (uuid,))

    db_con.commit()
    callback(db_cursor.rowcount)