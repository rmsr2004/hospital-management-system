/*********************************************************
*	Database for Hospital Management System				 *
* 	Authors:											 *
*		- João Afonso dos Santos Simões (2022236316)	 *
*		- João Pinho Marques (2022234692)				 *
*		- Rodrigo Miguel Santos Rodrigues (2022233032)	 *
*												 		 *									
*	Created on:	28/05/2024								 *
**********************************************************
*	user_permissions.sql: Grant privileges to            * 
*                         hospital_user                  *			
*********************************************************/

GRANT SELECT, INSERT, UPDATE ON employees TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON patients TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON nurses TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON doctors TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON assistants TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON contract_types TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON specialisations TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON appointments TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON prescriptions TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON medicines TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON side_effects TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON surgeries TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON hospitalizations TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON payments TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON bills TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON roles TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON sub_specialisations TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON nurse_categories TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON nurses_categories TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON probabilities TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON roles_appointments TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON roles_surgeries TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON nurses_roles TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON hospitalizations_prescriptions TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON side_effects_medicines TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON prescriptions_medicines TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON appointments_prescriptions TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON specialisations_doctors TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON sub_specialisations_doctors TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON posologies TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON posologies_medicines TO hospital_user;
GRANT SELECT, INSERT, UPDATE ON posologies_prescriptions TO hospital_user;


GRANT USAGE, SELECT, UPDATE ON SEQUENCE appointments_appointment_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE bills_bill_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE contract_types_ctype_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE doctors_ml_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE employees_person_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE hospitalizations_hosp_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE medicines_medication_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE nurse_categories_category_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE patients_person_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE payments_payment_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE posologies_posology_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE prescriptions_presc_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE probabilities_prob_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE roles_role_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE side_effects_side_effect_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE specialisations_spec_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE sub_specialisations_sub_spec_id_seq TO hospital_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE surgeries_surgery_id_seq TO hospital_user;
