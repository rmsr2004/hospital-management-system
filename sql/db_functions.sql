/*********************************************************
*	Database for Hospital Management System				 *
* 	Authors:											 *
*		- João Afonso dos Santos Simões (2022236316)	 *
*		- João Pinho Marques (2022234692)				 *
*		- Rodrigo Miguel Santos Rodrigues (2022233032)	 *
*												 		 *									
*	Created on:	28/05/2024								 *
**********************************************************
*	db_functions.sql: Create procedures, functions and   *
*                     triggers		                     *					
*********************************************************/

CREATE EXTENSION IF NOT EXISTS pgcrypto; -- Extension to use cryptographic functions

/* Checks if doctor is available for appointment */
CREATE OR REPLACE FUNCTION is_doctor_available_for_appointment(
    d_id INTEGER, 
    a_date DATE, 
    app_hour INTEGER, 
    app_minutes INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    appointment_start INTEGER := app_hour * 60 + app_minutes;
    appointment_end INTEGER := appointment_start + 30;
BEGIN
    -- Verify conflicts with surgeries
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries AS s
    WHERE s.doctor_id = d_id
      AND s.surgery_date = a_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < appointment_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + 120) > appointment_start
      );

    -- Verify conflicts with appointments
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments AS a
    WHERE a.doctor_id = d_id
      AND a.app_date = a_date
      AND (
          (a.app_hour * 60 + a.app_minutes) < appointment_end
          AND (a.app_hour * 60 + a.app_minutes + a.app_duration) > appointment_start
      );

    RETURN conflicting_surgeries = 0 AND conflicting_appointments = 0;
END;
$$ LANGUAGE plpgsql;

/* Checks if room is available for appointment */
CREATE OR REPLACE FUNCTION is_room_available_for_appointment(
    a_room BIGINT, 
    a_date DATE, 
    app_hour INTEGER, 
    app_minutes INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    appointment_start INTEGER := app_hour * 60 + app_minutes;
    appointment_end INTEGER := appointment_start + 30;
BEGIN
    -- Verify conflicts with surgeries
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries AS s
    WHERE s.surgery_room = a_room
      AND s.surgery_date = a_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < appointment_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + 120) > appointment_start
      );

    -- Verify conflicts with appointments
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments AS a
    WHERE a.app_room = a_room
      AND a.app_date = a_date
      AND (
          (a.app_hour * 60 + a.app_minutes) < appointment_end
          AND (a.app_hour * 60 + a.app_minutes + a.app_duration) > appointment_start
      );

    RETURN conflicting_surgeries = 0 AND conflicting_appointments = 0;
END;
$$ LANGUAGE plpgsql;

/* Checks if nurse is available for appointment */
CREATE OR REPLACE FUNCTION is_nurse_available_for_appointment(
    n_id INTEGER, 
    a_date DATE, 
    app_hour INTEGER, 
    app_minutes INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    appointment_start INTEGER := app_hour * 60 + app_minutes;
    appointment_end INTEGER := appointment_start + 30;
BEGIN
    -- Verify conflicts with surgeries
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries AS s
    JOIN roles_surgeries AS rs ON s.surgery_id = rs.surgery_id
    JOIN nurses_roles AS nr ON rs.role_id = nr.role_id
    WHERE nr.nurse_id = n_id
      AND s.surgery_date = a_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < appointment_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + s.surgery_duration) > appointment_start
      );

    -- Verify conflicts with appointments
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments AS a
    JOIN roles_appointments ra ON a.appointment_id = ra.app_id
    JOIN nurses_roles nr ON ra.role_id = nr.role_id
    WHERE nr.nurse_id = n_id
      AND a.app_date = a_date
      AND (
          (a.app_hour * 60 + a.app_minutes) < appointment_end
          AND (a.app_hour * 60 + a.app_minutes + a.app_duration) > appointment_start
      );
    RETURN conflicting_surgeries = 0 AND conflicting_appointments = 0;
END;
$$ LANGUAGE plpgsql;

/* Checks if doctor is available for surgery */
CREATE OR REPLACE FUNCTION is_doctor_available_for_surgery(
    d_id INTEGER, 
    s_date DATE, 
    surgery_hour INTEGER, 
    surgery_minutes INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    surgery_start INTEGER := surgery_hour * 60 + surgery_minutes;
    surgery_end INTEGER := surgery_start + 120; -- 2 hours duration (120 minutes)
BEGIN
    -- Verify conflicts with surgeries
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries AS s
    WHERE s.doctor_id = d_id
      AND s.surgery_date = s_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < surgery_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + 120) > surgery_start
      );

    -- Verify conflicts with appointments
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments AS a
    WHERE a.doctor_id = d_id
      AND a.app_date = s_date
      AND (
          (a.app_hour * 60 + a.app_minutes) < surgery_end
          AND (a.app_hour * 60 + a.app_minutes + a.app_duration) > surgery_start
      );

    RETURN conflicting_surgeries = 0 AND conflicting_appointments = 0;
END;
$$ LANGUAGE plpgsql;

/* Checks if room is available for surgery */
CREATE OR REPLACE FUNCTION is_room_available_for_surgery(
    s_room BIGINT, 
    s_date DATE, 
    surgery_hour INTEGER, 
    surgery_minutes INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    surgery_start INTEGER := surgery_hour * 60 + surgery_minutes;
    surgery_end INTEGER := surgery_start + 120; -- 2 hours duration (120 minutes)
BEGIN
    -- Verify conflicts with surgeries
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries AS s
    WHERE s.surgery_room = s_room
      AND s.surgery_date = s_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < surgery_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + 120) > surgery_start
      );

    -- Verify conflicts with appointments
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments AS a
    WHERE a.app_room = s_room
      AND a.app_date = s_date
      AND (
          (a.app_hour * 60 + a.app_minutes) < surgery_end
          AND (a.app_hour * 60 + a.app_minutes + a.app_duration) > surgery_start
      );

    RETURN conflicting_surgeries = 0 AND conflicting_appointments = 0;
END;
$$ LANGUAGE plpgsql;

/* Checks if nurse is available for surgery */
CREATE OR REPLACE FUNCTION is_nurse_available_for_surgery(
    n_id INTEGER, 
    s_date DATE, 
    surgery_hour INTEGER, 
    surgery_minutes INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    surgery_start INTEGER := surgery_hour * 60 + surgery_minutes;
    surgery_end INTEGER := surgery_start + 120;
BEGIN
    -- Verify conflicts with surgeries
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries AS s
    JOIN roles_surgeries AS rs ON s.surgery_id = rs.surgery_id
    JOIN nurses_roles AS nr ON rs.role_id = nr.role_id
    WHERE nr.nurse_id = n_id
    AND s.surgery_date = s_date
    AND (
        (s.surgery_hour * 60 + s.surgery_minutes) < surgery_end
        AND (s.surgery_hour * 60 + s.surgery_minutes + s.surgery_duration) > surgery_start
    );

    -- Verify conflicts with appointments
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments AS a
    JOIN roles_appointments AS ra ON a.appointment_id = ra.app_id
    JOIN nurses_roles AS nr ON ra.role_id = nr.role_id
    WHERE nr.nurse_id = n_id
    AND a.app_date = s_date
    AND (
        (a.app_hour * 60 + a.app_minutes) < surgery_end
        AND (a.app_hour * 60 + a.app_minutes + a.app_duration) > surgery_start
    );

    RETURN conflicting_surgeries = 0 AND conflicting_appointments = 0;
END;
$$ LANGUAGE plpgsql;


/* Obtains first available room */
CREATE OR REPLACE FUNCTION get_first_available_room(
    s_date DATE
)
RETURNS BIGINT AS $$
DECLARE
    room_number BIGINT := 71;
    available_room BIGINT := NULL;
BEGIN
    WHILE room_number <= 100 LOOP
        IF NOT EXISTS (
            SELECT 1
            FROM hospitalizations
            WHERE room = room_number
            AND s_date BETWEEN start_date AND final_date
        ) THEN
            available_room := room_number;
            EXIT;
        END IF;
        
        room_number := room_number + 1;
    END LOOP;

    RETURN available_room;
END;
$$ LANGUAGE plpgsql;

/* Update bills */
CREATE OR REPLACE PROCEDURE update_bills(
    amount FLOAT,
    p_method INTEGER, 
    id BIGINT, 
    OUT remaining_amount FLOAT
)
LANGUAGE plpgsql AS $$
DECLARE
    total_amount bills.total_payment%TYPE;
    payment_so_far payments.payment%TYPE;
    current_bill_status BOOLEAN;
BEGIN
    -- Verify bill status
    SELECT bill_status INTO current_bill_status
    FROM bills
    WHERE bill_id = id;

    -- if bill is already paid, raise an exception
    IF current_bill_status THEN
        RAISE EXCEPTION 'Cannot make a payment on a paid bill.';
    END IF;

    SELECT total_payment INTO total_amount
    FROM bills
    WHERE bill_id = id;

    -- Insert payment into payments table
    INSERT INTO payments (payment, payment_date, bill_id, method_payment)
    VALUES (amount, CURRENT_DATE, id, p_method);

    -- Calculate total payment so far
    SELECT COALESCE(SUM(payment), 0) INTO payment_so_far
    FROM payments
    WHERE bill_id = id;

    -- Calculate remaining amount
    remaining_amount := total_amount - payment_so_far;

    IF remaining_amount < 0 THEN
        remaining_amount := 0;
    END IF;

    -- If the total payment so far is greater than or equal to the total amount, update the bill status to 'paid'
    IF payment_so_far >= total_amount THEN
        UPDATE bills
        SET bill_status = TRUE
        WHERE bill_id = id;
    END IF;
END;
$$;

/* Trigger to validate an appointment */
CREATE OR REPLACE FUNCTION validate_appointment() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.app_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'A data da consulta deve ser no futuro.';
    END IF;

	IF NEW.app_type NOT IN ('GERAL', 'CARDIOLOGIA', 'DERMATOLOGIA', 'OFTALMOLOGIA', 'PEDIATRIA', 'PSIQUIATRIA', 'REUMATOLOGIA', 'ORTOPEDIA', 'ANESTESIA') THEN
        RAISE EXCEPTION 'Tipo de consulta inválido. Tipos de consultas disponíveis: GERAL, CARDIOLOGIA, DERMATOLOGIA, OFTALMOLOGIA, PEDIATRIA, PSIQUIATRIA, REUMATOLOGIA, ORTOPEDIA, ANESTESIA';
    END IF;

	IF NOT (NEW.app_room >= 0 AND NEW.app_room <= 30) THEN
		RAISE EXCEPTION 'A sala de consultas deve ser entre 0 e 30 inclusive';
	END IF;

    IF NEW.app_hour < 8 OR NEW.app_hour > 20 THEN
        RAISE EXCEPTION 'A hora do compromisso deve ser entre 8 e 20.';
    END IF;
    
    IF NEW.app_minutes < 0 OR NEW.app_minutes > 59 THEN
        RAISE EXCEPTION 'Os minutos do compromisso devem ser entre 0 e 59.';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM patients WHERE person_id = NEW.patient_id) THEN
        RAISE EXCEPTION 'O paciente com o ID % não existe.', NEW.patient_id;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM doctors WHERE person_id = NEW.doctor_id) THEN
        RAISE EXCEPTION 'O médico com o ID % não existe.', NEW.doctor_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_appointment_trigger
BEFORE INSERT OR UPDATE ON appointments
FOR EACH ROW
EXECUTE FUNCTION validate_appointment();

/* Trigger to validate a surgery */
CREATE OR REPLACE FUNCTION validate_surgery() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.surgery_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'A data da cirurgia deve ser no futuro.';
    END IF;

	IF NEW.surgery_type NOT IN ('CARDIOLOGIA', 'DERMATOLOGIA', 'OFTALMOLOGIA', 'REUMATOLOGIA', 'ORTOPEDIA') THEN
        RAISE EXCEPTION 'Tipo de cirurgia inválido. Tipos de cirurgias disponíveis: CARDIOLOGIA, DERMATOLOGIA, OFTALMOLOGIA,  REUMATOLOGIA, ORTOPEDIA';
    END IF;

	IF NOT (NEW.surgery_room >= 31 AND NEW.surgery_room <= 70) THEN
		RAISE EXCEPTION 'A sala de consultas deve ser entre 31 e 70 inclusive';
	END IF;
	
    IF NEW.surgery_hour < 8 OR NEW.surgery_hour > 20 THEN
        RAISE EXCEPTION 'A hora do compromisso deve ser entre 8 e 20.';
    END IF;
    
    IF NEW.surgery_minutes < 0 OR NEW.surgery_minutes > 59 THEN
        RAISE EXCEPTION 'Os minutos do compromisso devem ser entre 0 e 59.';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM patients WHERE person_id = NEW.patient_id) THEN
        RAISE EXCEPTION 'O paciente com o ID % não existe.', NEW.patient_id;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM doctors WHERE person_id = NEW.doctor_id) THEN
        RAISE EXCEPTION 'O médico com o ID % não existe.', NEW.doctor_id;
    END IF;

	IF NOT EXISTS (SELECT 1 FROM hospitalizations WHERE hospitalizations.hosp_id = NEW.hosp_id) THEN
        RAISE EXCEPTION 'A hospitalização com o ID % não existe.', NEW.hosp_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_surgery_trigger
BEFORE INSERT OR UPDATE ON surgeries
FOR EACH ROW
EXECUTE FUNCTION validate_surgery();

/* Trigger to validate a hospitalization */
CREATE OR REPLACE FUNCTION validate_hospitalization() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.start_date >= NEW.final_date THEN
        RAISE EXCEPTION 'A data de início deve ser anterior à data final da hospitalização.';
    END IF;

	IF NOT (NEW.room >= 71 AND NEW.room <= 100) THEN
		RAISE EXCEPTION 'A sala de hospitalizações deve ser entre 71 e 100 inclusive';
	END IF;

    IF NOT EXISTS (SELECT 1 FROM bills WHERE bill_id = NEW.bill_id) THEN
        RAISE EXCEPTION 'O ID da conta especificado não existe na tabela de contas.';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM employees WHERE person_id = NEW.assistant_id) THEN
        RAISE EXCEPTION 'O ID do assistente especificado não existe na tabela de funcionários.';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM employees WHERE person_id = NEW.nurse_id) THEN
        RAISE EXCEPTION 'O ID da enfermeira especificado não existe na tabela de funcionários.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_hospitalization_trigger
BEFORE INSERT ON hospitalizations
FOR EACH ROW
EXECUTE FUNCTION validate_hospitalization();

/* Trigger to create a new bill before hospitalization */
CREATE OR REPLACE FUNCTION create_bill_before_hospitalization()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO bills (total_payment, bill_status)
    VALUES (250, FALSE)
    RETURNING bill_id INTO NEW.bill_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_new_bill
BEFORE INSERT ON hospitalizations
FOR EACH ROW
EXECUTE FUNCTION create_bill_before_hospitalization();

/* Trigger to create a new bill before appointment */
CREATE OR REPLACE FUNCTION create_bill_before_appointment()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO bills (total_payment, bill_status)
    VALUES (50.0, FALSE)
    RETURNING bill_id INTO NEW.bill_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_new_bill
BEFORE INSERT ON appointments
FOR EACH ROW
EXECUTE FUNCTION create_bill_before_appointment();

/* Encrypts "input_text" with key "encrypt_key" */
CREATE OR REPLACE FUNCTION encrypt(input_text VARCHAR, encrypt_key VARCHAR)
RETURNS VARCHAR AS $$
DECLARE 
    data VARCHAR;
BEGIN
    data := pgp_sym_encrypt(input_text, encrypt_key);
    RETURN data;
END;
$$ LANGUAGE plpgsql; 

/* Decrypts "encrypted_text" with key "decrypt_key" */
CREATE OR REPLACE FUNCTION decrypt(encrypted_text VARCHAR, decrypt_key VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    data VARCHAR;
BEGIN
    data := pgp_sym_decrypt(encrypted_text::bytea, decrypt_key);
    RETURN data;
END;
$$
LANGUAGE plpgsql;

/* Trigger to validate an employee */
CREATE OR REPLACE FUNCTION validate_employee_data()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.final_date IS NOT NULL AND NEW.final_date < NEW.start_date THEN
        RAISE EXCEPTION 'Final date cannot be before start date';
    END IF;

    IF NEW.salary < 0 THEN
        RAISE EXCEPTION 'Salary must be a positive number';
    END IF;

    IF length(NEW.person_cc) <> 8 THEN
        RAISE EXCEPTION 'Person CC must be 8 digits';
    END IF;
    
    IF length(NEW.person_phone) <> 9 THEN
        RAISE EXCEPTION 'Person phone must be 9 digits';
    END IF;

    IF length(NEW.person_name) > 20 THEN
        RAISE EXCEPTION 'Person name must be at most 20 characters';
    END IF;
    
    IF length(NEW.person_address) > 50 THEN
        RAISE EXCEPTION 'Person address must be at most 50 characters';
    END IF;
    
    IF length(NEW.person_username) > 15 THEN
        RAISE EXCEPTION 'Person username must be at most 15 characters';
    END IF;
    
    IF length(NEW.person_password) > 512 THEN
        RAISE EXCEPTION 'Person password must be at most 512 characters';
    END IF;

    IF NEW.person_email IS NOT NULL AND length(NEW.person_email) > 30 THEN
        RAISE EXCEPTION 'Person email must be at most 30 characters';
    END IF;

    IF NEW.person_type < 1 OR NEW.person_type > 4 THEN
        RAISE EXCEPTION 'Person type must be between 1 and 4';
    END IF;

    IF EXISTS (SELECT 1 FROM employees WHERE person_cc = NEW.person_cc AND person_id <> NEW.person_id) THEN
        RAISE EXCEPTION 'Person CC must be unique';
    END IF;
    
    IF EXISTS (SELECT 1 FROM employees WHERE person_phone = NEW.person_phone AND person_id <> NEW.person_id) THEN
        RAISE EXCEPTION 'Person phone must be unique';
    END IF;
    
    IF EXISTS (SELECT 1 FROM employees WHERE person_username = NEW.person_username AND person_id <> NEW.person_id) THEN
        RAISE EXCEPTION 'Person username must be unique';
    END IF;
    
    IF NEW.person_email IS NOT NULL AND EXISTS (SELECT 1 FROM employees WHERE person_email = NEW.person_email AND person_id <> NEW.person_id) THEN
        RAISE EXCEPTION 'Person email must be unique';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_employee
BEFORE INSERT OR UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION validate_employee_data();

/* Trigger to validate a patient */
CREATE OR REPLACE FUNCTION validate_patient_data()
RETURNS TRIGGER AS $$
BEGIN
    IF length(NEW.person_cc) <> 8 THEN
        RAISE EXCEPTION 'Person CC must be 8 digits';
    END IF;
    
    IF length(NEW.person_phone) <> 9 THEN
        RAISE EXCEPTION 'Person phone must be 9 digits';
    END IF;

    IF length(NEW.person_name) > 20 THEN
        RAISE EXCEPTION 'Person name must be at most 20 characters';
    END IF;
    
    IF length(NEW.person_address) > 50 THEN
        RAISE EXCEPTION 'Person address must be at most 50 characters';
    END IF;
    
    IF length(NEW.person_username) > 15 THEN
        RAISE EXCEPTION 'Person username must be at most 15 characters';
    END IF;
    
    IF length(NEW.person_password) > 512 THEN
        RAISE EXCEPTION 'Person password must be at most 512 characters';
    END IF;

    IF NEW.person_email IS NOT NULL AND length(NEW.person_email) > 30 THEN
        RAISE EXCEPTION 'Person email must be at most 30 characters';
    END IF;

    IF NEW.person_type > 1 THEN
        RAISE EXCEPTION 'Person type must be between 1';
    END IF;

    IF EXISTS (SELECT 1 FROM patients WHERE person_cc = NEW.person_cc AND person_id <> NEW.person_id) THEN
        RAISE EXCEPTION 'Person CC must be unique';
    END IF;
    
    IF EXISTS (SELECT 1 FROM patients WHERE person_phone = NEW.person_phone AND  person_id <> NEW.person_id) THEN
        RAISE EXCEPTION 'Person phone must be unique';
    END IF;
    
    IF EXISTS (SELECT 1 FROM patients WHERE person_username = NEW.person_username AND person_id <> NEW.person_id) THEN
        RAISE EXCEPTION 'Person username must be unique';
    END IF;
    
    IF NEW.person_email IS NOT NULL AND EXISTS (SELECT 1 FROM patients WHERE person_email = NEW.person_email AND person_id <> NEW.person_id) THEN
        RAISE EXCEPTION 'Person email must be unique';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER validate_patient
BEFORE INSERT OR UPDATE ON patients
FOR EACH ROW
EXECUTE FUNCTION validate_patient_data();

/* Trigger to validate a medical license */
CREATE OR REPLACE FUNCTION validate_medical_license_data()
RETURNS TRIGGER AS $$
BEGIN
	-- Validate start_date format
    IF NEW.ml_issue_date::TEXT !~ '^\d{4}-\d{2}-\d{2}$' THEN
        RAISE EXCEPTION 'Issue date must be in the format YYYY-MM-DD';
    END IF;
    
    -- Validate final_date format
    IF NEW.ml_expiration_date IS NOT NULL AND NEW.ml_expiration_date::TEXT !~ '^\d{4}-\d{2}-\d{2}$' THEN
        RAISE EXCEPTION 'Expiration date must be in the format YYYY-MM-DD';
    END IF;

    -- Validate final_date
    IF NEW.ml_expiration_date IS NOT NULL AND NEW.ml_expiration_date <= NEW.ml_issue_date THEN
        RAISE EXCEPTION 'Expiration date must be after the issue date';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER medical_license
BEFORE INSERT OR UPDATE ON doctors
FOR EACH ROW
EXECUTE FUNCTION validate_medical_license_data();