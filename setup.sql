DROP DATABASE IF EXISTS job_scraper;
CREATE DATABASE job_scraper;

\c job_scraper

CREATE TABLE industry (
    industry_id SMALLINT NOT NULL,
    industry_name TEXT NOT NULL,
    PRIMARY KEY (industry_id),
    UNIQUE (industry_name)
);

CREATE TABLE salary_type (
    type_id SMALLINT NOT NULL,
    type TEXT NOT NULL,
    PRIMARY KEY (type_id)
);

CREATE TABLE requirement_type (
    type_id SMALLINT NOT NULL,
    type_name TEXT NOT NULL,
    PRIMARY KEY (type_id),
    UNIQUE (type_name)
);

CREATE TABLE job_location (
    location_id SMALLINT NOT NULL,
    location TEXT NOT NULL,
    PRIMARY KEY (location_id),
    UNIQUE (location)
);

CREATE TABLE posting_date (
    date_id SMALLINT NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (date_id),
    UNIQUE (date)
);

CREATE TABLE company (
    company_id SMALLINT NOT NULL,
    company_name TEXT NOT NULL,
    company_url TEXT NOT NULL,
    company_type TEXT NOT NULL,
    PRIMARY KEY (company_id),
    UNIQUE (company_url)
);

CREATE TABLE salary (
    salary_id SMALLINT NOT NULL,
    salary SMALLINT NOT NULL,
    PRIMARY KEY (salary_id),
    UNIQUE (salary)
);

CREATE TABLE employment_type (
    type_id SMALLINT NOT NULL,
    type_name TEXT NOT NULL,
    PRIMARY KEY (type_id),
    UNIQUE (type_name)
);

CREATE TABLE requirement (
    requirement_id SMALLINT NOT NULL,
    requirement_name TEXT NOT NULL,
    type_id SMALLINT NOT NULL,
    PRIMARY KEY (requirement_id),
    UNIQUE (requirement_name),
    FOREIGN KEY (type_id) REFERENCES requirement_type(type_id)
);

CREATE TABLE job_listing (
    job_id BIGINT NOT NULL,
    online_id SMALLINT NOT NULL,
    job_name TEXT NOT NULL,
    date_id SMALLINT NOT NULL,
    location_id SMALLINT NOT NULL,
    company_id SMALLINT NOT NULL,
    listing_url TEXT NOT NULL,
    high_salary_id SMALLINT NOT NULL,
    industry_id SMALLINT NOT NULL,
    employment_id SMALLINT NOT NULL,
    low_salary_id SMALLINT NOT NULL,
    salary_type_id SMALLINT NOT NULL,
    PRIMARY KEY (job_id),
    UNIQUE (online_id),
    UNIQUE (listing_url),
    FOREIGN KEY (low_salary_id) REFERENCES salary(salary_id),
    FOREIGN KEY (location_id) REFERENCES job_location(location_id),
    FOREIGN KEY (date_id) REFERENCES posting_date(date_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (salary_type_id) REFERENCES salary_type(type_id),
    FOREIGN KEY (employment_id) REFERENCES employment_type(type_id),
    FOREIGN KEY (high_salary_id) REFERENCES salary(salary_id),
    FOREIGN KEY (industry_id) REFERENCES industry(industry_id)
);

CREATE TABLE listing_requirement_link (
    link_id SMALLINT NOT NULL,
    requirement_id SMALLINT NOT NULL,
    job_id BIGINT NOT NULL,
    PRIMARY KEY (link_id),
    FOREIGN KEY (requirement_id) REFERENCES requirement(requirement_id),
    FOREIGN KEY (job_id) REFERENCES job_listing(job_id)
);
