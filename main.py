from flask import Flask, request, jsonify
from utils.database_helper import Database
import repositories.application_repository as application_repository
import repositories.job_repository as job_repository
import repositories.candidate_repository as candidate_repository
import module.combination_models as combination_models
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY')  #special object that stores configuration variables for your application. These variables can control various aspects of how your Flask application behaves.


#############################################job operations#########################################

@app.route('/add_job', methods=['POST'])
def add_job():
    try:
        job_name = request.json.get('job_name')
        location = request.json.get('location', '')
        required_skills = request.json.get('required_skills')

        if not job_name or not required_skills:
            return jsonify({'error': 'missing job_name of skills'}), 400

        db_helper = Database()
        data_list = [job_name, location, required_skills]
        job_id = job_repository.add_job(db_helper, data_list)
        # Return success response with job_id
        return jsonify({'job_id': job_id}), 201

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        return jsonify({'error': str(e)}), 500


@app.route('/display_jobs', methods=['GET'])
def display_jobs():
    try:
        db_helper = Database()
        job_df = job_repository.get_jobs(db_helper)
        # Convert DataFrame to list of dictionaries
        jobs_list = job_df.to_dict('records')

        return jsonify(jobs_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


################################################candidate operations#####################################################

@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    try:
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        major = request.json.get('major')
        skills = request.json.get('skills')
        phone_number = request.json.get('phone_number', '')

        if not first_name or not email or not major:
            return jsonify({'error': 'Missing first_name, email, or major'}), 400

        db_helper = Database()
        data_list = [first_name, last_name, email, major, skills, phone_number]
        candidate_id = candidate_repository.add_candidate(db_helper, data_list)

        # Return success response with candidate_id
        return jsonify({'candidate_id': candidate_id}), 201

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        return jsonify({'error': str(e)}), 500


@app.route('/display_candidates', methods=['GET'])
def display_candidates():
    try:
        db_helper = Database()
        candidate_df = candidate_repository.get_candidates(db_helper)

        # Convert DataFrame to list of dictionaries
        candidates_list = candidate_df.to_dict('records')

        return jsonify(candidates_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


################################################application operations###############################################

@app.route('/add_application', methods=['POST'])  ##confirmed
def add_application():
    try:
        # Retrieve data from JSON payload
        candidate_id = request.json.get('candidate_id')
        job_id = request.json.get('job_id')
        status = request.json.get('status')

        if not candidate_id or not job_id or not status:  #ensure all valuce are present
            return jsonify({'error': 'Missing candidate_id, job_id, or status parameter'}), 400

        db_helper = Database()  #instance from Database class

        # Add application and get the new application ID
        data_list = [candidate_id, job_id, status]
        application_id = application_repository.add_application(db_helper, data_list)

        # Return success response with application ID
        return jsonify({'application_id': application_id}), 201

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        return jsonify({'error': str(e)}), 500


@app.route('/display_applications', methods=['GET'])
def display_applications():
    try:
        db_helper = Database()
        applications_df = application_repository.get_applications(db_helper)

        # Convert DataFrame to list of dictionaries
        applications_list = applications_df.to_dict('records')

        return jsonify(applications_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


############################################combination#####################################################

@app.route('/candidates_for_job/<int:job_id>', methods=['GET'])
def candidates_for_job(job_id):
    try:
        db_helper = Database()
        candidates_df = combination_models.get_candidates_for_job(db_helper, job_id)
        candidates_list = candidates_df.to_dict('records')
        return jsonify(candidates_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/jobs_for_candidate/<int:candidate_id>', methods=['GET'])
def jobs_for_candidate(candidate_id):
    try:
        db_helper = Database()
        jobs_df = combination_models.get_jobs_for_candidate(db_helper, candidate_id)
        jobs_list = jobs_df.to_dict('records')
        return jsonify(jobs_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
