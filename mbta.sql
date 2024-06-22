CREATE DATABASE IF NOT EXISTS MBTAdb;

USE MBTAdb;

DROP TABLE IF EXISTS mbta_buses;

CREATE TABLE mbta_buses (
    record_num int AUTO_INCREMENT PRIMARY KEY,
    route_num int DEFAULT 1,
    id varchar(255) NOT NULL,
    bearing int NOT NULL,
    current_status varchar(15) CHECK (current_status IN ('STOPPED_AT','IN_TRANSIT_TO')),
    current_stop_sequence int,
    direction_id boolean NOT NULL,
    latitude decimal(11,8) NOT NULL,
    longitude decimal(11,8) NOT NULL,
    updated_at datetime
);