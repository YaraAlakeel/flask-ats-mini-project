import pandas as pd

def add_candidate (db_helper , data):  #data is either a list ot a list of lists
    if isinstance(data[0], list):  #Checks if the first element of data is a list. This is a basic check to distinguish between a single list  or list of lists
        # If data is a list of lists (for bulk insert)
        query = "INSERT INTO candidates ( first_name, last_name, email, major, skills,phone_number) VALUES %s RETURNING candidate_id;"
    else:
        # If data is a single list (for single insert)
        query = "INSERT INTO candidates ( first_name, last_name, email, major, skills,phone_number) VALUES (%s, %s, %s ,%s, %s, %s ) RETURNING candidate_id;"

    id = db_helper.add(query, data)
    return id

def get_candidates (db_helper)  :
    query = """
        SELECT candidate_id, first_name, last_name, email, major, skills,phone_number
        FROM candidates
    """
    rows = db_helper.execute_query(query, fetch_all=True)

    if rows:
        columns = ['candidate_id', 'first_name', 'last_name', 'email', 'major', 'skills','phone_number']
        return pd.DataFrame(rows, columns=columns)
    else:
        return pd.DataFrame(columns=['candidate_id', 'first_name', 'last_name', 'email', 'major', 'skills', 'phone_number'])
