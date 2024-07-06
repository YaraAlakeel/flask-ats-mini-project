
import pandas as pd

def add_application(db_helper, data):#data is either a list ot a list of lists
    if isinstance(data[0], list):#Checks if the first element of data is a list. This is a basic check to distinguish between a single list  or list of lists
        # If data is a list of lists (for bulk insert)
        query = "INSERT INTO applications (candidate_id, job_id, status) VALUES %s RETURNING application_id;"
    else:
        # If data is a single list (for single insert)
        query = "INSERT INTO applications (candidate_id, job_id, status) VALUES (%s, %s, %s) RETURNING application_id;"

    id = db_helper.add(query, data)
    return id


def get_applications(db_helper):
    query = """
        SELECT a.application_id, a.candidate_id, a.job_id, a.status
        FROM applications a
    """
    rows = db_helper.execute_query(query, fetch_all=True)

    if rows:
        columns = ['application_id','candidate_id', 'job_id', 'status']
        return pd.DataFrame(rows, columns=columns)
    else:
        return pd.DataFrame(columns=['application_id','candidate_id', 'job_id', 'status'])
