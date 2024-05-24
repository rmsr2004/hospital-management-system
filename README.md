# hospital-management-system

Installation Manual:
1. psql -U postgres -h 127.0.0.1 -p 5432 -f create_db.sql
2. psql -U postgres -h 127.0.0.1 -p 5432 -d hospital_db -f create_tables.sql
3. psql -U postgres -h 127.0.0.1 -p 5432 -d hospital_db -f db_functions.sql
4. psql -U postgres -h 127.0.0.1 -p 5432 -d hospital_db -f fill_db.sql
5. psql -U postgres -h 127.0.0.1 -p 5432 -d hospital_db -f user_permissions.sql

