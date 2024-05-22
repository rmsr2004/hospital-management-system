import flask
import logging
import psycopg2
import time
import jwt
import secrets

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
    db = psycopg2.connect(
        user = 'postgres',
        password = 'root',
        host = '127.0.0.1',
        port = '5432',
        database = 'hospital'
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
@app.route('/dbproj/register/doctor', methods=['POST'])
def add_doctor():
    logger.info('POST /dbproj/register/doctor')

    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/register/doctor - payload: {payload}')

    #
    # Validate payload.
    #

    if 'name' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'name value not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc value not in payload'}
        return flask.jsonify(response)
    if 'address' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'address value not in payload'}
        return flask.jsonify(response)
    if 'phone' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'phone value not in payload'}
        return flask.jsonify(response)
    if 'username' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'username value not in payload'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password value not in payload'}
        return flask.jsonify(response)
    if 'email' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'email value not in payload'}
        return flask.jsonify(response)
    if 'contract' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'contract details not in payload'}
        return flask.jsonify(response)
    if 'salary' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'salary value not in contract payload'}
        return flask.jsonify(response)
    if 'start_date' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'start date value not in contract payload'}
        return flask.jsonify(response)
    if 'final_date' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'final date value not in contract payload'}
        return flask.jsonify(response)
    if 'ctype_id' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'ctype_id value not in contract payload'}
        return flask.jsonify(response)
    if 'medical_license' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'medical_license details not in payload'}
        return flask.jsonify(response)
    if 'issue_date' not in payload['medical_license']:
        response = {'status': StatusCodes['api_error'], 'results': 'issue_date value not in medical_license payload'}
        return flask.jsonify(response)
    if 'expiration_date' not in payload['medical_license']:
        response = {'status': StatusCodes['api_error'], 'results': 'expiration_date value not in medical_license payload'}
        return flask.jsonify(response)

    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()

    # Query to insert the doctor
    statement = """
        INSERT INTO employees (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, salary, start_date, final_date, ctype_id, person_type) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); 

        INSERT INTO doctors (person_id, ml_issue_date, ml_expiration_date) 
                SELECT person_id, %s, %s FROM employees WHERE person_cc = %s
        RETURNING person_id;
    """
    values = (payload['cc'], payload['name'], payload['address'], payload['phone'], payload['username'], payload['password'], 
              payload['email'], payload['contract']['salary'], payload['contract']['start_date'], payload['contract']['final_date'], 
              payload['contract']['ctype_id'], "2", payload['medical_license']['issue_date'], payload['medical_license']['expiration_date'],
              payload['cc'])

    try:
        cur.execute(statement, values)

        doctor_id = cur.fetchone()[0]
        if doctor_id is None:
            raise Exception('Error inserting doctor!')
        
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
@app.route('/dbproj/register/nurse', methods=['POST'])
def add_nurse():
    logger.info('POST /dbproj/register/nurse')

    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/register/nurse - payload: {payload}')

    #
    # Validate payload.
    #

    if 'name' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'name value not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc value not in payload'}
        return flask.jsonify(response)
    if 'address' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'address value not in payload'}
        return flask.jsonify(response)
    if 'phone' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'phone value not in payload'}
        return flask.jsonify(response)
    if 'username' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'username value not in payload'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password value not in payload'}
        return flask.jsonify(response)
    if 'email' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'email value not in payload'}
        return flask.jsonify(response)
    if 'contract' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'contract details not in payload'}
        return flask.jsonify(response)
    if 'salary' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'salary value not in contract payload'}
        return flask.jsonify(response)
    if 'start_date' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'start date value not in contract payload'}
        return flask.jsonify(response)
    if 'final_date' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'final date value not in contract payload'}
        return flask.jsonify(response)
    if 'ctype_id' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'ctype_id value not in contract payload'}
        return flask.jsonify(response)
    if 'categories' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'categories values not in payload'}
        return flask.jsonify(response)
    if payload['categories'] == []:
        response = {'status': StatusCodes['api_error'], 'results': 'categories values is empty'}
        return flask.jsonify(response)
    
    categories = payload['categories']

    #
    # SQL query
    #
    
    conn = db_connection()
    cur = conn.cursor()

    # Query to insert the nurse
    insert_statement = """
        INSERT INTO employees (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, salary, start_date, final_date, ctype_id, person_type) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s);

        INSERT INTO nurses (person_id) 
        SELECT person_id FROM employees WHERE person_cc = %s RETURNING person_id;
    """
    values = (payload['cc'], payload['name'], payload['address'], payload['phone'], payload['username'], payload['password'], payload['email'], 
              payload['contract']['salary'], payload['contract']['start_date'], payload['contract']['final_date'], payload['contract']['ctype_id'],
              "3", payload['cc'])

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
@app.route('/dbproj/register/assistant', methods=['POST'])
def add_assistant():
    logger.info('POST /dbproj/register/assistant')

    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/register/assistant - payload: {payload}')

    #
    # Validate payload.
    #

    if 'name' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'name value not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc value not in payload'}
        return flask.jsonify(response)
    if 'address' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'address value not in payload'}
        return flask.jsonify(response)
    if 'phone' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'phone value not in payload'}
        return flask.jsonify(response)
    if 'username' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'username value not in payload'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password value not in payload'}
        return flask.jsonify(response)
    if 'email' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'email value not in payload'}
        return flask.jsonify(response)
    if 'contract' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'contract details not in payload'}
        return flask.jsonify(response)
    if 'salary' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'salary value not in contract payload'}
        return flask.jsonify(response)
    if 'start_date' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'start date value not in contract payload'}
        return flask.jsonify(response)
    if 'final_date' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'final date value not in contract payload'}
        return flask.jsonify(response)
    if 'ctype_id' not in payload['contract']:
        response = {'status': StatusCodes['api_error'], 'results': 'ctype_id value not in contract payload'}
        return flask.jsonify(response)

    #
    # SQL Query
    #

    conn = db_connection()
    cur = conn.cursor()


    # query to insert the assistant
    statement = """
        INSERT INTO employees (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, salary, start_date, final_date, ctype_id, person_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        INSERT INTO assistants (person_id) 
            SELECT person_id FROM employees WHERE person_cc = %s RETURNING person_id;
    """
    values = (payload['cc'], payload['name'], payload['address'], payload['phone'], payload['username'], payload['password'], payload['email'], 
              payload['contract']['salary'], payload['contract']['start_date'], payload['contract']['final_date'], payload['contract']['ctype_id'],
              "4", payload['cc'])

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
@app.route('/dbproj/register/patient', methods=['POST'])
def add_patient():
    logger.info('POST /dbproj/register/patient')

    payload = flask.request.get_json()

    logger.debug(f'POST /dbproj/register/patient - payload: {payload}')

    #
    # Validate payload.
    #

    if 'name' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'name value not in payload'}
        return flask.jsonify(response)
    if 'cc' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'cc value not in payload'}
        return flask.jsonify(response)
    if 'address' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'address value not in payload'}
        return flask.jsonify(response)
    if 'phone' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'phone value not in payload'}
        return flask.jsonify(response)
    if 'username' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'username value not in payload'}
        return flask.jsonify(response)
    if 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'password value not in payload'}
        return flask.jsonify(response)
    if 'email' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'email value not in payload'}
        return flask.jsonify(response)

    #
    # SQL Query
    #

    conn = db_connection()
    cur = conn.cursor()

    # query to insert the patient
    statement = """
        INSERT INTO patients (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING person_id;
    """
    values = (payload['cc'], payload['name'], payload['address'], payload['phone'], payload['username'], payload['password'], payload['email'],
              "1")

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
        SELECT person_type AS user_type, person_id AS user_id
        FROM patients
        WHERE person_username = %s AND person_password = %s
        UNION
        SELECT person_type AS user_type, person_id AS user_id
        FROM employees
        WHERE person_username = %s AND person_password = %s;
    """
    values = (payload['username'], payload['password'], payload['username'], payload['password'])

    try:
        cur.execute(statement, values)
        result = cur.fetchone()

        if result:
            user_type, user_id = result
            
            jwt_payload = { 'user_id': int(user_id), 'user_type': int(user_type)}
            jwt_token = jwt.encode(jwt_payload, secret_key, algorithm='HS256')
            
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

    if 'doctor_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'doctor_id is required!'}
        return flask.jsonify(response)
    if 'date'  not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'date is required!'}
        return flask.jsonify(response)
    if 'hour' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'hour is required!'}
        return flask.jsonify(response)
    if 'minutes' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'minutes is required!'}
        return flask.jsonify(response)
    if 'type' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'type is required!'}
        return flask.jsonify(response)
    if 'room' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'room is required!'}
        return flask.jsonify(response)
    if 'nurses' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'nurses is required!'}
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
        WHERE e.person_type = 2 AND e.person_id = %s AND ( %s = 'GERAL' AND sd.spec_id IS NULL 
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
        values = (payload['doctor_id'], payload['date'], payload['hour'], payload['minutes']);
        cur.execute(statement, values)

        result = cur.fetchone()[0]
        if not result:
            raise Exception('Doctor is already booked at this time!')
        

        # Query to verify if the room is available
        statement =  """
            SELECT is_room_available_for_appointment(%s, %s, %s, %s);
        """
        values = (payload['room'], payload['date'], payload['hour'], payload['minutes']);
        cur.execute(statement, values)

        result = cur.fetchone()[0]
        if not result:
            raise Exception('Room is already booked at this time!')
    

        # Query to insert the appointment
        statement =  """
            INSERT INTO appointments (doctor_id, patient_id, app_date, app_hour, app_minutes, app_type, app_room, app_status, app_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING appointment_id;
        """
        values = (payload['doctor_id'], jwt_token['user_id'], payload['date'], payload['hour'], payload['minutes'], payload['type'], 
                  payload['room'], 0, 30)
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

        conn.commit()
        response = {'status': StatusCodes['success'], 'results': appointment_id}

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
## Schedule Surgery
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

    # Verify if the user is a patient
    if jwt_token['user_type'] != user_types['assistant']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only assistants can schedule appointments!'}
        return flask.jsonify(response)
    
    #
    # Validate payload
    #

    if 'patient_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'patient_id is required!'}
        return flask.jsonify(response)
    if 'doctor_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'doctor_id is required!'}
        return flask.jsonify(response)
    if 'nurses' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'nurses is required!'}
        return flask.jsonify(response)
    
    # Verify if there is a responsible nurse and assign the nurse to a variable and remove it from the list
    nurses = payload['nurses'] # [[id, 'RESPONSAVEL']]
    nurse_responsible_id = None
    for nurse in nurses:
        if nurse[1] == "RESPONSAVEL":
            nurse_responsible_id = nurse[0]
            nurses.remove(nurse)
            break

    if nurse_responsible_id is None and hospitalization_id is None:
        response = {'status': StatusCodes['api_error'], 'errors': 'nurses must have a responsible nurse!'}
        return flask.jsonify(response)
    if 'date' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'date is required!'}
        return flask.jsonify(response)
    if 'type' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'type is required!'}
        return flask.jsonify(response)
    if 'room' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'room is required!'}
        return flask.jsonify(response)
    if 'hour' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'hour is required!'}
        return flask.jsonify(response)
    if 'minutes' not in payload:
        response = {'status': StatusCodes['api_error'], 'errors': 'minutes is required!'}
        return flask.jsonify(response)
    
    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()


    # Query to verify if the doctor exists and if the doctor type given corresponds to real doctor type
    statement =  """
        SELECT d.person_id, e.person_name, s.specialization, ss.sub_spec 
        FROM doctors AS d
        JOIN specialisations_doctors AS sd ON d.person_id = sd.doctor_id
        JOIN specialisations AS s ON sd.spec_id = s.spec_id
        JOIN sub_specialisations AS ss ON sd.spec_id = ss.spec_id
        JOIN employees AS e ON e.person_id = sd.doctor_id
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

            result = cur.fetchone()[0]
            if result is None:
                raise Exception('Nurse is not a valid nurse!')
            
            # Query to generate the hospitalization room
            statement = """
                SELECT get_first_available_room(%s);
            """
            values = (payload['date'], )
            cur.execute(statement, values)

            room = cur.fetchone()[0]
            if room is None:
                raise Exception('No rooms available for hospitalization!')
            
            # Query to insert the hospitalization
            statement = """
                INSERT INTO hospitalizations (start_date, final_date, room, assistant_id, nurse_id) 
                    VALUES (%s, %s, %s, %s, %s) RETURNING hosp_id;
            """
            values = (payload['date'], payload['date'], room, jwt_token['user_id'], nurse_responsible_id)
            
            cur.execute(statement, values)
            hospitalization_id = cur.fetchone()[0]

            logger.debug(f'POST /dbproj/surgery - hospitalization created')

        # Associate the surgery with the hospitalization
        statement = """
            INSERT INTO surgeries (doctor_id, patient_id, surgery_date, surgery_hour, surgery_minutes, surgery_type, surgery_room, 
                                   surgery_status, hosp_id, surgery_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 120) RETURNING surgery_id;
        """
        values = (payload['doctor_id'], payload['patient_id'], payload['date'], payload['hour'], payload['minutes'], payload['type'], 
                    payload['room'], 0, hospitalization_id)
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

            result = cur.fetchone()[0]
            if result != 'CIRURGIAS':
                raise Exception('Nurse is not a valid nurse!')
            

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
        logger.error(f'POST dproj/appointment - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error), 'results': None}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()
    return  

##
## See Appointments
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

def validate_token(jwt_token):
    try:
        decoded_token = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
    
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