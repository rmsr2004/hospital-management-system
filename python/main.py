import flask
import logging
import psycopg2
import jwt
import secrets
from dotenv import dotenv_values
from cryptography.fernet import Fernet

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

    required_fields = ['name', 'cc', 'address', 'phone', 'username', 'password', 'email', 'contract', 'medical_license']
    required_contract_fields = ['salary', 'start_date', 'final_date', 'ctype_id']
    required_medical_license_fields = ['issue_date', 'expiration_date']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in payload'}
            return flask.jsonify(response)
        
    # Verify contract fields
    for field in required_contract_fields:
        if field not in payload['contract']:
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in contract payload'}
            return flask.jsonify(response)
        
    # Verify medical license fields
    for field in required_medical_license_fields:
        if field not in payload['medical_license']:
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in medical_license payload'}
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
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in payload'}
            return flask.jsonify(response)
        
    # Verify contract fields
    for field in required_contract_fields:
        if field not in payload['contract']:
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in contract payload'}
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
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in payload'}
            return flask.jsonify(response)
        
    # Verify contract fields
    for field in required_contract_fields:
        if field not in payload['contract']:
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in contract payload'}
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
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in payload'}
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

            logger.debug(f'PUT /dbproj/user - user_type: {user_type}, user_id: {user_id}, decrypted_password: {decrypted_password}')

            if decrypted_password != payload['password']:
                raise Exception('Invalid password!')
            
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
        SELECT m.dosage, m.medication, pr.prob, s.side_effect
        FROM appointments_prescriptions AS ap
        JOIN prescriptions AS pres ON ap.presc_id = pres.presc_id
        JOIN prescriptions_medicines AS pm ON pres.presc_id = pm.presc_id
        JOIN medicines AS m ON pm.medication_id = m.medication_id
        JOIN side_effects_medicines AS sem ON m.medication_id = sem.medication_id
        JOIN side_effects AS s ON sem.side_effect_id = s.side_effect_id
        JOIN probabilities AS pr ON s.prob_id = pr.prob_id
        WHERE ap.patient_id = %s;
    """
    values = (person_id, )

    try:
        cur.execute(statement, values)
        prescriptions = cur.fetchall()

        if prescriptions:
            response = {
                'status': StatusCodes['success'],
                'results': [
                    {
                        'dosage': pres[0],
                        'medication': pres[1],
                        'prob': pres[2],
                        'side_effect': pres[3]
                    } for pres in prescriptions
                ]
            }
        else:
            statement = """
                SELECT hosp_id FROM surgeries WHERE patient_id = %s
            """
            values = (person_id, )
            cur.execute(statement, values)

            result = cur.fetchone()
            hosp_id = result[0]
            if result:
                hosp_id = result[0]
                
                statement = """
                    SELECT m.dosage, m.medication, pr.prob, s.side_effect
                    FROM hospitalizations_prescriptions AS hp
                    JOIN prescriptions AS pres ON hp.presc_id = pres.presc_id
                    JOIN prescriptions_medicines AS pm ON pres.presc_id = pm.presc_id
                    JOIN medicines AS m ON pm.medication_id = m.medication_id
                    JOIN side_effects_medicines AS sem ON m.medication_id = sem.medication_id
                    JOIN side_effects AS s ON sem.side_effect_id = s.side_effect_id
                    JOIN probabilities AS pr ON s.prob_id = pr.prob_id
                    WHERE hp.hosp_id = %s;
                """
                values = (hosp_id, )
                cur.execute(statement, values)
                
                prescriptions = cur.fetchall()

                if prescriptions:
                    response = {
                        'status': StatusCodes['success'],
                        'results': [
                            {
                                'dosage': pres[0],
                                'medication': pres[1],
                                'prob': pres[2],
                                'side_effect': pres[3]
                            } for pres in prescriptions
                        ]
                    }
                else:
                    raise Exception('No prescriptions found for the given ID.')
            else:
                raise Exception('No prescriptions found for the given ID.')

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
    if jwt_token['user_type'] == user_types['doctor']:
        response = {'status': StatusCodes['api_error'], 'errors': 'Only doctors can add prescriptions!'}
        return flask.jsonify(response)
    
    #
    # Validate payload
    #

    required_fields = ['prescriptions', 'medicines', 'type']
    medicine_fields = ['medicine', 'dosage']

    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)
    
    if prescription['type'] not in ['hospitalization', 'appointment']:
        response = {'status': 'api_error', 'errors': 'Invalid type! Must be "hospitalization" or "appointment".'}
        return flask.jsonify(response)

    prescription = payload['prescriptions'][0]
    medicine = prescription['medicines'][0]

    for field in medicine_fields:
        if field not in medicine:
            response = {'status': StatusCodes['api_error'], 'errors': f'{field} value not in payload'}
            return flask.jsonify(response)
    
    #
    # SQL query
    #

    conn = db_connection()
    cur = conn.cursor()

    # Query to insert the prescription
    statement = """
        INSERT INTO prescriptions DEFAULT VALUES RETURNING presc_id
    """

    try:
        cur.execute(statement)
        presc_id = cur.fetchone()[0]

        # Query to check if medicine exists in medicines table
        statement = """
            SELECT medication_id FROM medicines WHERE medication = %s AND dosage = %s;
        """
        values = (medicine['medicine'], medicine['dosage'])
        cur.execute(statement, values)

        result = cur.fetchone()
        if result is None:
            raise Exception('The specified medicine does not exist!')

        medication_id = result[0]

        # Query to insert the medicine in prescriptions_medicines table
        statement = """
            INSERT INTO prescriptions_medicines (presc_id, medication_id) VALUES (%s, %s);
        """
        values = (presc_id, medication_id)
        cur.execute(statement, values)

        if prescription['type'] == 'hospitalization':
            if 'doctor' not in prescription:
                raise Exception('doctor is required for hospitalization type!')
            
            doctor_id = prescription['doctor']

            # Query to find hosp_id using doctor_id from surgeries table
            statement = """
                SELECT hosp_id FROM surgeries WHERE doctor_id = %s;
            """
            values = (doctor_id, )
            cur.execute(statement, values)

            result = cur.fetchone()
            if result is None:
                raise Exception('No hospitalization found for the given doctor!')
            
            hosp_id = result[0]
            
            statement = """
                INSERT INTO hospitalizations_prescriptions (hosp_id, presc_id) VALUES (%s, %s);
            """
            values = (hosp_id, presc_id)
            cur.execute(statement, values)

        elif prescription['type'] == 'appointment':
            if 'doctor' not in prescription:
                raise Exception('Doctor is required for appointments type!')

            doctor_id = prescription['doctor']

            # Query to find patient_id using doctor_id from appointments table
            statement = """
                SELECT patient_id FROM appointments WHERE doctor_id = %s;
            """
            values = (doctor_id, )
            cur.execute(statement, values)

            result = cur.fetchone()

            if result is None:
                raise Exception('No appointment found for the given doctor!')
            
            patient_id = result[0]

            statement = """
                SELECT add_appointment_prescription(%s, %s, %s);
            """
            values = (patient_id, doctor_id, presc_id)
            cur.execute(statement, values)

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
    values = (int(bill_id), int(bill_id))

    try:
        cur.execute(statement, values)
        result = cur.fetchone()

        if result is None:
            raise Exception('Bill {bill_id} does not exist!')
        
        if result != jwt_token['user_id']:
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
            CALL update_bills(%s, %s, %s);
        """
        values = (float(payload['amount']), int(payload['payment_method']), int(bill_id))

        cur.execute(statement, values)
        remaining_amount = cur.fetchone()[0]
    
        # Commit the transaction
        conn.commit()

        response = {'status': StatusCodes['success'], 'results': remaining_amount}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /departments - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

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
        WITH combined_payments AS (
            -- Select payments from appointments
            SELECT p.person_id, p.person_name AS client_name, a.appointment_id AS procedure_id, a.doctor_id,
                   a.app_date AS procedure_date, SUM(pm.payment) AS total_payment
            FROM patients p
            JOIN appointments a ON p.person_id = a.patient_id
            JOIN bills b ON a.bill_id = b.bill_id
            JOIN payments pm ON b.bill_id = pm.bill_id
            WHERE DATE_TRUNC('month', a.app_date) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY p.person_id, p.person_name, a.appointment_id, a.doctor_id, a.app_date
            UNION ALL
            SELECT p.person_id, p.person_name AS client_name, h.hosp_id AS procedure_id, s.doctor_id,h.start_date AS procedure_date,
                   SUM(pm.payment) AS total_payment
            FROM patients p
            JOIN surgeries s ON p.person_id = s.patient_id
            JOIN hospitalization        
        # Formata os resultados em um formato mais legível para o Postmans h ON s.hosp_id = h.hosp_id
            JOIN bills b ON h.bill_id = b.bill_id
            JOIN payments pm ON b.bill_id = pm.bill_id
            WHERE DATE_TRUNC('month', h.start_date) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY p.person_id, p.person_name, h.hosp_id, s.doctor_id, h.start_date
        )
        SELECT client_name,procedure_id, doctor_id, procedure_date, total_payment
        FROM combined_payments
        ORDER BY total_payment DESC;
    """

    try:
        cur.execute()
        top_clients = cur.fetchall()

        if top_clients == []:
            raise Exception('No patients found!')

        results = []
        count = 0

        for client in top_clients:
            client_data = {
                'client_name': client[0],
                'appointment/hospitalizaiotn id': client[1],
                'doctor_id': client[2],
                'appointment/hospitalization date': client[3],
                'total_payment': float(client[4]) 
            }
            results.append(client_data)

            count += 1
            if count==3:
                break
            
        response = {'status': StatusCodes['success'], 'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /departments - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

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
        SELECT e.person_name AS doctor_name, COUNT(s.surgery_id) AS num_surgeries
        FROM surgeries AS s
        JOIN employees AS e ON s.doctor_id = e.person_id
        WHERE s.surgery_date >= (CURRENT_DATE - INTERVAL '12 months') 
            AND s.surgery_date <= CURRENT_DATE
        GROUP BY e.person_name
        ORDER BY num_surgeries DESC;
    """

    try:
        cur.execute(statement)
        rows = cur.fetchall()

        logger.debug('GET /dbproj/report - parse')

        results = []
        for row in rows:
            logger.debug(row)

            content = {
                'doctor_name': row[0],
                'num_surgeries': row[1]
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