DROP DATABASE IF EXISTS :dbname;
CREATE DATABASE :dbname;

\c :dbname

CREATE TABLE industry (
    industry_id INT GENERATED ALWAYS AS IDENTITY,
    industry TEXT UNIQUE,
    PRIMARY KEY (industry_id)
);

CREATE TABLE salary_type (
    salary_type_id INT GENERATED ALWAYS AS IDENTITY,
    salary_type TEXT NOT NULL UNIQUE,
    PRIMARY KEY (salary_type_id)
);

CREATE TABLE requirement_type (
    requirement_type_id INT GENERATED ALWAYS AS IDENTITY,
    requirement_type TEXT NOT NULL UNIQUE,
    PRIMARY KEY (requirement_type_id)
);

CREATE TABLE location (
    location_id INT GENERATED ALWAYS AS IDENTITY,
    location TEXT UNIQUE,
    PRIMARY KEY (location_id)
);

CREATE TABLE posting_date (
    posting_date_id INT GENERATED ALWAYS AS IDENTITY,
    posting_date DATE NOT NULL UNIQUE,
    PRIMARY KEY (posting_date_id)
);

CREATE TABLE salary (
    salary_id INT GENERATED ALWAYS AS IDENTITY,
    salary FLOAT UNIQUE,
    PRIMARY KEY (salary_id)
);

CREATE TABLE employment_type (
    employment_type_id INT GENERATED ALWAYS AS IDENTITY,
    employment_type TEXT UNIQUE,
    PRIMARY KEY (employment_type_id)
);

CREATE TABLE company (
    company_id INT GENERATED ALWAYS AS IDENTITY,
    company TEXT,
    url TEXT UNIQUE,
    type TEXT,
    PRIMARY KEY (company_id)
);

CREATE TABLE title (
    title_id INT GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL UNIQUE,
    PRIMARY KEY (title_id)
);


CREATE TABLE title_category (
    title_category_id INT GENERATED ALWAYS AS IDENTITY,
    title_category TEXT NOT NULL UNIQUE,
    PRIMARY KEY (title_category_id)
);

CREATE TABLE requirement (
    requirement_id INT GENERATED ALWAYS AS IDENTITY,
    requirement TEXT NOT NULL UNIQUE,
    requirement_type_id INT NOT NULL,
    PRIMARY KEY (requirement_id),
    FOREIGN KEY (requirement_type_id) REFERENCES requirement_type(requirement_type_id)
);

CREATE TABLE job_listing (
    job_listing_id BIGINT GENERATED ALWAYS AS IDENTITY,
    job_listing TEXT NOT NULL UNIQUE,
    title_id INT NOT NULL,
    posting_date_id INT NOT NULL,
    location_id INT,
    employment_type_id INT,
    company_id INT,
    url TEXT NOT NULL UNIQUE,
    high_salary_id INT NOT NULL,
    industry_id INT,
    low_salary_id INT NOT NULL,
    salary_type_id INT NOT NULL,
    title_category_id INT NOT NULL,
    PRIMARY KEY (job_listing_id),
    FOREIGN KEY (low_salary_id) REFERENCES salary(salary_id),
    FOREIGN KEY (high_salary_id) REFERENCES salary(salary_id),
    FOREIGN KEY (location_id) REFERENCES location(location_id),
    FOREIGN KEY (posting_date_id) REFERENCES posting_date(posting_date_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (salary_type_id) REFERENCES salary_type(salary_type_id),
    FOREIGN KEY (employment_type_id) REFERENCES employment_type(employment_type_id),
    FOREIGN KEY (industry_id) REFERENCES industry(industry_id),
    FOREIGN KEY (title_category_id) REFERENCES title_category(title_category_id)
);

CREATE TABLE requirement_link (
    requirement_link_id BIGINT GENERATED ALWAYS AS IDENTITY,
    requirement_id INT NOT NULL,
    job_listing_id BIGINT NOT NULL,
    PRIMARY KEY (requirement_link_id),
    FOREIGN KEY (requirement_id) REFERENCES requirement(requirement_id),
    FOREIGN KEY (job_listing_id) REFERENCES job_listing(job_listing_id),
    CONSTRAINT unique_id_pairs UNIQUE (job_listing_id, requirement_id)
);

CREATE TABLE alias (
    alias_id BIGINT GENERATED ALWAYS AS IDENTITY,
    requirement_id INT NOT NULL,
    alias TEXT NOT NULL,
    PRIMARY KEY (alias_id),
    FOREIGN KEY (requirement_id) REFERENCES requirement(requirement_id),
    CONSTRAINT unique_alias_pairs UNIQUE (requirement_id, alias)
);

INSERT INTO requirement_type (requirement_type) VALUES ('HARD'),('SOFT'),('CERT'),('PERK');

