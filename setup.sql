CREATE DATABASE job_scraper;

\c job_scraper

CREATE TABLE company (
    id INT GENERATED ALWAYS AS IDENTITY,
    name TEXT,
    url TEXT,
    type TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE job_location (
    id INT GENERATED ALWAYS AS IDENTITY,
    location TEXT,
    PRIMARY KEY (id)
);

 CREATE TABLE salary (
    id INT GENERATED ALWAYS AS IDENTITY,
    salary INT,
    PRIMARY KEY (id)
);

 CREATE TABLE salary_type (
    id INT GENERATED ALWAYS AS IDENTITY,
    type TEXT,
    PRIMARY KEY (id)
);