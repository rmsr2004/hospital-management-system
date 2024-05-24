/*
	TRIGGERS, FUNCTIONS AND PROCEDURES
*/

/* Verificar se o médico está disponível para uma consulta */
CREATE OR REPLACE FUNCTION is_doctor_available_for_appointment(d_id INTEGER, a_date DATE, app_hour INTEGER, app_minutes INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    appointment_start INTEGER := app_hour * 60 + app_minutes;
    appointment_end INTEGER := appointment_start + 30;
BEGIN
    -- Verificar conflitos com cirurgias
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries s
    WHERE s.doctor_id = d_id
      AND s.surgery_date = a_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < appointment_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + 120) > appointment_start
      );

    -- Verificar conflitos com consultas
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments a
    WHERE a.doctor_id = d_id
      AND a.app_date = a_date
      AND (
          (a.app_hour * 60 + a.app_minutes) < appointment_end
          AND (a.app_hour * 60 + a.app_minutes + a.app_duration) > appointment_start
      );

    RETURN conflicting_surgeries = 0 AND conflicting_appointments = 0;
END;
$$ LANGUAGE plpgsql;

/* Verificar se a sala está disponível para uma cirurgia */
CREATE OR REPLACE FUNCTION is_room_available_for_surgery(s_room BIGINT, s_date DATE, surgery_hour INTEGER, surgery_minutes INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    surgery_start INTEGER := surgery_hour * 60 + surgery_minutes;
    surgery_end INTEGER := surgery_start + 120; -- duração fixa de 2 horas (120 minutos)
BEGIN
    -- Verificar conflitos com cirurgias
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries s
    WHERE s.surgery_room = s_room
      AND s.surgery_date = s_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < surgery_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + 120) > surgery_start
      );

    -- Verificar conflitos com consultas
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

/* Verificar se o médico está disponível para uma cirurgia */
CREATE OR REPLACE FUNCTION is_doctor_available_for_surgery(d_id INTEGER, s_date DATE, surgery_hour INTEGER, surgery_minutes INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    surgery_start INTEGER := surgery_hour * 60 + surgery_minutes;
    surgery_end INTEGER := surgery_start + 120; -- duração fixa de 2 horas (120 minutos)
BEGIN
    -- Verificar conflitos com cirurgias
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries s
    WHERE s.doctor_id = d_id
      AND s.surgery_date = s_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < surgery_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + 120) > surgery_start
      );

    -- Verificar conflitos com consultas
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

/* Verificar se a sala está disponível para uma consulta */
CREATE OR REPLACE FUNCTION is_room_available_for_appointment(a_room BIGINT, a_date DATE, app_hour INTEGER, app_minutes INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    conflicting_surgeries INTEGER;
    conflicting_appointments INTEGER;
    appointment_start INTEGER := app_hour * 60 + app_minutes;
    appointment_end INTEGER := appointment_start + 30;
BEGIN
    -- Verificar conflitos com cirurgias
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries s
    WHERE s.surgery_room = a_room
      AND s.surgery_date = a_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < appointment_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + 120) > appointment_start
      );

    -- Verificar conflitos com consultas
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments a
    WHERE a.app_room = a_room
      AND a.app_date = a_date
      AND (
          (a.app_hour * 60 + a.app_minutes) < appointment_end
          AND (a.app_hour * 60 + a.app_minutes + a.app_duration) > appointment_start
      );

    RETURN conflicting_surgeries = 0 AND conflicting_appointments = 0;
END;
$$ LANGUAGE plpgsql;


/* Verificar se a enfermeira está disponível para uma consulta */
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
    -- Verificar conflitos com cirurgias
    SELECT COUNT(*)
    INTO conflicting_surgeries
    FROM surgeries s
    JOIN roles_surgeries rs ON s.surgery_id = rs.surgery_id
    JOIN nurses_roles nr ON rs.role_id = nr.role_id
    WHERE nr.nurse_id = n_id
      AND s.surgery_date = a_date
      AND (
          (s.surgery_hour * 60 + s.surgery_minutes) < appointment_end
          AND (s.surgery_hour * 60 + s.surgery_minutes + s.surgery_duration) > appointment_start
      );

    -- Verificar conflitos com consultas
    SELECT COUNT(*)
    INTO conflicting_appointments
    FROM appointments a
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


/* Verificar se a enfermeira está disponível para uma cirurgia */
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
    -- Verificar conflitos com outras cirurgias
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

    -- Verificar conflitos com consultas
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

/* Função para obter a primeira sala disponível */
CREATE OR REPLACE FUNCTION get_first_available_room(s_date DATE)
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

CREATE OR REPLACE PROCEDURE update_bills(amount FLOAT, p_method INTEGER, id BIGINT, OUT remaining_amount FLOAT)
LANGUAGE plpgsql AS $$
DECLARE
    total_amount bills.total_payment%TYPE;
    payment_so_far payments.payment%TYPE;
    current_bill_status BOOLEAN;
BEGIN
    -- Verifique o status da fatura
    SELECT bill_status INTO current_bill_status
    FROM bills
    WHERE bill_id = id;

    -- Se a fatura já estiver paga, interrompa o procedimento
    IF current_bill_status THEN
        RAISE EXCEPTION 'Cannot make a payment on a paid bill.';
    END IF;

    -- Determine o total_payment da fatura
    SELECT total_payment INTO total_amount
    FROM bills
    WHERE bill_id = id;

    -- Calcule o total já pago para o bill_id especificado
    SELECT COALESCE(SUM(payment), 0) INTO payment_so_far
    FROM payments
    WHERE bill_id = id;

    -- Calcule o valor restante
    remaining_amount := total_amount - payment_so_far;

    -- Insira um novo pagamento na tabela payments
    INSERT INTO payments (payment, payment_date, bill_id, payment_method)
    VALUES (amount, CURRENT_DATE, id, p_method);

    -- Calcule o novo pagamento total
    payment_so_far := payment_so_far + amount;

    -- Se o pagamento total até agora for maior ou igual ao total da fatura
    IF payment_so_far >= total_amount THEN
        -- Atualize o status da fatura para 'paga'
        UPDATE bills
        SET bill_status = TRUE
        WHERE bill_id = id;
    END IF;
END;
$$;


/* Trigger para validar uma consulta */
CREATE OR REPLACE FUNCTION validate_appointment() RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se a data é no futuro
    IF NEW.app_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'A data da consulta deve ser no futuro.';
    END IF;

	-- Verifica se o tipo de consulta é válido
	IF NEW.app_type NOT IN ('GERAL', 'CARDIOLOGIA', 'DERMATOLOGIA', 'OFTALMOLOGIA', 'PEDIATRIA', 'PSIQUIATRIA', 'REUMATOLOGIA', 'ORTOPEDIA', 'ANESTESIA') THEN
        RAISE EXCEPTION 'Tipo de consulta inválido. Tipos de consultas disponíveis: GERAL, CARDIOLOGIA, DERMATOLOGIA, OFTALMOLOGIA, PEDIATRIA, PSIQUIATRIA, REUMATOLOGIA, ORTOPEDIA, ANESTESIA';
    END IF;

	-- Verifica se a sala é válida
	IF NOT (NEW.app_room >= 0 AND NEW.app_room <= 30) THEN
		RAISE EXCEPTION 'A sala de consultas deve ser entre 0 e 30 inclusive';
	END IF;
	
    -- Verifica se a hora é válida (0-23)
    IF NEW.app_hour < 0 OR NEW.app_hour > 23 THEN
        RAISE EXCEPTION 'A hora do compromisso deve ser entre 0 e 23.';
    END IF;
    
    -- Verifica se os minutos são válidos (0-59)
    IF NEW.app_minutes < 0 OR NEW.app_minutes > 59 THEN
        RAISE EXCEPTION 'Os minutos do compromisso devem ser entre 0 e 59.';
    END IF;
    
    -- Verifica se o paciente existe
    IF NOT EXISTS (SELECT 1 FROM patients WHERE person_id = NEW.patient_id) THEN
        RAISE EXCEPTION 'O paciente com o ID % não existe.', NEW.patient_id;
    END IF;
    
    -- Verifica se o médico existe
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

/* Trigger para validar uma cirurgia */
CREATE OR REPLACE FUNCTION validate_surgery() RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se a data é no futuro
    IF NEW.surgery_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'A data da consulta deve ser no futuro.';
    END IF;

	-- Verifica se o tipo de consulta é válido
	IF NEW.surgery_type NOT IN ('CARDIOLOGIA', 'DERMATOLOGIA', 'OFTALMOLOGIA', 'REUMATOLOGIA', 'ORTOPEDIA') THEN
        RAISE EXCEPTION 'Tipo de consulta inválido. Tipos de consultas disponíveis: CARDIOLOGIA, DERMATOLOGIA, OFTALMOLOGIA,  REUMATOLOGIA, ORTOPEDIA';
    END IF;

	-- Verifica se a sala é válida
	IF NOT (NEW.surgery_room >= 31 AND NEW.surgery_room <= 70) THEN
		RAISE EXCEPTION 'A sala de consultas deve ser entre 31 e 70 inclusive';
	END IF;
	
    -- Verifica se a hora é válida (0-23)
    IF NEW.surgery_hour < 0 OR NEW.surgery_hour > 23 THEN
        RAISE EXCEPTION 'A hora do compromisso deve ser entre 0 e 23.';
    END IF;
    
    -- Verifica se os minutos são válidos (0-59)
    IF NEW.surgery_minutes < 0 OR NEW.surgery_minutes > 59 THEN
        RAISE EXCEPTION 'Os minutos do compromisso devem ser entre 0 e 59.';
    END IF;
    
    -- Verifica se o paciente existe
    IF NOT EXISTS (SELECT 1 FROM patients WHERE person_id = NEW.patient_id) THEN
        RAISE EXCEPTION 'O paciente com o ID % não existe.', NEW.patient_id;
    END IF;
    
    -- Verifica se o médico existe
    IF NOT EXISTS (SELECT 1 FROM doctors WHERE person_id = NEW.doctor_id) THEN
        RAISE EXCEPTION 'O médico com o ID % não existe.', NEW.doctor_id;
    END IF;

	-- Verifica se a hospitalização existe
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

/* Trigger para validar uma hospitalização */
CREATE OR REPLACE FUNCTION validate_hospitalization() RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se a data de início é anterior à data final
    IF NEW.start_date >= NEW.final_date THEN
        RAISE EXCEPTION 'A data de início deve ser anterior à data final da hospitalização.';
    END IF;

	-- Verifica se a sala é válida
	IF NOT (NEW.room >= 71 AND NEW.room <= 100) THEN
		RAISE EXCEPTION 'A sala de consultas deve ser entre 71 e 100 inclusive';
	END IF;

    -- Verificar se o ID da conta existe na tabela de contas
    IF NOT EXISTS (SELECT 1 FROM bills WHERE bill_id = NEW.bill_id) THEN
        RAISE EXCEPTION 'O ID da conta especificado não existe na tabela de contas.';
    END IF;

    -- Verificar se o ID do assistente existe na tabela de funcionários
    IF NOT EXISTS (SELECT 1 FROM employees WHERE person_id = NEW.assistant_id) THEN
        RAISE EXCEPTION 'O ID do assistente especificado não existe na tabela de funcionários.';
    END IF;

    -- Verificar se o ID da enfermeira existe na tabela de funcionários
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

/* Trigger para criar uma nova fatura antes de uma hospitalização */
CREATE OR REPLACE FUNCTION create_bill_before_hospitalization()
RETURNS TRIGGER AS $$
BEGIN
    -- Insere uma nova linha na tabela bills
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

/* Trigger para criar uma nova fatura antes de uma consulta */
CREATE OR REPLACE FUNCTION create_bill_before_appointment()
RETURNS TRIGGER AS $$
BEGIN
    -- Insere uma nova fatura na tabela bills
    INSERT INTO bills (total_payment, bill_status)
    VALUES (50.0, FALSE)
    RETURNING bill_id INTO NEW.bill_id;  -- Retorna o ID da fatura para a nova appointment
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_new_bill
BEFORE INSERT ON appointments
FOR EACH ROW
EXECUTE FUNCTION create_bill_before_appointment();


CREATE EXTENSION IF NOT EXISTS pgcrypto;


CREATE OR REPLACE FUNCTION encrypt(input_text VARCHAR, encrypt_key VARCHAR)
RETURNS VARCHAR AS $$
DECLARE 
    data VARCHAR;
BEGIN
 data := pgp_sym_encrypt(input_text, encrypt_key);
 RETURN data;
END;
$$
LANGUAGE plpgsql; 

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

CREATE OR REPLACE FUNCTION add_appointment_prescriptions(patient_id INTEGER, doctor_id INTEGER, presc_id INTEGER)
RETURNS VARCHAR AS $$
DECLARE
    app_id INT;
BEGIN
    -- Verifica se o agendamento (appointment) existe para o paciente (_patient_id) e o médico (_doctor_id)
    SELECT appointment_id INTO app_id 
    FROM appointments 
    WHERE patient_id = patient_id AND doctor_id = doctor_id;
    
    IF NOT FOUND THEN
        RETURN 'Appointment does not exist for the given patient and doctor';
    END IF;

    -- Insere na tabela appointments_prescriptions
    INSERT INTO appointments_prescriptions (app_id, patient_id, doctor_id, presc_id)
    VALUES (app_id, patient_id, doctor_id, presc_id);
    
    RETURN 'Prescription added successfully!';
END;
$$ LANGUAGE plpgsql;
