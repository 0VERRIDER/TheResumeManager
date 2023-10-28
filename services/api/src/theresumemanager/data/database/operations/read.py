from ..connection import db_cursor

def read_data(uuid, callback):
    query = """
        SELECT * FROM `job_application` WHERE `uuid` = %s
    """

    db_cursor.execute(query, (uuid,))

    columns = [column[0] for column in db_cursor.description]
    data = db_cursor.fetchone()
    result = {columns[i]: data[i] for i in range(len(columns))} if data else None

    callback(result)

    return result

# def read_data(callback):
#     query = """
#         SELECT * FROM `job_application`
#     """

#     db_cursor.execute(query)

#     callback(db_cursor.fetchall())
