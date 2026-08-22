#!/bin/sh
set -eu

for variable_name in MYSQL_DATABASE MYSQL_USER MYSQL_MIGRATION_USER
do
    eval "variable_value=\${${variable_name}:-}"

    case "${variable_value}" in
        ''|*[!A-Za-z0-9_]*)
            echo "${variable_name} contiene un valor no permitido" >&2
            exit 1
            ;;
    esac
done

if [ "${MYSQL_USER}" = "root" ]; then
    echo "MYSQL_USER no puede ser root" >&2
    exit 1
fi

if [ -z "${MYSQL_MIGRATION_PASSWORD:-}" ]; then
    echo "MYSQL_MIGRATION_PASSWORD no esta definida" >&2
    exit 1
fi

migration_password_sql=$(
    printf '%s' "${MYSQL_MIGRATION_PASSWORD}" |
        sed "s/'/''/g"
)

mysql \
    --protocol=socket \
    -uroot \
    -p"${MYSQL_ROOT_PASSWORD}" <<-EOSQL
REVOKE ALL PRIVILEGES, GRANT OPTION
FROM '${MYSQL_USER}'@'%';

GRANT
    SELECT,
    INSERT,
    UPDATE,
    DELETE,
    EXECUTE
ON ${MYSQL_DATABASE}.*
TO '${MYSQL_USER}'@'%';

CREATE USER IF NOT EXISTS
    '${MYSQL_MIGRATION_USER}'@'%'
    IDENTIFIED BY '${migration_password_sql}';

GRANT
    SELECT,
    INSERT,
    UPDATE,
    DELETE,
    CREATE,
    DROP,
    REFERENCES,
    INDEX,
    ALTER,
    EXECUTE,
    CREATE VIEW,
    SHOW VIEW,
    CREATE ROUTINE,
    ALTER ROUTINE,
    TRIGGER
ON ${MYSQL_DATABASE}.*
TO '${MYSQL_MIGRATION_USER}'@'%';
EOSQL
