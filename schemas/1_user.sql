CREATE ROLE stupidity_db_user
    LOGIN
    PASSWORD 'stupidity_db_password';

GRANT CONNECT ON DATABASE stupidity_db TO stupidity_db_user;

GRANT pg_read_all_data TO stupidity_db_user;
GRANT pg_write_all_data TO stupidity_db_user;
