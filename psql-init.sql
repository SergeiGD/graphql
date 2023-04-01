CREATE TABLE IF NOT EXISTS permission (
    id serial primary key,
    name varchar(255) NOT NULL,
    code varchar(255) NOT NULL,
    PRIMARY KEY (id)
)
