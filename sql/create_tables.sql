CREATE TABLE employees (
	salary	 			FLOAT(8) NOT NULL,
	start_date	 		DATE NOT NULL,
	final_date	 		DATE,
	ctype_id 			BIGINT NOT NULL,
	person_id		 	SERIAL,
	person_cc		 	BIGINT NOT NULL,
	person_name		 	VARCHAR(20) NOT NULL,
	person_address	 	VARCHAR(50) NOT NULL,
	person_phone		VARCHAR(10) NOT NULL,
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
	person_phone	 	VARCHAR(10) NOT NULL,
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
	presc_id 				BIGSERIAL,
	presc_date				DATE NOT NULL,
	presc_validity_date 	DATE NOT NULL,
	PRIMARY KEY(presc_id)
);

CREATE TABLE medicines (
	medication_id		BIGSERIAL,
	medication	 		VARCHAR(20) NOT NULL,
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

CREATE TABLE posologies (
	posology_id 	BIGSERIAL,
	dosage			INTEGER NOT NULL,
	frequency		INTEGER NOT NULL,
	PRIMARY KEY(posology_id)
);

CREATE TABLE posologies_medicines (
	posology_id	 		BIGINT,
	medication_id		BIGINT,
	PRIMARY KEY(posology_id, medication_id)
);

CREATE TABLE posologies_prescriptions (
	posology_id 	BIGINT,
	presc_id 		BIGINT,
	PRIMARY KEY(posology_id,presc_id)
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
ALTER TABLE posologies_prescriptions ADD CONSTRAINT posologies_prescriptions_fk1 FOREIGN KEY (posology_id) REFERENCES posologies(posology_id);
ALTER TABLE posologies_prescriptions ADD CONSTRAINT posologies_prescriptions_fk2 FOREIGN KEY (presc_id) REFERENCES prescriptions(presc_id);
ALTER TABLE posologies_medicines ADD CONSTRAINT posologies_medicines_fk1 FOREIGN KEY (posology_id) REFERENCES posologies(posology_id);
ALTER TABLE posologies_medicines ADD CONSTRAINT posologies_medicines_fk2 FOREIGN KEY (medication_id) REFERENCES medicines(medication_id);
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