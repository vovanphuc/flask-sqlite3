DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id integer primary key autoincrement,
    name string not null,
);
CREATE TABLE date_time (
    id integer primary key autoincrement,
    id_nv integer not null,
    status boolean default(TRUE),
    time_checkin time,
);

