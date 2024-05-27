/*********************************************************
*	Database for Hospital Management System				 *
* 	Authors:											 *
*		- João Afonso dos Santos Simões (2022236316)	 *
*		- João Pinho Marques (2022234692)				 *
*		- Rodrigo Miguel Santos Rodrigues (2022233032)	 *
*												 		 *									
*	Created on:	28/05/2024								 *
**********************************************************
*	fill_db.sql: SCRIPT TO FILL THE DATABASE WITH DATA	 *			
*********************************************************/

/*
*	Contract Types
*/
INSERT INTO contract_types (ctype) VALUES ('EFETIVO');
INSERT INTO contract_types (ctype) VALUES ('PART-TIME');
INSERT INTO contract_types (ctype) VALUES ('TEMPORARIO');
/*
*	Nurses Roles - Surgeries
*/
INSERT INTO roles (role, role_type) VALUES ('ASSISTENTE', 1);
INSERT INTO roles (role, role_type) VALUES ('MONITOR', 1);
INSERT INTO roles (role, role_type) VALUES ('ANESTESISTA', 1);
/*
*	Nurses Roles - Appointments
*/
INSERT INTO roles (role, role_type) VALUES ('TRIAGEM', 0);
INSERT INTO roles (role, role_type) VALUES ('PREPARACAO', 0);
INSERT INTO roles (role, role_type) VALUES ('SUPORTE', 0);
/*
*	Doctors specialisations
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
*	Doctors sub specialisations
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
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'CARDIOLOGIA');	    -- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'DERMATOLOGIA');	    -- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'OFTALMOLOGIA');	    -- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'PEDIATRIA');	    -- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'PSIQUIATRIA');	    -- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'REUMATOLOGIA');	    -- CIRURGIAO
INSERT INTO sub_specialisations (spec_id, sub_spec) VALUES (9, 'ORTOPEDIA');	    -- CIRURGIAO
/*
*	Nurses Categories
*/
INSERT INTO nurse_categories (category) VALUES ('CIRURGIAS');
INSERT INTO nurse_categories (category) VALUES ('CONSULTAS');
INSERT INTO nurse_categories (category) VALUES ('HOSPITALIZACOES');
/*
*	Insert doctors into employees
*/
INSERT INTO employees (salary, start_date, final_date, ctype_id, person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type)
VALUES
    (10000.00, '2020-01-01', NULL, 1, '12345789', 'Carlos Mendes', 'Viseu', '123452667', 'carlos', encrypt('senha123', 'my_secret_key'), 'carlos@email.com', 2),
    (9000.00, '2019-05-15', NULL, 1, '98765321', 'Ana Silva', 'Coimbra', '987654322', 'ana', encrypt('senha456', 'my_secret_key'), 'ana@email.com', 2),
    (9500.00, '2020-03-10', NULL, 1, '45679123', 'Ricardo Oliveira', 'Lisboa', '452678923', 'ricardo', encrypt('senha789', 'my_secret_key'), 'ricardo@email.com', 2),
    (8500.00, '2018-09-20', NULL, 1, '78923456', 'Marta Santos', 'Porto', '789123526', 'marta', encrypt('senha1011', 'my_secret_key'), 'marta@email.com', 2),
    (8800.00, '2019-12-05', NULL, 1, '23567891', 'José Ferreira', 'Braga', '234578291', 'jose', encrypt('senha1213', 'my_secret_key'), 'jose@email.com', 2),
    (9200.00, '2019-08-10', NULL, 1, '68912345', 'Sofia Almeida', 'Viseu', '678123245', 'sofia', encrypt('senha1415', 'my_secret_key'), 'sofia@email.com', 2),
    (8700.00, '2020-04-25', NULL, 1, '45678912', 'Tiago Martins', 'Coimbra', '456728912', 'tiago', encrypt('senha1617', 'my_secret_key'), 'tiago@email.com', 2),
    (9200.00, '2018-11-15', NULL, 1, '89234567', 'Manuel Pereira', 'Faro', '812345267', 'manuel', encrypt('senha1819', 'my_secret_key'), 'manuel@email.com', 2),
	(10000.00, '2020-01-02', NULL, 1, '13436789', 'Carlos Meneses', 'Vila Real', '132356789', 'carlosm', encrypt('senha223', 'my_secret_key'), 'carlosm@email.com', 2),
    (9000.00, '2019-05-16', NULL, 1, '97653321', 'Ana Carla', 'Aveiro', '987543224', 'anac', encrypt('senha426', 'my_secret_key'), 'anac@email.com', 2);
/*
*	Insert nurses into employees
*/
INSERT INTO employees (salary, start_date, final_date, ctype_id, person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type)
VALUES
    (3500.00, '2019-03-20', NULL, 2, '11222333', 'Maria Oliveira', 'Castelo Branco', '111222333', 'maria', encrypt('senha21', 'my_secret_key'), 'maria@email.com', 3),
    (3400.00, '2020-02-10', NULL, 2,'44555666', 'Joana Santos', 'Santarem', '444552566', 'joana', encrypt('senha22', 'my_secret_key'), 'joana@email.com', 3),
    (3600.00, '2018-08-15', NULL, 2, '77882999', 'Ana Costa', 'Beja', '777882899', 'ana_c', encrypt('senha23', 'my_secret_key'), 'ana_c@email.com', 3);
/*
*	Insert assistants into employees
*/
INSERT INTO employees (salary, start_date, final_date, ctype_id, person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type)
VALUES
    (2000.00, '2017-12-01', NULL, 2, '99888777', 'Pedro Rodrigues', 'Coimbra', '499828777', 'pedro', encrypt('senha24', 'my_secret_key'), 'pedro@email.com', 4),
	(3000.00, '2017-12-02', NULL, 2, '99888277', 'Rodrigo Rodrigues', 'Viseu', '699822777', 'rodrigo', encrypt('senha25', 'my_secret_key'), 'rrodrigues@email.com', 4);
/*
*	Insert doctors into doctors
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
*	Associate doctors with specialisations and sub specialisations
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
*	Insert nurses
*/
INSERT INTO nurses (person_id)
VALUES
    ((SELECT person_id FROM employees WHERE person_name = 'Maria Oliveira')),
    ((SELECT person_id FROM employees WHERE person_name = 'Joana Santos')),
    ((SELECT person_id FROM employees WHERE person_name = 'Ana Costa'));
/*
*   Associate nurses with categories
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
*	Insert Assistants
*/
INSERT INTO assistants (person_id)
VALUES ((SELECT person_id FROM employees WHERE person_name = 'Pedro Rodrigues'));
INSERT INTO assistants (person_id)
VALUES ((SELECT person_id FROM employees WHERE person_name = 'Rodrigo Rodrigues'));
/*
*	Insert patients
*/
INSERT INTO patients (person_cc, person_name, person_address, person_phone, person_username, person_password, person_email, person_type)
VALUES
    (12445789, 'João Silva', 'Viana do Castelo', '111232333', 'joao', encrypt('senha1323', 'my_secret_key'), 'joao@email.com', 1),
    (98764321, 'Ana Sousa', 'Leiria', '444555666', 'ana', encrypt('senha456', 'my_secret_key'), 'ana@email.com', 1),
    (45689123, 'Carlos Santos', 'Lisboa', '777888999', 'carlos', encrypt('senha789', 'my_secret_key'), 'carlos@email.com', 1),
    (78123456, 'Marta Ferreira', 'Santarem', '101112131', 'marta', encrypt('senha1011', 'my_secret_key'), 'marta@email.com', 1),
    (24567891, 'Pedro Almeida', 'Viseu', '314151617', 'pedromaria', encrypt('senha1213', 'my_secret_key'), 'pedromaria@email.com', 1),
    (78912345, 'Sofia Costa', 'Aveiro', '181920212', 'sofia', encrypt('senha1415', 'my_secret_key'), 'sofia@email.com', 1),
    (45638912, 'Rita Oliveira', 'Coimbra', '222324252', 'rita', encrypt('senha1617', 'my_secret_key'), 'rita@email.com', 1),
    (91234567, 'Hugo Martins', 'Beja', '262728293', 'hugo', encrypt('senha1819', 'my_secret_key'), 'hugo@email.com', 1);
/*
*   Insert medicines, probabilities and side effects
*/
INSERT INTO medicines(medication) VALUES ('BRUFFEN');
INSERT INTO medicines(medication) VALUES ('PARACETAMOL');
INSERT INTO medicines(medication) VALUES ('ASPIRINA');
INSERT INTO medicines(medication) VALUES ('BILASTINA');
INSERT INTO medicines(medication) VALUES ('XAROPE');

INSERT INTO probabilities(prob) VALUES (37);
INSERT INTO probabilities(prob) VALUES (50);

INSERT INTO side_effects(side_effect, prob_id) VALUES ('DOR DE CABEÇA', 1);
INSERT INTO side_effects(side_effect, prob_id) VALUES ('TONTURA', 2);

INSERT INTO side_effects_medicines(side_effect_id, medication_id) VALUES (1, 1);
INSERT INTO side_effects_medicines(side_effect_id, medication_id) VALUES (2, 2);
INSERT INTO side_effects_medicines(side_effect_id, medication_id) VALUES (1, 3);
INSERT INTO side_effects_medicines(side_effect_id, medication_id) VALUES (2, 4);
INSERT INTO side_effects_medicines(side_effect_id, medication_id) VALUES (2, 5);