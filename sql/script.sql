CREATE DATABASE hospital_db;
CREATE USER hosp_user WITH PASSWORD 'hospninja';
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospninja;


DO $$DECLARE
    tabname RECORD;
BEGIN
    FOR tabname IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || tabname.tablename || ' CASCADE';
    END LOOP;
END$$;


DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS nurses;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS assistants;
DROP TABLE IF EXISTS contract_types;
DROP TABLE IF EXISTS specialisations;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS medicines;
DROP TABLE IF EXISTS side_effects;
DROP TABLE IF EXISTS surgeries;
DROP TABLE IF EXISTS hospitalizations;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS sub_specialisations;
DROP TABLE IF EXISTS nurse_categories;
DROP TABLE IF EXISTS probabilities;
DROP TABLE IF EXISTS roles_appointments;
DROP TABLE IF EXISTS roles_surgeries;
DROP TABLE IF EXISTS nurses_roles;
DROP TABLE IF EXISTS hospitalizations_prescriptions;
DROP TABLE IF EXISTS side_effects_medicines;
DROP TABLE IF EXISTS prescriptions_medicines;
DROP TABLE IF EXISTS appointments_prescriptions;
DROP TABLE IF EXISTS specialisations_doctors;

CREATE TABLE employees (
	salary	 			FLOAT(8) NOT NULL,
	start_date	 		DATE NOT NULL,
	final_date	 		DATE,
	ctype_id 			BIGINT NOT NULL,
	person_id		 	SERIAL,
	person_cc		 	BIGINT NOT NULL,
	person_name		 	VARCHAR(20) NOT NULL,
	person_address	 	VARCHAR(50) NOT NULL,
	person_phone		VARCHAR(9) NOT NULL,
	person_username		VARCHAR(15) NOT NULL,
	person_password	 	VARCHAR(512) NOT NULL,
	person_email		VARCHAR(30),
	person_type		 	INTEGER NOT NULL,
	PRIMARY KEY(person_id)
);

CREATE TABLE patients (
	person_id	 		SERIAL,
	person_cc	 		BIGINT NOT NULL,
	person_name	 		VARCHAR(20) NOT NULL,
	person_address	 	VARCHAR(50) NOT NULL,
	person_phone	 	VARCHAR(9) NOT NULL,
	person_username 	VARCHAR(15) NOT NULL,
	person_password		VARCHAR(512) NOT NULL,
	person_email	 	VARCHAR(30),
	person_type	 		INTEGER NOT NULL,
	PRIMARY KEY(person_id)
);

CREATE TABLE nurses (
	person_id 		INTEGER,
	PRIMARY KEY(person_id)
);

CREATE TABLE doctors (
	ml_id		 			BIGSERIAL NOT NULL,
	ml_issue_date	 		DATE NOT NULL,
	ml_expiration_date		DATE NOT NULL,
	person_id	 			INTEGER,
	PRIMARY KEY(person_id)
);

CREATE TABLE assistants (
	person_id		INTEGER,
	PRIMARY KEY(person_id)
);

CREATE TABLE contract_types (
	ctype_id		BIGSERIAL,
	ctype	 		VARCHAR(20) NOT NULL,
	PRIMARY KEY(ctype_id)
);

CREATE TABLE specialisations (
	spec_id	 			BIGSERIAL,
	specialization		VARCHAR(20) NOT NULL,
	PRIMARY KEY(spec_id)
);

CREATE TABLE appointments (
	appointment_id		BIGSERIAL,
	app_date			DATE NOT NULL,
	app_status			INTEGER NOT NULL,
	app_type			VARCHAR(20) NOT NULL,
	app_room			BIGINT NOT NULL,
	app_hour			INTEGER NOT NULL,
	app_minutes			INTEGER NOT NULL,
	app_duration		BIGINT NOT NULL,
	patient_id			INTEGER,
	doctor_id 			INTEGER,
	bill_id				BIGINT NOT NULL,
	PRIMARY KEY(appointment_id,patient_id,doctor_id)
);

CREATE TABLE prescriptions (
	presc_id 	BIGSERIAL,
	PRIMARY KEY(presc_id)
);

CREATE TABLE medicines (
	medication_id		BIGSERIAL,
	medication	 		VARCHAR(20) NOT NULL,
	dosage	 			FLOAT(8) NOT NULL,
	PRIMARY KEY(medication_id)
);

CREATE TABLE side_effects (
	side_effect_id		BIGSERIAL,
	side_effect		 	VARCHAR(20) NOT NULL,
	prob_id 			BIGINT NOT NULL,
	PRIMARY KEY(side_effect_id)
);

CREATE TABLE surgeries (
	surgery_id				BIGSERIAL,
	surgery_date			DATE NOT NULL,
	surgery_status			INTEGER NOT NULL,
	surgery_type			VARCHAR(20) NOT NULL,
	surgery_room			BIGINT NOT NULL,
	surgery_hour			INTEGER NOT NULL,
	surgery_minutes			INTEGER NOT NULL,
	surgery_duration		BIGINT NOT NULL,
	doctor_id 				INTEGER,
	patient_id				INTEGER NOT NULL,
	hosp_id				 	BIGINT NOT NULL,
	PRIMARY KEY(surgery_id,doctor_id)
);

CREATE TABLE hospitalizations (
	hosp_id				BIGSERIAL,
	start_date			DATE NOT NULL,
	final_date			DATE NOT NULL,
	room				BIGINT NOT NULL,
	bill_id				BIGINT NOT NULL,
	assistant_id		INTEGER NOT NULL,
	nurse_id	 		INTEGER NOT NULL,
	PRIMARY KEY(hosp_id)
);

CREATE TABLE payments (
	payment_id	 		BIGSERIAL,
	payment	 			FLOAT(8) NOT NULL,
    method_payment      INTEGER NOT NULL,
	payment_date		DATE NOT NULL,
	bill_id 			BIGINT,
	PRIMARY KEY(payment_id,bill_id)
);

CREATE TABLE bills (
	bill_id	 			BIGSERIAL,
	total_payment	 	FLOAT(8) NOT NULL,
	bill_status		 	BOOL NOT NULL DEFAULT FALSE,
	PRIMARY KEY(bill_id)
);

CREATE TABLE roles (
	role_id		BIGSERIAL,
	role	 	VARCHAR(20) NOT NULL,
	role_type	INTEGER,
	PRIMARY KEY(role_id)
);

CREATE TABLE sub_specialisations (
	sub_spec_id		BIGSERIAL,
	sub_spec		VARCHAR(20) NOT NULL,
	spec_id 		BIGINT NOT NULL,
	PRIMARY KEY(sub_spec_id)
);

CREATE TABLE nurse_categories (
	category_id		BIGSERIAL,
	category	 	VARCHAR(20) NOT NULL,
	PRIMARY KEY(category_id)
);

CREATE TABLE nurses_categories (
	nurse_id        INTEGER,
	category_id     BIGINT,
	PRIMARY KEY(nurse_id,category_id)
);

CREATE TABLE probabilities (
	prob_id		BIGSERIAL,
	prob	 	FLOAT(8) NOT NULL,
	PRIMARY KEY(prob_id)
);

CREATE TABLE roles_appointments (
	role_id			BIGINT,
	app_id			BIGINT,
	patient_id		INTEGER,
	doctor_id 		INTEGER,
	PRIMARY KEY(role_id,app_id,patient_id,doctor_id)
);

CREATE TABLE roles_surgeries (
	role_id			BIGINT,
	surgery_id		BIGINT,
	doctor_id 		INTEGER,
	PRIMARY KEY(role_id,surgery_id,doctor_id)		
);

CREATE TABLE nurses_roles (
	nurse_id		INTEGER,
	role_id			BIGINT NOT NULL,
	PRIMARY KEY(nurse_id)
);

CREATE TABLE hospitalizations_prescriptions (
	hosp_id 		BIGINT,
	presc_id		BIGINT NOT NULL,
	PRIMARY KEY(hosp_id)
);

CREATE TABLE side_effects_medicines (
	side_effect_id		BIGINT,
	medication_id	 	BIGINT,
	PRIMARY KEY(side_effect_id,medication_id)
);

CREATE TABLE prescriptions_medicines (
	presc_id	 		BIGINT,
	medication_id		BIGINT,
	PRIMARY KEY(presc_id,medication_id)
);

CREATE TABLE appointments_prescriptions (
	app_id			BIGINT,
	patient_id		INTEGER,
	doctor_id 		INTEGER,
	presc_id		BIGINT NOT NULL,
	PRIMARY KEY(app_id,patient_id,doctor_id)
);

CREATE TABLE specialisations_doctors (
	spec_id			BIGINT,
	doctor_id		INTEGER,
	PRIMARY KEY(doctor_id)
);

CREATE TABLE sub_specialisations_doctors (
	doctor_id       INTEGER,
	sub_spec_id		BIGINT,
	PRIMARY KEY(doctor_id,sub_spec_id)
);

ALTER TABLE employees ADD UNIQUE (person_cc, person_phone, person_username, person_password, person_email);
ALTER TABLE employees ADD CONSTRAINT employees_fk1 FOREIGN KEY (ctype_id) REFERENCES contract_types(ctype_id);
ALTER TABLE employees ADD CONSTRAINT constraint_0 CHECK (person_type >= 1 AND person_type <=4);
ALTER TABLE patients ADD UNIQUE (person_cc, person_phone, person_username, person_password, person_email);
ALTER TABLE patients ADD CONSTRAINT constraint_0 CHECK (person_type >= 1 AND person_type <=4);
ALTER TABLE nurses ADD CONSTRAINT nurses_fk2 FOREIGN KEY (person_id) REFERENCES employees(person_id);
ALTER TABLE doctors ADD UNIQUE (ml_id);
ALTER TABLE doctors ADD CONSTRAINT doctors_fk1 FOREIGN KEY (person_id) REFERENCES employees(person_id);
ALTER TABLE assistants ADD CONSTRAINT assistants_fk1 FOREIGN KEY (person_id) REFERENCES employees(person_id);
ALTER TABLE appointments ADD CONSTRAINT appointments_fk1 FOREIGN KEY (patient_id) REFERENCES patients(person_id);
ALTER TABLE appointments ADD CONSTRAINT appointments_fk2 FOREIGN KEY (doctor_id) REFERENCES doctors(person_id);
ALTER TABLE appointments ADD CONSTRAINT appointments_fk4 FOREIGN KEY (bill_id) REFERENCES bills(bill_id);
ALTER TABLE appointments ADD CONSTRAINT constraint_0 CHECK (app_status >= 0 AND app_status <=1);
ALTER TABLE appointments ADD CONSTRAINT constraint_1 CHECK (app_hour >= 0 AND app_hour <= 23);
ALTER TABLE appointments ADD CONSTRAINT constraint_2 CHECK (app_minutes >= 0 AND app_minutes <= 59);
ALTER TABLE medicines ADD UNIQUE (medication);
ALTER TABLE side_effects ADD UNIQUE (side_effect);
ALTER TABLE side_effects ADD CONSTRAINT side_effects_fk1 FOREIGN KEY (prob_id) REFERENCES probabilities(prob_id);
ALTER TABLE surgeries ADD CONSTRAINT surgeries_fk1 FOREIGN KEY (doctor_id) REFERENCES doctors(person_id);
ALTER TABLE surgeries ADD CONSTRAINT surgeries_fk2 FOREIGN KEY (patient_id) REFERENCES patients(person_id);
ALTER TABLE surgeries ADD CONSTRAINT surgeries_fk3 FOREIGN KEY (hosp_id) REFERENCES hospitalizations(hosp_id);
ALTER TABLE surgeries ADD CONSTRAINT constraint_0 CHECK (surgery_status >= 0 AND surgery_status <=1);
ALTER TABLE surgeries ADD CONSTRAINT constraint_1 CHECK (surgery_hour >= 0 AND surgery_hour <= 23);
ALTER TABLE surgeries ADD CONSTRAINT constraint_2 CHECK (surgery_minutes >= 0 AND surgery_minutes <= 59);
ALTER TABLE hospitalizations ADD UNIQUE (bill_id, nurse_id);
ALTER TABLE hospitalizations ADD CONSTRAINT hospitalizations_fk1 FOREIGN KEY (bill_id) REFERENCES bills(bill_id);
ALTER TABLE hospitalizations ADD CONSTRAINT hospitalizations_fk2 FOREIGN KEY (assistant_id) REFERENCES assistants(person_id);
ALTER TABLE hospitalizations ADD CONSTRAINT hospitalizations_fk3 FOREIGN KEY (nurse_id) REFERENCES nurses(person_id);
ALTER TABLE payments ADD CONSTRAINT payments_fk1 FOREIGN KEY (bill_id) REFERENCES bills(bill_id);
ALTER TABLE payments ADD CONSTRAINT constraint_0 CHECK (method_payment >= 0 AND method_payment <=2);
ALTER TABLE sub_specialisations ADD CONSTRAINT sub_specialisations_fk1 FOREIGN KEY (spec_id) REFERENCES specialisations(spec_id);
ALTER TABLE sub_specialisations_doctors ADD CONSTRAINT doctors_specialisations_fk1 FOREIGN KEY (doctor_id) REFERENCES doctors(person_id);
ALTER TABLE sub_specialisations_doctors ADD CONSTRAINT sub_specialisations_doctors_fk2 FOREIGN KEY (sub_spec_id) REFERENCES sub_specialisations(sub_spec_id);
ALTER TABLE roles_appointments ADD CONSTRAINT roles_appointments_fk1 FOREIGN KEY (role_id) REFERENCES roles(role_id);
ALTER TABLE roles_appointments ADD CONSTRAINT roles_appointments_fk2 FOREIGN KEY (app_id, patient_id, doctor_id) REFERENCES appointments(appointment_id, patient_id, doctor_id);
ALTER TABLE roles_surgeries ADD CONSTRAINT roles_surgeries_fk1 FOREIGN KEY (role_id) REFERENCES roles(role_id);
ALTER TABLE roles_surgeries ADD CONSTRAINT roles_surgeries_fk2 FOREIGN KEY (surgery_id, doctor_id) REFERENCES surgeries(surgery_id, doctor_id);
ALTER TABLE nurses_roles ADD CONSTRAINT nurses_roles_fk1 FOREIGN KEY (nurse_id) REFERENCES nurses(person_id);
ALTER TABLE nurses_roles ADD CONSTRAINT nurses_roles_fk2 FOREIGN KEY (role_id) REFERENCES roles(role_id);
ALTER TABLE hospitalizations_prescriptions ADD UNIQUE (presc_id);
ALTER TABLE hospitalizations_prescriptions ADD CONSTRAINT hospitalizations_prescriptions_fk1 FOREIGN KEY (hosp_id) REFERENCES hospitalizations(hosp_id);
ALTER TABLE hospitalizations_prescriptions ADD CONSTRAINT hospitalizations_prescriptions_fk2 FOREIGN KEY (presc_id) REFERENCES prescriptions(presc_id);
ALTER TABLE side_effects_medicines ADD CONSTRAINT side_effects_medicines_fk1 FOREIGN KEY (side_effect_id) REFERENCES side_effects(side_effect_id);
ALTER TABLE side_effects_medicines ADD CONSTRAINT side_effects_medicines_fk2 FOREIGN KEY (medication_id) REFERENCES medicines(medication_id);
ALTER TABLE prescriptions_medicines ADD CONSTRAINT prescriptions_medicines_fk1 FOREIGN KEY (presc_id) REFERENCES prescriptions(presc_id);
ALTER TABLE prescriptions_medicines ADD CONSTRAINT prescriptions_medicines_fk2 FOREIGN KEY (medication_id) REFERENCES medicines(medication_id);
ALTER TABLE appointments_prescriptions ADD UNIQUE (presc_id);
ALTER TABLE appointments_prescriptions ADD CONSTRAINT appointments_prescriptions_fk1 FOREIGN KEY (app_id, patient_id, doctor_id) REFERENCES appointments(appointment_id, patient_id, doctor_id);
ALTER TABLE appointments_prescriptions ADD CONSTRAINT appointments_prescriptions_fk2 FOREIGN KEY (presc_id) REFERENCES prescriptions(presc_id);
ALTER TABLE specialisations_doctors ADD CONSTRAINT specialisations_doctors_fk1 FOREIGN KEY (spec_id) REFERENCES specialisations(spec_id);
ALTER TABLE specialisations_doctors ADD CONSTRAINT specialisations_doctors_fk2 FOREIGN KEY (doctor_id) REFERENCES doctors(person_id);
ALTER TABLE nurses_categories ADD CONSTRAINT nurses_categories_fk1 FOREIGN KEY (nurse_id) REFERENCES nurses(person_id);
ALTER TABLE nurses_categories ADD CONSTRAINT nurses_categories_fk2 FOREIGN KEY (category_id) REFERENCES nurse_categories(category_id);
ALTER TABLE appointments ADD CONSTRAINT check_app_room CHECK (app_room >= 0 AND app_room <= 30);
ALTER TABLE surgeries ADD CONSTRAINT check_surg_room CHECK (surgery_room >= 31 AND surgery_room <= 70);
ALTER TABLE hospitalizations ADD CONSTRAINT check_hosp_room CHECK (room >= 71 AND room <= 100);
ALTER TABLE roles ADD CONSTRAINT chk_role_type_0 CHECK (
    (role_type = 0 AND role IN ('TRIAGEM', 'PREPARACAO', 'SUPORTE')) OR
    (role_type = 1 AND role IN ('ASSISTENTE', 'MONITOR', 'ANESTESISTA'))
);

ALTER TABLE appointments ADD CONSTRAINT check_type CHECK (
	app_type IN ('GERAL', 'CARDIOLOGIA', 'DERMATOLOGIA', 'OFTALMOLOGIA', 'PEDIATRIA', 'PSIQUIATRIA', 'REUMATOLOGIA', 'ORTOPEDIA', 'ANESTESIA')
);

ALTER TABLE surgeries ADD CONSTRAINT check_type CHECK (
	surgery_type IN ('CARDIOLOGIA', 'DERMATOLOGIA', 'OFTALMOLOGIA', 'REUMATOLOGIA', 'ORTOPEDIA')
);


/*
	Tipos de Contratos
*/
	
INSERT INTO contract_types (ctype) VALUES ('EFETIVO');
INSERT INTO contract_types (ctype) VALUES ('PART-TIME');
INSERT INTO contract_types (ctype) VALUES ('TEMPORARIO');

/*
	Funções das Enfermeiras - Cirurgias
*/
INSERT INTO roles (role, role_type) VALUES ('ASSISTENTE', 1);
INSERT INTO roles (role, role_type) VALUES ('MONITOR', 1);
INSERT INTO roles (role, role_type) VALUES ('ANESTESISTA', 1);
/*
	Funções das Enfermeiras- Consultas
*/
INSERT INTO roles (role, role_type) VALUES ('TRIAGEM', 0);
INSERT INTO roles (role, role_type) VALUES ('PREPARACAO', 0);
INSERT INTO roles (role, role_type) VALUES ('SUPORTE', 0);

/*
	Especializações dos Médicos
*/
INSERT INTO specialisations (specialization) VALUES ('CARDIOLOGIA');
INSERT INTO specialisations (specialization) VALUES ('DERMATOLOGIA');
INSERT INTO specialisations (specialization) VALUES ('OFTALMOLOGIA');
INSERT INTO specialisations (specialization) VALUES ('PEDIATRIA');
INSERT INTO specialisations (specialization) VALUES ('PSIQUIATRIA');
INSERT INTO specialisations (specialization) VALUES ('REUMATOLOGIA');
INSERT INTO specialisations (specialization) VALUES ('ORTOPEDIA');
INSERT INTO specialisations (specialization) VALUES ('ANESTESIA');
INSERT INTO specialisations (specialization) VALUES ('CIRURGIA');

/*
	Sub Especializações dos Médicos
*/
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (1, 'INTERVENCIONISTA'); -- CARDIOLOGISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (1, 'ECOCARDIOGRAFIA');	-- CARDIOLOGISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (2, 'DERMATOPATOLOGIA');	-- DERMATOLOGISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (2, 'ESTETICA');			-- DERMATOLOGISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (3, 'GLAUCOMA');			-- OFTALMOLOGISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (3, 'CORNEA');			-- OFTALMOLOGISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (4, 'NEONATOLOGIA');		-- PEDIATRA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (4, 'INTENSIVA');		-- PEDIATRA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (5, 'GERIARTRICA');		-- PSIQUIATRA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (5, 'EMERGENCIA');		-- PSIQUIATRA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (6, 'AUTOIMUNE');		-- REUMATOLOGISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (6, 'DEGENERATIVA');		-- REUMATOLOGISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (7, 'DESPORTIVA');		-- ORTOPEDISTA
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (7, 'COLUNA');			-- ORTOPEDISTA

INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'CARDIOLOGIA');	-- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'DERMATOLOGIA');	-- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'OFTALMOLOGIA');	-- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'PEDIATRIA');	-- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'PSIQUIATRIA');	-- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'REUMATOLOGIA');	-- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'ORTOPEDIA');	-- CIRURGIAO

/*
	Categorias das Enfermeiras
*/
INSERT INTO nurse_categories (category) VALUES ('CIRURGIAS');
INSERT INTO nurse_categories (category) VALUES ('CONSULTAS');
INSERT INTO nurse_categories (category) VALUES ('HOSPITALIZACOES');


/*
	Inserir dados na tabela employees para os médicos
*/
INSERT INTO employees (salary, start_date, final_date, ctype_id, person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type)
VALUES
    (10000.00, '2020-01-01', NULL, 1, 123456789, 'Carlos Mendes', 'Viseu', '123456789', 'carlos', encrypt('senha123', 'my_secret_key'), 'carlos@email.com', 2),
    (9000.00, '2019-05-15', NULL, 1, 987654321, 'Ana Silva', 'Coimbra', '987654321', 'ana', encrypt('senha456', 'my_secret_key'), 'ana@email.com', 2),
    (9500.00, '2020-03-10', NULL, 1, 456789123, 'Ricardo Oliveira', 'Lisboa', '456789123', 'ricardo', encrypt('senha789', 'my_secret_key'), 'ricardo@email.com', 2),
    (8500.00, '2018-09-20', NULL, 1, 789123456, 'Marta Santos', 'Porto', '789123456', 'marta', encrypt('senha1011', 'my_secret_key'), 'marta@email.com', 2),
    (8800.00, '2019-12-05', NULL, 1, 234567891, 'José Ferreira', 'Braga', '234567891', 'jose', encrypt('senha1213', 'my_secret_key'), 'jose@email.com', 2),
    (9200.00, '2019-08-10', NULL, 1, 678912345, 'Sofia Almeida', 'Viseu', '678912345', 'sofia', encrypt('senha1415', 'my_secret_key'), 'sofia@email.com', 2),
    (8700.00, '2020-04-25', NULL, 1, 345678912, 'Tiago Martins', 'Coimbra', '345678912', 'tiago', encrypt('senha1617', 'my_secret_key'), 'tiago@email.com', 2),
    (9200.00, '2018-11-15', NULL, 1, 891234567, 'Manuel Pereira', 'Faro', '891234567', 'manuel', encrypt('senha1819', 'my_secret_key'), 'manuel@email.com', 2),
	(10000.00, '2020-01-02', NULL, 1, 123436789, 'Carlos Meneses', 'Vila Real', '123356789', 'carlosm', encrypt('senha223', 'my_secret_key'), 'carlosm@email.com', 2),
    (9000.00, '2019-05-16', NULL, 1, 987653321, 'Ana Carla', 'Aveiro', '987654324', 'anac', encrypt('senha426', 'my_secret_key'), 'anac@email.com', 2);


/*
	Inserir dados na tabela employees para as enfermeiras
*/
INSERT INTO employees (salary, start_date, final_date, ctype_id, person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type)
VALUES
    (3500.00, '2019-03-20', NULL, 2, 111222333, 'Maria Oliveira', 'Castelo Branco', '111222333', 'maria', encrypt('senha21', 'my_secret_key'), 'maria@email.com', 3),
    (3400.00, '2020-02-10', NULL, 2, 444555666, 'Joana Santos', 'Santarem', '444555666', 'joana', encrypt('senha22', 'my_secret_key'), 'joana@email.com', 3),
    (3600.00, '2018-08-15', NULL, 2, 777888999, 'Ana Costa', 'Beja', '777888999', 'ana_c', encrypt('senha23', 'my_secret_key'), 'ana_c@email.com', 3);

/*
	Inserir dados na tabela employees para o assistente
*/
INSERT INTO employees (salary, start_date, final_date, ctype_id, person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type)
VALUES
    (2000.00, '2017-12-01', NULL, 2, 999888777, 'Pedro Rodrigues', 'Coimbra', '999888777', 'pedro', encrypt('senha24', 'my_secret_key'), 'pedro@email.com', 4),
	(3000.00, '2017-12-02', NULL, 2, 999888277, 'Rodrigo Rodrigues', 'Viseu', '999882777', 'rodrigo', encrypt('senha25', 'my_secret_key'), 'rrodrigues@email.com', 4);

/*
	Inserir médicos
*/
INSERT INTO doctors (ml_id, ml_issue_date, ml_expiration_date, person_id)
VALUES
    (DEFAULT, '2023-01-15', '2025-01-15', 
        (SELECT person_id FROM employees WHERE person_name = 'Carlos Mendes')),
    (DEFAULT, '2022-06-10', '2024-06-10', 
        (SELECT person_id FROM employees WHERE person_name = 'Ana Silva')),
    (DEFAULT, '2023-03-20', '2025-03-20', 
        (SELECT person_id FROM employees WHERE person_name = 'Ricardo Oliveira')),
    (DEFAULT, '2022-08-05', '2024-08-05', 
        (SELECT person_id FROM employees WHERE person_name = 'Marta Santos')),
    (DEFAULT, '2023-02-28', '2025-02-28', 
        (SELECT person_id FROM employees WHERE person_name = 'José Ferreira')),
    (DEFAULT, '2022-12-10', '2024-12-10', 
        (SELECT person_id FROM employees WHERE person_name = 'Sofia Almeida')),
    (DEFAULT, '2023-04-25', '2025-04-25', 
        (SELECT person_id FROM employees WHERE person_name = 'Tiago Martins')),
    (DEFAULT, '2022-11-15', '2024-11-15', 
        (SELECT person_id FROM employees WHERE person_name = 'Manuel Pereira')),
	(DEFAULT, '2023-01-15', '2025-01-15', 
        (SELECT person_id FROM employees WHERE person_name = 'Carlos Meneses')),
    (DEFAULT, '2022-06-10', '2024-06-10', 
        (SELECT person_id FROM employees WHERE person_name = 'Ana Carla'));

/*
	Inserir especializações dos médicos e sub-especializações
*/
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (1,1);
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (2,2);
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (3,3);
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (4,4);
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (5,5);
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (6,6);
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (7,7);
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (8,8);
INSERT INTO specialisations_doctors (spec_id, doctor_id) VALUES (9,9);

INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (1,1);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (3,2);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (5,3);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (7,4);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (5,5);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (9,6);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (11,7);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (13,8);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (15,9);
INSERT INTO sub_specialisations_doctors (sub_spec_id, doctor_id) VALUES (16,9);


/*
    
*/

/*
	Inserir enfermeiras
*/
INSERT INTO nurses (person_id)
VALUES
    ((SELECT person_id FROM employees WHERE person_name = 'Maria Oliveira')),
    ((SELECT person_id FROM employees WHERE person_name = 'Joana Santos')),
    ((SELECT person_id FROM employees WHERE person_name = 'Ana Costa'));

/*
	Inserir categorias nas enfermeiras
*/
INSERT INTO nurses_categories (nurse_id, category_id) 
VALUES 
    ((SELECT person_id FROM employees WHERE person_name = 'Maria Oliveira'),
        (SELECT category_id FROM nurse_categories WHERE category = 'CIRURGIAS')),
    ((SELECT person_id FROM employees WHERE person_name = 'Joana Santos'),
        (SELECT category_id FROM nurse_categories WHERE category = 'CONSULTAS')),
    ((SELECT person_id FROM employees WHERE person_name = 'Ana Costa'),
        (SELECT category_id FROM nurse_categories WHERE category = 'HOSPITALIZACOES')),
    ((SELECT person_id FROM employees WHERE person_name = 'Ana Costa'),
        (SELECT category_id FROM nurse_categories WHERE category = 'CIRURGIAS')),
    ((SELECT person_id FROM employees WHERE person_name = 'Ana Costa'),
        (SELECT category_id FROM nurse_categories WHERE category = 'CONSULTAS'));
    

/*
	Inserir assistentes
*/
INSERT INTO assistants (person_id)
VALUES ((SELECT person_id FROM employees WHERE person_name = 'Pedro Rodrigues'));

INSERT INTO assistants (person_id)
VALUES ((SELECT person_id FROM employees WHERE person_name = 'Rodrigo Rodrigues'));

/*
	Inserir pacientes
*/
INSERT INTO patients (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type)
VALUES
    (123456789, 'João Silva', 'Viana do Castelo', '111222333', 'joao', encrypt('senha123', 'my_secret_key'), 'joao@email.com', 1),
    (987654321, 'Ana Sousa', 'Leiria', '444555666', 'ana', encrypt('senha456', 'my_secret_key'), 'ana@email.com', 1),
    (456789123, 'Carlos Santos', 'Lisboa', '777888999', 'carlos', encrypt('senha789', 'my_secret_key'), 'carlos@email.com', 1),
    (789123456, 'Marta Ferreira', 'Santarem', '101112131', 'marta', encrypt('senha1011', 'my_secret_key'), 'marta@email.com', 1),
    (234567891, 'Pedro Almeida', 'Viseu', '314151617', 'pedromaria', encrypt('senha1213', 'my_secret_key'), 'pedromaria@email.com', 1),
    (678912345, 'Sofia Costa', 'Aveiro', '181920212', 'sofia', encrypt('senha1415', 'my_secret_key'), 'sofia@email.com', 1),
    (345678912, 'Rita Oliveira', 'Coimbra', '222324252', 'rita', encrypt('senha1617', 'my_secret_key'), 'rita@email.com', 1),
    (891234567, 'Hugo Martins', 'Beja', '262728293', 'hugo', encrypt('senha1819', 'my_secret_key'), 'hugo@email.com', 1);

/*
    Inserir medicamentos
*/
INSERT INTO medicines(medication, dosage) VALUES ('BRUFFEN', 330);
INSERT INTO medicines(medication, dosage) VALUES ('PARACETAMOL', 500);

INSERT INTO probabilities(prob) VALUES (37);
INSERT INTO probabilities(prob) VALUES (50);

INSERT INTO side_effects(side_effect, prob_id) VALUES ('DOR DE CABEÇA', 1);
INSERT INTO side_effects(side_effect, prob_id) VALUES ('TONTURA', 2);

INSERT INTO side_effects_medicines(side_effect_id, medication_id) VALUES (1, 1);
INSERT INTO side_effects_medicines(side_effect_id, medication_id) VALUES (2, 2);


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
