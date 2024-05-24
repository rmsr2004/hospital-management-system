CREATE DATABASE hospital_db;

CREATE USER hosp_user WITH PASSWORD 'hospninja';

GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hosp_user;