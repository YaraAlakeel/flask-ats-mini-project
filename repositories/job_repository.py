import pandas as pd

def __init__(self, db):
    self.db = db

def add_job(db_helper, data):#data is either a list ot a list of lists
    if isinstance(data[0], list):#Checks if the first element of data is a list. This is a basic check to distinguish between a single list  or list of lists
        # If data is a list of lists (for bulk insert)
        query = "INSERT INTO jobs ( job_name, location , required_skills) VALUES %s RETURNING job_id;"
    else:
        # If data is a single list (for single insert)
        query = "INSERT INTO jobs ( job_name, location , required_skills) VALUES (%s, %s, %s) RETURNING job_id;"

    id = db_helper.add(query, data)
    return id

def get_jobs(db_helper):
    query = """
        SELECT a.job_id, a.job_name, a.location, a.required_skills
        FROM jobs a
    """
    rows = db_helper.execute_query(query, fetch_all=True)

    if rows:
        columns = ['job_id','job_name', 'location', 'required_skills']
        return pd.DataFrame(rows, columns=columns)
    else:
        return pd.DataFrame(columns=['job_id','job_name', 'location', 'required_skills'])

