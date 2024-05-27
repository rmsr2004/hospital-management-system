from dotenv import dotenv_values
from cryptography.fernet import Fernet
from datetime import datetime
import flask
import logging
import psycopg2
import jwt
import secrets
import json

app = flask.Flask(__name__)

secret_key = secrets.token_hex(64)  # Generate a random secret key to encode/decode JWT tokens

StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500
} # Status codes for the API

user_types = {
    'patient': 1,
    'doctor': 2,
    'nurse': 3, 
    'assistant': 4
} # User types


##########################################################
## DATABASE ACCESS
##########################################################

def db_connection():
    #
    # Decrypting the environment variables on .env file
    #
    
    env_vars = dotenv_values(".env")

    key = env_vars["KEY"].encode()
    cipher_suite = Fernet(key)

    decrypted_user = cipher_suite.decrypt(eval(env_vars["USER"])).decode()
    decrypted_password = cipher_suite.decrypt(eval(env_vars["PASSWORD"])).decode()
    decrypted_host = cipher_suite.decrypt(eval(env_vars["HOST"])).decode()
    decrypted_port = cipher_suite.decrypt(eval(env_vars["PORT"])).decode()
    decrypted_database = cipher_suite.decrypt(eval(env_vars["DATABASE"])).decode()

    db = psycopg2.connect(
        user=decrypted_user,
        password=decrypted_password,
        host=decrypted_host,
        port=decrypted_port,
        database=decrypted_database
    )
    return db

##########################################################
## ENDPOINTS
##########################################################
@app.route('/dbproj/')
def landing_page():
    return """
        Welcome to our Hospital Management System! <br/>
        <br/>
        Check the sources for instructions on how to use the endpoints!<br/>
        <br/>
        BD 2023-2024 Team<br/>
        <br/>
    """


##
## Register Doctors
##
## Example of payload:
##  POST http://localhost:8080/dbproj/register/doctor
##  {
##	    "name": "Rodrigo",
##	    "cc": "741258963",
##	    "address": "Vouzela",
##	    "phone": "963245449",
##	    "username": "rmsr2004",
##	    "password": "1234",
##	    "email": "rodrigomiguelsr2004@gmail.com",
##	    "contract": {
##		    "salary": 1200.00,
##		    "start_date": "2024-12-21",
##		    "final_date": "2025-12-21",
##		    "ctype_id": "3"
##	    },
##	    "medical_license": {
##		    "issue_date": "2024-12-21",
##		    "expiration_date": "2025-12-21"
##	    }
##  }
##
##
@app.route('/dbproj/register/doctor', methods=['POST'])
def add_doctor():
    logger.info('POST /dbproj/register/doctor')

    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/register/doctor - payload: {payload}')

    #
    # Validate payload.
    #

    required_fields = ['name', 'cc', 'address', 'phone', 'username', 'password', 'email', 'contract', 'medical_license', 'specialisations']
    required_contract_fields = ['salary', 'start_date', 'final_date', 'ctype_id']
    required_medical_license_fields = ['issue_date', 'expiration_date']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)
        
    # Verify contract fields
    for field in required_contract_fields:
        if field not in payload['contract']:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in contract payload'}
            return flask.jsonify(response)
        
    # Verify medical license fields
    for field in required_medical_license_fields:
        if field not in payload['medical_license']:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in medical_license payload'}
            return flask.jsonify(response)
    
    specialisations = payload['specialisations']
        
    # Validate Date formats
    dates = [payload['contract']['start_date'], payload['contract']['final_date'], payload['medical_license']['issue_date'], payload['medical_license']['expiration_date']]

    for date in dates:
        if not validate_date_format(date):
            response = {'status': StatusCodes['api_error'], 'errors': f'Invalid date format: {date}'}
            return flask.jsonify(response)

    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()

    conn.autocommit = False
        
    # Query to insert the doctor
    statement = """
        INSERT INTO employees (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, salary, start_date, final_date, ctype_id, person_type) 
                VALUES (%s, %s, %s, %s, %s, encrypt(%s, 'my_secret_key'), %s, %s, %s, %s, %s, %s); 

        INSERT INTO doctors (person_id, ml_issue_date, ml_expiration_date) 
                SELECT person_id, %s, %s FROM employees WHERE person_cc = %s
        RETURNING person_id;
    """
    values = (
        payload['cc'], payload['name'], payload['address'], payload['phone'], payload['username'], payload['password'], 
        payload['email'], payload['contract']['salary'], payload['contract']['start_date'], payload['contract']['final_date'], 
        payload['contract']['ctype_id'], "2", payload['medical_license']['issue_date'], payload['medical_license']['expiration_date'],
        payload['cc']
    )

    try:
        cur.execute(statement, values)

        doctor_id = cur.fetchone()[0]
        if doctor_id is None:
            raise Exception('Error inserting doctor!')
        
        # Queries to insert the doctor specialisations and sub-specialisations
        for spec in specialisations:
            spec_id, sub_spec_id = spec

            # Query to verify if the specialisation exists
            statement = """
                SELECT spec_id FROM specialisations WHERE spec_id = %s;
            """
            values = (spec_id, )
            cur.execute(statement, values)

            result = cur.fetchone()
            if result is None:
                raise Exception(f'Specialisation {spec_id} does not exist!')
            
            # Query to verify if the sub-specialisation exists
            if sub_spec_id is not None:
                statement = """
                    SELECT sub_spec_id FROM sub_specialisations WHERE sub_spec_id = %s;
                """
                values = (sub_spec_id, )
                cur.execute(statement, values)

                result = cur.fetchone()
                if result is None:
                    raise Exception(f'Sub-specialisation {sub_spec_id} does not exist!')
                
                # Query to insert the doctor sub-specialisation
                statement = """
                    INSERT INTO sub_specialisations_doctors (doctor_id, sub_spec_id) VALUES (%s, %s);
                """
                values = (doctor_id, sub_spec_id)
                cur.execute(statement, values)
                
            # Query to insert the doctor specialisation
            statement = """
                INSERT INTO specialisations_doctors (doctor_id, spec_id) VALUES (%s, %s);
            """
            values = (doctor_id, spec_id)
            cur.execute(statement, values)

        
        response = {'status': StatusCodes['success'], 'results': doctor_id}

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST dbproj/register/doctor - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## Register Nurses
##
## Example of payload:
##  POST http://localhost:8080/dbproj/register/nurse
##  {
##	    "name": "Rodrigo",
##	    "cc": "741358963",
##	    "address": "Vouzela",
##	    "phone": "983245449",
##	    "username": "rr21",
##	    "password": "12340",
##	    "email": "rodrigo2004@gmail.com",
##	    "contract": {
##		    "salary": 1200.00,
##		    "start_date": "2024-12-21",
##		    "final_date": "2025-12-21",
##		    "ctype_id": "3"
##	    },
##	    "categories": [1,2,3]
##  }
##
##
@app.route('/dbproj/register/nurse', methods=['POST'])
def add_nurse():
    logger.info('POST /dbproj/register/nurse')

    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/register/nurse - payload: {payload}')

    #
    # Validate payload.
    #

    required_fields = ['name', 'cc', 'address', 'phone', 'username', 'password', 'email', 'contract', 'categories']
    required_contract_fields = ['salary', 'start_date', 'final_date', 'ctype_id']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)
        
    # Verify contract fields
    for field in required_contract_fields:
        if field not in payload['contract']:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in contract payload'}
            return flask.jsonify(response)
        
    if payload['categories'] == []:
        response = {'status': StatusCodes['api_error'], 'errors': 'categories values is empty'}
        return flask.jsonify(response)
    
    categories = payload['categories']

    # Validate Date formats
    dates = [payload['contract']['start_date'], payload['contract']['final_date']]
    for date in dates:
        if not validate_date_format(date):
            response = {'status': StatusCodes['api_error'], 'errors': f'Invalid date format: {date}'}
            return flask.jsonify(response)

    #
    # SQL query
    #
    
    conn = db_connection()
    cur = conn.cursor()
    

    # Query to insert the nurse
    insert_statement = """
        INSERT INTO employees (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, salary, start_date, final_date, ctype_id, person_type) 
        VALUES (%s, %s, %s, %s, %s, encrypt(%s, 'my_secret_key'), %s, %s, %s, %s, %s ,%s);

        INSERT INTO nurses (person_id) 
        SELECT person_id FROM employees WHERE person_cc = %s RETURNING person_id;
    """
    values = (
        payload['cc'], payload['name'], payload['address'], payload['phone'], payload['username'], payload['password'], payload['email'], 
        payload['contract']['salary'], payload['contract']['start_date'], payload['contract']['final_date'], payload['contract']['ctype_id'],
        "3", payload['cc']
    )

    try:
        cur.execute(insert_statement, values)

        nurse_id = cur.fetchone()[0]

        if nurse_id is None:
            raise Exception('Error inserting nurse!')
        
        # Queries to insert the nurse categories
        for category_id in categories:
            # Query to verify if the category exists
            statement = """
                SELECT category_id FROM nurse_categories WHERE category_id = %s;
            """ 
            values = (category_id, )
            cur.execute(statement, values)

            result = cur.fetchone()
            if result is None:
                raise Exception(f'Category {category_id} does not exist!')
            
            # Query to insert the nurse category
            statement = """
                INSERT INTO nurses_categories (nurse_id, category_id) VALUES (%s, %s);
            """
            values = (nurse_id, category_id)
            cur.execute(statement, values)
    
        response = {'status': StatusCodes['success'], 'results': nurse_id}

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST /dbproj/register/nurse - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## Register Assistants
##
## Example of payload:
##  POST http://localhost:8080/dbproj/register/assistant
##  {
##	    "name": "Rodrigo",
##	    "cc": "741358923",
##	    "address": "Vouzela",
##	    "phone": "983225449",
##	    "username": "rr2321",
##	    "password": "12345",
##	    "email": "rr213@gmail.com",
##	    "contract": {
##		    "salary": 1200.00,
##		    "start_date": "2024-12-21",
##		    "final_date": "2025-12-21",
##		    "ctype_id": "3"
##	    }
##  }
##
##
@app.route('/dbproj/register/assistant', methods=['POST'])
def add_assistant():
    logger.info('POST /dbproj/register/assistant')

    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/register/assistant - payload: {payload}')

    #
    # Validate payload.
    #

    required_fields = ['name', 'cc', 'address', 'phone', 'username', 'password', 'email', 'contract']
    required_contract_fields = ['salary', 'start_date', 'final_date', 'ctype_id']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)
        
    # Verify contract fields
    for field in required_contract_fields:
        if field not in payload['contract']:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in contract payload'}
            return flask.jsonify(response)
    
    # Validate Date formats
    dates = [payload['contract']['start_date'], payload['contract']['final_date']]
    for date in dates:
        if not validate_date_format(date):
            response = {'status': StatusCodes['api_error'], 'errors': f'Invalid date format: {date}'}
            return flask.jsonify(response)

    #
    # SQL Query
    #

    conn = db_connection()
    cur = conn.cursor()


    # query to insert the assistant
    statement = """
        INSERT INTO employees (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, salary, start_date, final_date, ctype_id, person_type) 
            VALUES (%s, %s, %s, %s, %s, encrypt(%s, 'my_secret_key'), %s, %s, %s, %s, %s, %s);
        INSERT INTO assistants (person_id) 
            SELECT person_id FROM employees WHERE person_cc = %s RETURNING person_id;
    """
    values = (
        payload['cc'], payload['name'], payload['address'], payload['phone'], payload['username'], payload['password'], payload['email'], 
        payload['contract']['salary'], payload['contract']['start_date'], payload['contract']['final_date'], payload['contract']['ctype_id'],
        "4", payload['cc']
    )

    try:
        cur.execute(statement, values)
        
        assistant_id = cur.fetchone()[0]
        if assistant_id is None:
            raise Exception('Error inserting assistant!')
        
        response = {'status': StatusCodes['success'], 'results': assistant_id}

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST /dbproj/register/assistant - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## Register Patients
## 
## Example of payload:
##  POST http://localhost:8080/dbproj/register/patient
##  {
##	    "name": "Rodrigo",
##	    "cc": "741358923",
##	    "address": "Vouzela",
##	    "phone": "983225449",
##	    "username": "drmdas23",
##	    "password": "12345",
##	    "email": "rodrigosantosrmasd@gmail.com"
##  }
##
##
@app.route('/dbproj/register/patient', methods=['POST'])
def add_patient():
    logger.info('POST /dbproj/register/patient')

    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/register/patient - payload: {payload}')

    #
    # Validate payload.
    #

    required_fields = ['name', 'cc', 'address', 'phone', 'username', 'password', 'email']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)


    #
    # SQL Query
    #

    conn = db_connection()
    cur = conn.cursor()

    # query to insert the patient
    statement = """
        INSERT INTO patients (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type) 
            VALUES (%s, %s, %s, %s, %s, encrypt(%s, 'my_secret_key'), %s, %s) RETURNING person_id;
    """
    values = (
        payload['cc'], payload['name'], payload['address'], payload['phone'], payload['username'], payload['password'], 
        payload['email'], "1"
    )

    try:
        cur.execute(statement, values)
        
        patient_id = cur.fetchone()[0]
        if patient_id is None:
            raise Exception('Error inserting patient!')
        
        response = {'status': StatusCodes['success'], 'results': patient_id}

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST /dbproj/register/patient - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## User Login
## 
## Example of payload:
##  PUT http://localhost:8080/dbproj/user
##  {
##	    "username": "pedro",
##	    "password": "senha24"
##  }
##
##
@app.route('/dbproj/user', methods = ['PUT'])
def login():
    logger.info('PUT /dbproj/user')

    payload = flask.request.get_json()

    logger.debug(f'PUT /dbproj/user - payload: {payload}')

    #
    # Validate payload.
    #

    if 'username' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'username is required!'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'password is required!'}
        return flask.jsonify(response)
    
    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()
    

    statement =  """
        SELECT person_type, person_id, decrypt(person_password, 'my_secret_key') AS decrypted_password
        FROM employees
        WHERE person_username = %s
        UNION
        SELECT person_type, person_id, decrypt(person_password, 'my_secret_key') AS decrypted_password
        FROM patients
        WHERE person_username = %s;
    """
    values = (payload['username'], payload['username'])

    try:
        cur.execute(statement, values)
        result = cur.fetchone()

        if result:
            user_type, user_id, decrypted_password = result

            if decrypted_password != payload['password']:
                raise Exception('Invalid password!')
            
            jwt_payload = { 'user_id': int(user_id), 'user_type': int(user_type)}
            jwt_token = jwt.encode(jwt_payload, secret_key, algorithm='HS256')

            logger.debug(f'PUT /dbproj/user - user {user_id} logged in')
            
            response = {'status': StatusCodes['success'], 'results': jwt_token}

            conn.commit()
        else:
            raise Exception('Invalid username or password!')
        
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'PUT dproj/user - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error), 'results': None}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## Schedule Appointment
##
## Example of payload:
##  POST http://localhost:8080/dbproj/appointment
##  {
##	    "doctor_id": "10",
##	    "date": "2024-10-20",
##	    "type": "GERAL",
##	    "room": "3",
##	    "hour": "15",
##	    "minutes": "30",
##	    "nurses": [
##		    [12, "TRIAGEM"]
##	    ]
##  }
##
##
@app.route('/dbproj/appointment', methods = ['POST'])
def schedule_appointment():
    logger.info('POST /dbproj/appointment')
    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/appointment - payload: {payload}')

    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)
    
    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)

    # Verify if the user is a patient
    if jwt_token['user_type'] != user_types['patient']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only patients can schedule appointments!'}
        return flask.jsonify(response)
    
    #
    # Validate payload.
    #

    required_fields = ['doctor_id', 'date', 'hour', 'minutes', 'type', 'room', 'nurses']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)
    
    if payload['nurses'] == []:
        response = {'status': StatusCodes['api_error'], 'errors': 'nurses values is empty'}
        return flask.jsonify(response)
    
    # Validate Date format
    if not validate_date_format(payload['date']):
        response = {'status': StatusCodes['api_error'], 'errors': f'Invalid date format: {payload["date"]}'}
        return flask.jsonify(response)
    
    #
    # SQL query 
    #

    conn = db_connection()
    cur = conn.cursor()
    
    # Query to verify if the doctor exists and if the doctor type given corresponds to real doctor type
    statement =  """
        SELECT e.person_id, e.person_name, s.specialization
        FROM employees AS e
        LEFT JOIN specialisations_doctors AS sd ON e.person_id = sd.doctor_id
        LEFT JOIN specialisations AS s ON s.spec_id = sd.spec_id
        WHERE e.person_type = 2 AND e.person_id = %s AND ( (%s = 'GERAL' AND sd.spec_id IS NULL)
                                                           OR s.specialization = %s);
    """
    values = (payload['doctor_id'], payload['type'], payload['type'])

    try:
        cur.execute(statement, values)
        
        result = cur.fetchone()
        if result is None:
            raise Exception('Doctor does not exist or the type of appointment does not correspond to the doctor specialisation!')

        # Query to verify if the doctor is available
        statement =  """
            SELECT is_doctor_available_for_appointment(%s, %s, %s, %s);
        """
        values = (payload['doctor_id'], payload['date'], payload['hour'], payload['minutes'])
        cur.execute(statement, values)

        result = cur.fetchone()[0]
        if not result:
            raise Exception('Doctor is already booked at this time!')
        

        # Query to verify if the room is available
        statement =  """
            SELECT is_room_available_for_appointment(%s, %s, %s, %s);
        """
        values = (payload['room'], payload['date'], payload['hour'], payload['minutes'])
        cur.execute(statement, values)

        result = cur.fetchone()[0]
        if not result:
            raise Exception('Room is already booked at this time!')
    

        # Query to insert the appointment
        statement =  """
            INSERT INTO appointments (doctor_id, patient_id, app_date, app_hour, app_minutes, app_type, app_room, app_status, app_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING appointment_id;
        """
        values = (
            payload['doctor_id'], jwt_token['user_id'], payload['date'], payload['hour'], payload['minutes'], 
            payload['type'], payload['room'], 0, 30
        )
        cur.execute(statement, values)

        appointment_id = cur.fetchone()[0]

        logger.debug(f'POST /dbproj/appointment - appointment {appointment_id} created')

        # Inserir enfermeiros associados à consulta
        for nurse in payload['nurses']:
            nurse_id, role_name = nurse

            # Verify if nurse is a "CONSULTAS" nurse
            statement =  """
                SELECT nc.category
                FROM nurse_categories AS nc
                JOIN nurses_categories AS nsc ON nsc.category_id = nc.category_id
                JOIN employees AS e ON e.person_id = nsc.nurse_id
                WHERE e.person_id = %s AND nc.category = 'CONSULTAS';
            """
            values = (nurse_id, )

            cur.execute(statement, values)
            result = cur.fetchone()

            if result is None:
                raise Exception('Nurse is not a valid nurse!')
            
            # Verificar se o role existe na tabela de roles
            statement = """
                SELECT role_id 
                FROM roles 
                WHERE role = %s
                AND role_type = 0;
            """
            values = (role_name, )
            cur.execute(statement, values)

            role_id = cur.fetchone()
            
            if role_id is None:
                raise Exception(f'Role {role_name} does not exist or is not valid for appointment!')
            

            role_id = role_id[0]

            # Verify if the nurse is available
            statement = """
                SELECT is_nurse_available_for_appointment(%s, %s, %s, %s);
            """
            values = (nurse_id, payload['date'], payload['hour'], payload['minutes'])
            cur.execute(statement, values)

            available = cur.fetchone()[0]
            if not available:
                raise Exception(f'Nurse {nurse_id} is not available at this time!')
            
            # Inserir na tabela nurses_roles se não existir
            statement = """
                INSERT INTO nurses_roles (nurse_id, role_id)
                VALUES (%s, %s)
                ON CONFLICT (nurse_id) DO NOTHING
            """
            values = (nurse_id, role_id)
            cur.execute(statement, values)


            # Inserir na tabela roles_appointments
            statement = """
                INSERT INTO roles_appointments (role_id, app_id, doctor_id, patient_id)
                VALUES (%s, %s, %s, %s)
            """
            values = (role_id, appointment_id, payload['doctor_id'], jwt_token['user_id'])
            cur.execute(statement, values)
        
        response = {'status': StatusCodes['success'], 'results': appointment_id}

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST dproj/appointment - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': error, 'results': None}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## See Appointments
##
## GET http://localhost:8080/dbproj/appointments/<patient_id>
##
##
@app.route('/dbproj/appointments/<patient_id>', methods = ['GET'])
def see_appointments(patient_id=None):
    if patient_id is None:
        response = {'status': StatusCodes['api_error'], 'errors': 'patient_id is required!'}
        return flask.jsonify(response)
        
    logger.info(f'GET /dbproj/appointments/{patient_id}')

    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)
    
    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)
    
    # Verify if the user is an assistant or the target patient
    if not (jwt_token['user_type'] == user_types['assistant'] or jwt_token['user_type'] == user_types['patient']):
        response = {'status': StatusCodes['api_error'], 'errors': 'Only patients or assistants can see appointments!'}
        return flask.jsonify(response)
    
    if jwt_token['user_id'] != int(patient_id) and jwt_token['user_type'] != user_types['assistant']:
        response = {'status': StatusCodes['api_error'], 'errors': 'You can only see your own appointments!'}
        return flask.jsonify(response)

    #
    # SQL query
    #
        
    conn = db_connection()
    cur = conn.cursor()

    statement = """
        SELECT appointment_id, doctor_id, employees.person_name, app_date, app_hour, app_minutes, app_type, app_room, 
                CASE 
                    WHEN appointments.app_status = 0 THEN 'marcada' 
                    WHEN appointments.app_status = 1 THEN 'realizada' 
                    ELSE 'unknown' 
                END AS app_status 
        FROM appointments
        JOIN employees ON appointments.doctor_id = employees.person_id
        WHERE patient_id = %s;
    """
    values = (patient_id, )

    try:
        cur.execute(statement, values)
        rows = cur.fetchall()

        logger.debug(f'GET /appointments/{patient_id} - parse')
        
        results = []
        for row in rows:
            logger.debug(row)

            content = {
                'appointment_id': row[0], 
                'doctor_id': row[1], 
                'doctor_name': row[2], 
                'date': row[3], 
                'hour': row[4],
                'minutes': row[5],
                'type': row[6],
                'room': row[7],
                'status': row[8]
            }
            results.append(content)
        
        if results == []:
            raise Exception('No appointments found!')
        
        response = {'status': StatusCodes['success'], 'results': results}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /departments - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## Schedule Surgery
##
## Example of payload:
##  POST http://localhost:8080/dbproj/surgery
##  POST http://localhost:8080/dbproj/surgery/10
##
##  {
##	    "patient_id": "10",
##	    "doctor_id": "9",
##	    "nurses": [
##				[19, "RESPONSAVEL"],
##				[13, "MONITOR"],
##				[11, "ANESTESISTA"]
##			],
##	    "date": "2024-12-25",
##	    "type": "ORTOPEDIA",
##	    "room": "35",
##	    "hour": "13",
##	    "minutes": "00"
##      "final_date": ... -> if hospitalization_id is provided
##  }
##
##
@app.route('/dbproj/surgery', methods = ['POST'])
@app.route('/dbproj/surgery/<hospitalization_id>', methods = ['POST'])
def shedule_surgery(hospitalization_id=None):
    if hospitalization_id is not None:
        logger.info(f'POST /dbproj/surgery/{hospitalization_id}')
    else:
        logger.info('POST /dbproj/surgery')
    
    payload = flask.request.get_json()
    
    if hospitalization_id is not None:
        logger.debug(f'POST /dbproj/surgery/{hospitalization_id} - payload: {payload}')
    else:
        logger.debug(f'POST /dbproj/surgery - payload: {payload}')
    
    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)

    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)

    # Verify if the user is a assistant
    if jwt_token['user_type'] != user_types['assistant']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only assistants can schedule appointments!'}
        return flask.jsonify(response)
    
    #
    # Validate payload
    #

    required_fields = ['patient_id', 'doctor_id', 'nurses', 'date', 'type', 'room', 'hour', 'minutes']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)

    
    # Verify if there is a responsible nurse and assign the nurse to a variable and remove it from the list
    nurses = payload['nurses'] # [[id, 'RESPONSAVEL']]
    if nurses == []:
        response = {'status': StatusCodes['api_error'], 'errors': 'nurses values is empty'}
        return flask.jsonify(response)
    
    nurse_responsible_id = None
    for nurse in nurses:
        if nurse[1] == "RESPONSAVEL":
            nurse_responsible_id = nurse[0]
            nurses.remove(nurse)
            break

    if nurse_responsible_id is None and hospitalization_id is None:
        response = {'status': StatusCodes['api_error'], 'errors': 'nurses must have a responsible nurse!'}
        return flask.jsonify(response)
    
    if hospitalization_id is None:
        if 'final_date' not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': 'final_date is required!'}
            return flask.jsonify(response)
        if not validate_date_format(payload['final_date']):
            response = {'status': StatusCodes['api_error'], 'errors': f'Invalid date format: {payload["final_date"]}'}
            return flask.jsonify(response)
        
    if not validate_date_format(payload['date']):
        response = {'status': StatusCodes['api_error'], 'errors': f'Invalid date format: {payload["date"]}'}
        return flask.jsonify(response)
    
    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()


    # Query to verify if the doctor exists and if the doctor type given corresponds to real doctor type
    statement =  """
        SELECT d.ml_id, e.person_name, s.specialization, ss.sub_spec
        FROM doctors AS d
        JOIN employees AS e ON d.person_id = e.person_id
        JOIN specialisations_doctors AS sd ON d.ml_id = sd.doctor_id
        JOIN specialisations AS s ON sd.spec_id = s.spec_id
        LEFT JOIN sub_specialisations_doctors AS ssd ON d.ml_id = ssd.doctor_id
        LEFT JOIN sub_specialisations AS ss ON ssd.sub_spec_id = ss.sub_spec_id
        WHERE e.person_id = %s AND s.specialization = 'CIRURGIA' AND ss.sub_spec = %s;
    """
    values = (payload['doctor_id'], payload['type'])
    
    try:
        cur.execute(statement, values)

        result = cur.fetchone()
        if result is None:
            raise Exception('Doctor does not exist or the type of surgery does not correspond to the doctor specialisation!')
        

        # Verify if the doctor is available
        statement = """
            SELECT is_doctor_available_for_surgery(%s, %s, %s, %s);
        """
        values = (payload['doctor_id'], payload['date'], payload['hour'], payload['minutes'])
        
        cur.execute(statement, values)
        
        doctor_available = cur.fetchone()[0]
        if not doctor_available:
            raise Exception('Doctor is not available at this time!')
        
        logger.debug(f'POST /dbproj/surgery - doctor is available')
        
        # Doctor is available, verify if the room is available
        statement = """
            SELECT is_room_available_for_surgery(%s, %s, %s, %s);
        """
        values = (payload['room'], payload['date'], payload['hour'], payload['minutes'])

        cur.execute(statement, values)
        
        room_available = cur.fetchone()[0]
        if not room_available:
            raise Exception('Room is not available at this time!')
        
        logger.debug(f'POST /dbproj/surgery - room is available')
        

        # Hospitalization_id is not provided, create a hospitalization
        if hospitalization_id is None:
            logger.debug(f'POST /dbproj/surgery - creating hospitalization..')
            # Verify if nurse is a "HOSPITALIZACOES" nurse
            statement =  """
                SELECT nc.category
                FROM nurse_categories AS nc
                JOIN nurses_categories AS nsc ON nsc.category_id = nc.category_id
                JOIN employees AS e ON e.person_id = nsc.nurse_id
                WHERE e.person_id = %s AND nc.category = 'HOSPITALIZACOES';
            """
            values = (nurse_responsible_id, )
            cur.execute(statement, values)

            result = cur.fetchone()
            if result is None:
                raise Exception(f'Responsible nurse {nurse_responsible_id} is not a valid nurse!')
            
            logger.debug(f'POST /dbproj/surgery - responsible nurse is valid')
            
            # Query to generate the hospitalization room
            statement = """
                SELECT get_first_available_room(%s);
            """
            values = (payload['date'], )
            cur.execute(statement, values)

            room = cur.fetchone()[0]
            if room is None:
                raise Exception('No rooms available for hospitalization!')
            
            logger.debug(f'POST /dbproj/surgery - room {room} available')
            
            # Query to insert the hospitalization
            statement = """
                INSERT INTO hospitalizations (start_date, final_date, room, assistant_id, nurse_id) 
                    VALUES (%s, %s, %s, %s, %s) RETURNING hosp_id;
            """
            values = (payload['date'], payload['final_date'], room, jwt_token['user_id'], nurse_responsible_id)
            cur.execute(statement, values)

            hospitalization_id = cur.fetchone()[0]
            if hospitalization_id is None:
                raise Exception('Error creating hospitalization!')

            logger.debug(f'POST /dbproj/surgery - hospitalization created')

        # Associate the surgery with the hospitalization
        statement = """
            INSERT INTO surgeries (doctor_id, patient_id, surgery_date, surgery_hour, surgery_minutes, surgery_type, surgery_room, 
                                   surgery_status, hosp_id, surgery_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 120) RETURNING surgery_id;
        """
        values = (
            payload['doctor_id'], payload['patient_id'], payload['date'], payload['hour'], payload['minutes'], 
            payload['type'], payload['room'], 0, hospitalization_id
        )
        cur.execute(statement, values)

        surgery_id = cur.fetchone()[0]

        logger.debug(f'POST /dbproj/surgery - surgery {surgery_id} created')
        
        # Inserir enfermeiros associados à cirurgia
        # Verify if the nurses are available
        for nurse in nurses:
            nurse_id, role_name = nurse

            # Verify if nurse is a "CIRURGIAS" nurse
            statement = """
                SELECT nc.category
                FROM nurse_categories AS nc
                JOIN nurses_categories AS nsc ON nsc.category_id = nc.category_id
                JOIN employees AS e ON e.person_id = nsc.nurse_id
                WHERE e.person_id = %s AND nc.category = 'CIRURGIAS';
            """
            values = (nurse_id, )

            cur.execute(statement, values)

            result = cur.fetchone()
            if result is None:
                raise Exception(f'Nurse {nurse_id} is not a valid nurse!')
            

            # Verificar se o role existe na tabela de roles
            statement = """
                SELECT role_id 
                FROM roles 
                WHERE role = %s
                AND role_type = 1;
            """
            values = (role_name, )
            cur.execute(statement, values)

            role_id = cur.fetchone()
            
            if role_id is None:
                raise Exception(f'Role {role_name} does not exist!')

            role_id = role_id[0]

            logger.debug(f'POST /dbproj/surgery - role_id: {role_id}')

            # Verify if the nurse is available
            statement = """
                SELECT is_nurse_available_for_appointment(%s, %s, %s, %s);
            """
            values = (nurse_id, payload['date'], payload['hour'], payload['minutes'])
            cur.execute(statement, values)

            available = cur.fetchone()[0]
            if not available:
                raise Exception(f'Nurse {nurse_id} is not available at this time!')

            # Inserir na tabela nurses_roles se não existir
            statement = """
                INSERT INTO nurses_roles (nurse_id, role_id)
                VALUES (%s, %s)
                ON CONFLICT (nurse_id) DO NOTHING
            """
            values = (nurse_id, role_id)
            cur.execute(statement, values)

            logger.debug(f'POST /dbproj/surgery - nurse inserted')

            # Inserir na tabela roles_surgeries
            statement = """
                INSERT INTO roles_surgeries (role_id, surgery_id, doctor_id)
                VALUES (%s, %s, %s)
            """
            values = (role_id, surgery_id, payload['doctor_id'])
            cur.execute(statement, values)

            logger.debug(f'POST /dbproj/surgery - role inserted')

        logger.debug(f'POST /dbproj/surgery - nurses inserted')
        conn.commit()

        response = {'status': StatusCodes['success'], 'results': surgery_id} 
    
    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST dproj/surgery - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': str(error), 'results': None}

    finally:
        if conn is not None:
            conn.close()
    
    return  flask.jsonify(response)

##
## Get Prescriptions
##
##
@app.route('/dbproj/prescriptions/<person_id>', methods=['GET'])
def get_prescriptions(person_id):
    logger.info(f'GET /dbproj/prescriptions/{person_id}')

    logger.debug(f'person_id: {person_id}')

    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)

    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)

    # Verify if the user is the targeted patient or a employee
    if jwt_token['user_type'] == user_types['patient'] and jwt_token['user_id'] != int(person_id):
        response = {'status': StatusCodes['api_error'], 'errors': 'You can only see your own prescriptions!'}
        return flask.jsonify(response)
    
    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()

    # Query to get prescriptions
    statement = """
        SELECT * FROM (
            (SELECT p.presc_id, p.presc_validity_date, pos.dosage, pos.frequency, m.medication
            FROM prescriptions AS p
            JOIN posologies_prescriptions AS pp ON p.presc_id = pp.presc_id
            JOIN posologies AS pos ON pp.posology_id = pos.posology_id
            JOIN posologies_medicines AS pm ON pos.posology_id = pm.posology_id
            JOIN medicines AS m ON pm.medication_id = m.medication_id
            JOIN appointments_prescriptions AS ap ON ap.presc_id = p.presc_id
            WHERE ap.patient_id = %s)

            UNION

            (SELECT p.presc_id, p.presc_validity_date, pos.dosage, pos.frequency, m.medication
            FROM prescriptions AS p
            JOIN posologies_prescriptions AS pp ON p.presc_id = pp.presc_id
            JOIN posologies AS pos ON pp.posology_id = pos.posology_id
            JOIN posologies_medicines AS pm ON pos.posology_id = pm.posology_id
            JOIN medicines AS m ON pm.medication_id = m.medication_id
            JOIN hospitalizations_prescriptions AS hp ON p.presc_id = hp.presc_id
            JOIN hospitalizations AS h ON hp.hosp_id = h.hosp_id
            JOIN surgeries AS s ON s.hosp_id = h.hosp_id
            WHERE s.patient_id = %s)
        )
        ORDER BY presc_id ASC;
    """
    values = (person_id, person_id)

    try:
        cur.execute(statement, values)
        prescriptions = cur.fetchall()

        if prescriptions == []:
            raise Exception('No prescriptions found!')
        
        results = []
        for prescription in prescriptions:
            content = {
                'prescription_id': prescription[0],
                'validity_date': prescription[1],
                'posology': [{ 'dosage': prescription[2], 'frequency': prescription[3], 'medication': prescription[4]}]
            }
            results.append(content)
    
        response = {'status': StatusCodes['success'], 'results': results}
    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST /dbproj/prescriptions/{person_id} - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': str(error), 'results': None}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


##
## ADD prescriptions
##
@app.route('/dbproj/prescription/', methods=['POST'])
def add_prescription():
    logger.info(f'POST /dbproj/prescription/')
    payload = flask.request.get_json()


    logger.debug(f'POST /dbproj/prescription/ - payload: {payload}')
    
    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)

    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)

    # Verify if the user is the targeted patient or a employee
    if jwt_token['user_type'] != user_types['doctor']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only doctors can add prescriptions!'}
        return flask.jsonify(response)
    
    #
    # Validate payload
    #

    required_fields = ['type', 'event_id', 'validity_date', 'medicines']
    medicine_fields = ['medicine', 'posology_dose', 'posology_frequency']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)
    
    if payload['type'] not in ['hospitalization', 'appointment']:
        response = {'status': 'api_error', 'errors': 'Invalid type! Must be "hospitalization" or "appointment".'}
        return flask.jsonify(response)

    medicines = payload['medicines']

    for medicine in medicines:
        for field in medicine_fields:
            if field not in medicine:
                response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
                return flask.jsonify(response)
            
    # Validate Date format
    if not validate_date_format(payload['validity_date']):
        response = {'status': StatusCodes['api_error'], 'errors': f'Invalid date format: {payload["validity_date"]}'}
        return flask.jsonify(response)
    
    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()

    # Query to verify if the event exists
    if payload['type'] == 'hospitalization':
        statement = """
            SELECT hosp_id FROM hospitalizations WHERE hosp_id = %s;
        """
    else:
        statement = """
            SELECT appointment_id FROM appointments WHERE appointment_id = %s;
        """
    values = (payload['event_id'], )
    
    try:
        cur.execute(statement, values)
        
        event_id = cur.fetchone()
        if event_id is None:
            raise Exception('Event does not exist!')
        
        # Query to insert the prescription
        statement = """
            INSERT INTO prescriptions (presc_date, presc_validity_date) VALUES (CURRENT_DATE, %s) 
            RETURNING presc_id;
        """
        values = (payload['validity_date'], )
        cur.execute(statement, values)

        presc_id = cur.fetchone()[0]
        if presc_id is None:
            raise Exception('Error creating prescription!')
    

        # Validate the medicines
        for medicine in medicines:
            statement = """
                SELECT medication_id FROM medicines WHERE medication = %s;
            """
            values = (medicine['medicine'], )
            cur.execute(statement, values)

            medication_id = cur.fetchone()
            if medication_id is None:
                raise Exception(f'Medicine {medicine["medicine"]} does not exist!')
            
            # Query to verify if posology exists
            statement = """
                SELECT posology_id FROM posologies WHERE dosage = %s AND frequency = %s;
            """
            values = (medicine['posology_dose'], medicine['posology_frequency'])
            cur.execute(statement, values)

            result = cur.fetchone()
            if result is None:
                # Posology does not exist, insert it
                statement = """
                    INSERT INTO posologies (dosage, frequency) VALUES (%s, %s) RETURNING posology_id;
                """
                values = (medicine['posology_dose'], medicine['posology_frequency'])
                cur.execute(statement, values)

                posology_id = cur.fetchone()[0]
            else:
                posology_id = result[0]
            
            # Insert current posology and medication in posologies_medicines table if does not exist
            statement = """
                SELECT posology_id FROM posologies_medicines WHERE posology_id = %s AND medication_id = %s;
            """
            values = (posology_id, medication_id)
            cur.execute(statement, values)

            result = cur.fetchone()
            if result is None:
                statement = """
                    INSERT INTO posologies_medicines (posology_id, medication_id) VALUES (%s, %s);
                """
                values = (posology_id, medication_id)
                cur.execute(statement, values)

            # Insert the prescription and posology in posologies_prescriptions table
            statement = """
                INSERT INTO posologies_prescriptions (posology_id, presc_id) VALUES (%s, %s);
            """
            values = (posology_id, presc_id)
            cur.execute(statement, values)

            # Insert the medicine and prescription in prescriptions_medicines table
            statement = """
                INSERT INTO prescriptions_medicines (medication_id, presc_id) VALUES (%s, %s);
            """
            values = (medication_id, presc_id)
            cur.execute(statement, values)
        
        # Query to insert the prescription in the appointments_prescriptions or hospitalizations_prescriptions
        if payload['type'] == 'hospitalization':
            statement = """
                INSERT INTO hospitalizations_prescriptions (hosp_id, presc_id) VALUES (%s, %s);
            """
            values = (event_id, presc_id)
            cur.execute(statement, values)

        elif payload['type'] == 'appointment':
            # Query to verify if appointment already has a prescription
            statement = """
                SELECT app_id FROM appointments_prescriptions WHERE app_id = %s;
            """
            values = (event_id, )
            cur.execute(statement, values)

            result = cur.fetchone()
            if result is not None:
                raise Exception('Appointment already has a prescription!')
            
            # Query to get appointment_id, doctor_id and patient_id
            statement = """
                SELECT appointment_id, doctor_id, patient_id FROM appointments WHERE appointment_id = %s;
            """
            values = (event_id, )
            cur.execute(statement, values)

            app_id, doctor_id, patient_id = cur.fetchone()

            statement = """
                INSERT INTO appointments_prescriptions (app_id, patient_id, doctor_id, presc_id) 
                    VALUES (%s, %s, %s, %s);
            """
            values = (app_id, patient_id, doctor_id, presc_id)
            cur.execute(statement, values)

        # Commit the transaction
        conn.commit()

        response = {'status': StatusCodes['success'], 'results': presc_id}

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST dbproj/prescription/ - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': error, 'results': None}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## Execute Payment
##
@app.route('/dbproj/bills/<bill_id>', methods=['POST'])
def execute_payment(bill_id):
    logger.info(f'POST dbproj/bills/{bill_id}')

    payload = flask.request.get_json()

    logger.debug(f'POST dbproj/bills/{bill_id} - payload: {payload}')

    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)

    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)

    # Verify if the user is a patient 
    if jwt_token['user_type'] != user_types['patient']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only patients can pay their bills!'}
        return flask.jsonify(response)

    #
    # Query to get the patient_id of the bill and verify if token user is the same
    # 

    conn = db_connection()
    cur = conn.cursor()

    statement = """
        SELECT p.person_id
        FROM patients AS p
        JOIN appointments AS a ON p.person_id = a.patient_id
        JOIN bills AS b ON b.bill_id = a.bill_id
        WHERE b.bilL_id = %s
        UNION
        SELECT p.person_id
        FROM patients AS p
        JOIN surgeries AS s ON s.patient_id = p.person_id
        JOIN hospitalizations AS h ON s.hosp_id = h.hosp_id
        JOIN bills AS b ON b.bill_id = h.bill_id
        WHERE b.bilL_id = %s;
    """
    values = (bill_id, bill_id)

    try:
        cur.execute(statement, values)
        result = cur.fetchone()

        if result[0] is None:
            raise Exception('Bill {bill_id} does not exist!')
        
        if result[0] != jwt_token['user_id']:
            logger.debug(f'Bill {bill_id} does not belong to user {jwt_token["user_id"]}')
            raise Exception('You can only pay your own bills!')

        #
        # Validate payload
        #

        if 'amount' not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': 'amount is required!'}
            return flask.jsonify(response)
        
        if 'payment_method' not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': 'payment method is required!'}
            return flask.jsonify(response)
    
        #
        # SQL query
        #
    
        # Perform the payment and update bill status if necessary
        statement = """
            CALL update_bills(%s, %s, %s, %s);
        """
        values = (payload['amount'], payload['payment_method'], bill_id, None)

        cur.execute(statement, values)
        remaining_amount = cur.fetchone()[0]
    
        # Commit the transaction
        conn.commit()

        response = {'status': StatusCodes['success'], 'results': remaining_amount}

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST dbproj/bills/f{bill_id} - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': error, 'results': None}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## List Top 3 patients
##
##
@app.route('/dbproj/top3', methods=['GET'])
def get_top_clients():
    logger.info('GET /dbproj/top3')
    
    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)

    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)

    # Verify if the user is a assistant
    if jwt_token['user_type'] != user_types['assistant']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only assistants can get top3 patients'}
        return flask.jsonify(response)

    #
    # SQL query
    #    

    conn = db_connection()
    cur = conn.cursor()

    # Query to get the top 3 clients
    statement = """
        SELECT
            p.person_name AS patient_name,
            COALESCE(total_appointments.total_paid, 0) + COALESCE(total_hospitalizations.total_paid, 0) AS total_paid,
            service_details.service_type,
            service_details.service_id,
            service_details.service_date,
            service_details.doctor_id,
            service_details.doctor_name,
            service_details.app_type, -- Buscando app_type diretamente de appointments
            service_details.surgery_id, -- ID da cirurgia
            service_details.surgery_type, -- Tipo de cirurgia
            service_details.payment_for_service
        FROM patients p
        LEFT JOIN (
            SELECT p.person_id, SUM(py.payment) AS total_paid
            FROM patients p
            JOIN appointments a ON p.person_id = a.patient_id
            JOIN bills b ON a.bill_id = b.bill_id
            JOIN payments py ON b.bill_id = py.bill_id
            WHERE EXTRACT(YEAR FROM py.payment_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                AND EXTRACT(MONTH FROM py.payment_date) = EXTRACT(MONTH FROM CURRENT_DATE)
            GROUP BY p.person_id
        ) total_appointments ON p.person_id = total_appointments.person_id
        LEFT JOIN (
            SELECT p.person_id, SUM(py.payment) AS total_paid
            FROM patients p
            JOIN surgeries s ON p.person_id = s.patient_id
            JOIN hospitalizations h ON s.hosp_id = h.hosp_id
            JOIN bills b ON h.bill_id = b.bill_id
            JOIN payments py ON b.bill_id = py.bill_id
            WHERE EXTRACT(YEAR FROM py.payment_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                AND EXTRACT(MONTH FROM py.payment_date) = EXTRACT(MONTH FROM CURRENT_DATE)
            GROUP BY p.person_id
        ) total_hospitalizations ON p.person_id = total_hospitalizations.person_id
        JOIN (
            SELECT 
                'appointment' AS service_type,
                a.appointment_id AS service_id,
                a.app_date AS service_date,
                d.person_id AS doctor_id,
                e.person_name AS doctor_name,
                py.payment AS payment_for_service,
                p.person_id AS patient_id,
                'Consulta' AS appointment_type, -- Definindo a coluna appointment_type
                a.app_type AS app_type, -- Buscando app_type diretamente de appointments
                NULL AS surgery_id, -- Para consultas, o surgery_id é NULL
                NULL AS surgery_type, -- Para consultas, o surgery_type é NULL
                a.appointment_id -- Adicionando o appointment_id
            FROM patients p
            JOIN appointments a ON p.person_id = a.patient_id
            JOIN bills b ON a.bill_id = b.bill_id
            JOIN payments py ON b.bill_id = py.bill_id
            JOIN doctors d ON a.doctor_id = d.person_id
            JOIN employees e ON d.person_id = e.person_id
            WHERE EXTRACT(YEAR FROM py.payment_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                AND EXTRACT(MONTH FROM py.payment_date) = EXTRACT(MONTH FROM CURRENT_DATE)
                AND a.app_type IN ('GERAL', 'CARDIOLOGIA', 'DERMATOLOGIA', 'OFTALMOLOGIA', 'PEDIATRIA', 'PSIQUIATRIA', 'REUMATOLOGIA', 'ORTOPEDIA', 'ANESTESIA')
            
            UNION ALL

            SELECT 
                'hospitalization' AS service_type,
                h.hosp_id AS service_id,
                h.start_date AS service_date,
                d.person_id AS doctor_id,
                e.person_name AS doctor_name,
                py.payment AS payment_for_service,
                p.person_id AS patient_id,
                NULL AS appointment_type, -- Para hospitalizações, o appointment_type é NULL
                NULL AS app_type, -- Para hospitalizações, o app_type é NULL
                s.surgery_id, -- ID da cirurgia
                s.surgery_type, -- Tipo de cirurgia
                NULL AS appointment_id -- O appointment_id é NULL para hospitalizações
            FROM patients p
            JOIN surgeries s ON p.person_id = s.patient_id
            JOIN hospitalizations h ON s.hosp_id = h.hosp_id
            JOIN bills b ON h.bill_id = b.bill_id
            JOIN payments py ON b.bill_id = py.bill_id
            JOIN doctors d ON s.doctor_id = d.person_id
            JOIN employees e ON d.person_id = e.person_id
            WHERE EXTRACT(YEAR FROM py.payment_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                AND EXTRACT(MONTH FROM py.payment_date) = EXTRACT(MONTH FROM CURRENT_DATE)
        ) service_details ON p.person_id = service_details.patient_id
        ORDER BY total_paid DESC;
    """

    try:
        cur.execute(statement)
        result = cur.fetchall()

        if result == []:
            raise Exception('No patients found!')

        patients_data = []
        patients_grouped = {}
        
        for row in result:
            p_name, total_amount, type, *procedure_data = row

            # Get details of the procedure
            if type == 'appointment':
                procedure_id = procedure_data[0]
                procedure_key = tuple(procedure_data[1:])  # Exclude the cost field
            elif type == 'hospitalization':
                procedure_id = procedure_data[0]
                procedure_key = tuple(procedure_data[1:])  # Exclude the cost field

            procedure_cost = procedure_data[-1]

            if p_name not in patients_grouped:
                patients_grouped[p_name] = {
                    'patient_name': p_name,
                    'total_amount': total_amount,
                    'procedures': []
                }

            # Verify if the procedure already exists
            existing_procedure_index = None
            for index, existing_procedure in enumerate(patients_grouped[p_name]['procedures']):
                if existing_procedure['id'] == procedure_id:
                    existing_procedure_index = index
                    break

            # Procedure already exists, update the cost
            if existing_procedure_index is not None:
                patients_grouped[p_name]['procedures'][existing_procedure_index]['cost'] += procedure_cost
            else:
                # If the procedure does not exist, add it
                if type == 'appointment':
                    patients_grouped[p_name]['procedures'].append({
                        'id': procedure_id,
                        'type': type,
                        'date': date_to_str(procedure_key[0]),
                        'doctor_id': procedure_key[1],
                        'doctor_name': procedure_key[2],
                        'appointment_type': procedure_key[3],
                        'cost': procedure_cost
                    })
                elif type == 'hospitalization':
                    patients_grouped[p_name]['procedures'].append({
                        'id': procedure_id,
                        'type': type,
                        'date': date_to_str(procedure_key[0]),
                        'doctor_id': procedure_key[1],
                        'doctor_name': procedure_key[2],
                        'surgery_id': procedure_key[4],
                        'surgery_type': procedure_key[5],
                        'cost': procedure_cost
                    })

        for patient_data in patients_grouped.values():
            patients_data.append(patient_data)
        
        response = {'status': StatusCodes['success'], 'results': patients_data[:3]}

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'GET dbproj/top3 - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': error, 'results': None}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
##  Get Daily Summary
##
##
@app.route('/dbproj/daily/<date>', methods=['GET'])
def get_daily_summary(date):
    logger.info(f'GET /dbproj/daily/{date}')

    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)

    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)

    # Verify if the user is a assistant
    if jwt_token['user_type'] != user_types['assistant']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only assistants can get daily summary'}
        return flask.jsonify(response)
    
    if not date:
        response = {'status': StatusCodes['api_error'], 'errors': 'Date is required!'}
        return flask.jsonify(response)
    
    # Validate date format and parse the date string into year, month, and day
    if not validate_date_format(date):
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid date format!'}
        return flask.jsonify(response)
    
    year, month, day = date.split('-')
    year, month, day = int(year), int(month), int(day)
    
    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()

    date_str = f"{year}-{month:02d}-{day:02d}" 

    statement = """
        SELECT 
            (SELECT COUNT(*) FROM surgeries WHERE surgery_date = %s),
            (SELECT COALESCE(SUM(payment), 0) FROM payments WHERE payment_date = %s),
            (SELECT COUNT(*) FROM prescriptions WHERE presc_date = %s);
    """
    values = (date_str, date_str, date_str)

    try:
        cur.execute(statement, values)
        row = cur.fetchone()

        if row is None:
            raise Exception('No data found for the given date!')

        response = {
            'status': StatusCodes['success'], 
            'results': {
                'amount_spent': row[1], 
                'surgeries': row[0], 
                'prescriptions': row[2]
            }
        }

    except (Exception, psycopg2.DatabaseError) as error:
        # an error occurred, rollback
        conn.rollback()

        logger.error(f'POST dbproj/daily/{date} - error: {error}')

        error = str(error).split('\n')[0]
        response = {'status': StatusCodes['internal_error'], 'errors': error, 'results': None}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## See Monthly Report
##
@app.route('/dbproj/report', methods=['GET'])
def get_monthly_surgery_report():
    logger.info('GET /dbproj/report')
    
    #
    # Validate Authorization header
    #

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Authorization header is required!'}
        return flask.jsonify(response)

    jwt_token = validate_token(jwt_token)
    if not jwt_token:
        response = {'status': StatusCodes['api_error'], 'errors': 'Invalid or Expirated token!'}
        return flask.jsonify(response)

    # Verify if the user is a assistant
    if jwt_token['user_type'] != user_types['assistant']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only assistants can schedule appointments!'}
        return flask.jsonify(response)

    #
    # SQL query
    #    
    conn = db_connection()
    cur = conn.cursor()

    # Query to get the number of surgeries per doctor in the last 12 months
    statement = """
        SELECT dms.surgery_month, dms.doctor_name, dms.num_surgeries
        FROM (
            SELECT to_char(s.surgery_date, 'YYYY-MM') AS surgery_month, e.person_name AS doctor_name, COUNT(s.surgery_id) AS num_surgeries
            FROM surgeries AS s
            JOIN employees AS e ON s.doctor_id = e.person_id
            WHERE s.surgery_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '12 months'
                AND s.surgery_date < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
            GROUP BY to_char(s.surgery_date, 'YYYY-MM'), e.person_name
        ) dms
        JOIN (
            SELECT surgery_month, MAX(num_surgeries) AS max_surgeries
            FROM (
                SELECT to_char(s.surgery_date, 'YYYY-MM') AS surgery_month, e.person_name AS doctor_name, COUNT(s.surgery_id) AS num_surgeries
                FROM surgeries AS s
                JOIN employees AS e ON s.doctor_id = e.person_id
                WHERE s.surgery_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '12 months'
                    AND s.surgery_date < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
                GROUP BY to_char(s.surgery_date, 'YYYY-MM'), e.person_name
            ) inner_query
            GROUP BY surgery_month
        ) max_surgeries ON dms.surgery_month = max_surgeries.surgery_month AND dms.num_surgeries = max_surgeries.max_surgeries
        ORDER BY dms.surgery_month;
    """

    try:
        cur.execute(statement)
        rows = cur.fetchall()

        logger.debug('GET /dbproj/report - parse')

        results = []
        for row in rows:
            logger.debug(row)

            content = {
                'month': row[0],
                'doctor_name': row[1],
                'num_surgeries': row[2]
            }

            results.append(content)
        
        if results == []:
            raise Exception('No surgeries found!')

        response = {'status': StatusCodes['success'], 'report': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /dbproj/report - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

##
## Validate Token
##
def validate_token(jwt_token):
    try:
        decoded_token = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

##
## Validate Date Format
##
def validate_date_format(date_string):
    year, month, day = date_string.split('-')
    year, month, day = int(year), int(month), int(day)

    # Check if the date is valid
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return False
    
    try:
        # Tentativa de converter a string para um objeto datetime
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def date_to_str(d):
    if isinstance(d, datetime):
        return d.isoformat()
    return d
    
    
if __name__ == '__main__':
    # set up logging
    logging.basicConfig(filename='log_file.log')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    host = '127.0.0.1'
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')