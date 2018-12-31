DROP TABLE IF EXISTS sensor_temps;
DROP TABLE IF EXISTS owm_temps;
DROP TABLE IF EXISTS metoffice_temps;

CREATE TABLE sensor_temps(
measurement_time DATETIME,
temp NUMERIC
);

CREATE TABLE owm_temps(
measurement_time DATETIME,
temp NUMERIC
);

CREATE TABLE metoffice_temps(
measurement_time DATETIME,
temp NUMERIC
);
