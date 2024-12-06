-- Переключаемся на базу данных, созданную через POSTGRES_DB
\c "scopus-server"

-- Создаем последовательность для генерации уникальных значений
CREATE SEQUENCE request_id_seq;

-- Создаем таблицу и используем последовательность для поля id
CREATE TABLE request (
    id BIGINT PRIMARY KEY DEFAULT nextval('request_id_seq'),
    folder_id VARCHAR(60) NOT NULL,
    first_status VARCHAR(50) DEFAULT 'false',
    second_status VARCHAR(50) DEFAULT 'false',
    search_type VARCHAR(50),
    query TEXT,
    result JSONB
);
