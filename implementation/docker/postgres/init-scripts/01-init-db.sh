#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";

    -- Create application user
    CREATE USER appuser WITH PASSWORD 'apppassword';
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO appuser;

    -- Create schemas
    CREATE SCHEMA IF NOT EXISTS app;
    CREATE SCHEMA IF NOT EXISTS audit;

    GRANT ALL ON SCHEMA app TO appuser;
    GRANT ALL ON SCHEMA audit TO appuser;

    -- Set search path
    ALTER DATABASE $POSTGRES_DB SET search_path TO app, public;

    \echo 'Database initialization completed'
EOSQL
