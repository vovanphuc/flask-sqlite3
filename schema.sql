DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id integer primary key autoincrement,
    name string not null,
);
CREATE TABLE check_in (
    id integer primary key autoincrement,
    id_nv integer not null,
    status boolean default(TRUE),
    date string,
    time string,
);

