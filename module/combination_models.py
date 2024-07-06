import pandas as pd

def get_candidates_for_job(db_helper, job_id):
    query = """
        SELECT c.*
        FROM candidates c
        JOIN applications a ON c.candidate_id = a.candidate_id
        WHERE a.job_id = %s;
    """
    rows = db_helper.execute_query(query, (job_id,), fetch_all=True)
    columns = ['candidate_id', 'first_name', 'last_name', 'email', 'major', 'skills', 'phone_number']
    return pd.DataFrame(rows, columns=columns)


def get_jobs_for_candidate(db_helper, candidate_id):
    query = """
        SELECT j.*
        FROM jobs j
        JOIN applications a ON j.job_id = a.job_id
        WHERE a.candidate_id = %s;
    """
    rows = db_helper.execute_query(query, (candidate_id,), fetch_all=True)
    columns = ['job_id', 'job_name', 'location', 'required_skills']
    return pd.DataFrame(rows, columns=columns)
