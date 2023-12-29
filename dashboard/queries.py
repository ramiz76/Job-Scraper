
top_requirements = """
SELECT r.requirement_id AS "ID",r.requirement AS "Requirement",rt.requirement_type AS "Requirement Type", 
COUNT(DISTINCT rl.job_listing_id) AS "Listing Count",
(SELECT COUNT(*) FROM job_listing) AS "Total Listings"
FROM requirement r
JOIN requirement_link rl ON rl.requirement_id = r.requirement_id
JOIN requirement_type rt ON r.requirement_type_id = rt.requirement_type_id
JOIN job_listing j ON rl.job_listing_id = j.job_listing_id
GROUP BY r.requirement,r.requirement_id,rt.requirement_type
ORDER BY "Listing Count" DESC;"""


all_requirements = """SELECT * FROM requirement;"""

all_aliases = """SELECT requirement_id AS "Requirement ID",alias AS "Alias" FROM alias;"""

all_requirement_links = """
SELECT r.requirement_id AS "Requirement ID",r.requirement AS "Requirement",
rt.requirement_type AS "Requirement Type", jl.job_listing_id AS "Listing ID"
FROM requirement_link rl
LEFT JOIN requirement r ON rl.requirement_id = r.requirement_id
LEFT JOIN requirement_type rt ON r.requirement_type_id = rt.requirement_type_id
LEFT JOIN job_listing jl ON rl.job_listing_id = jl.job_listing_id;
"""

listing_count = """SELECT COUNT(*) FROM job_listing;"""


all_titles = """SELECT title FROM title;"""


grouped_requirements = """WITH GROUPED_SKILLS AS (
    SELECT
        r.requirement_id,
        r.requirement,
        CASE
            WHEN r.requirement ILIKE '%SQL%' THEN 'SQL'
            WHEN r.requirement ILIKE '%AWS%' OR r.requirement ILIKE '%Amazon%' THEN 'AWS'
            WHEN r.requirement ILIKE '%Azure%' THEN 'Azure'
            WHEN r.requirement ILIKE '%GCP%' OR r.requirement ILIKE '%Google%' THEN 'GCP'
            WHEN r.requirement ILIKE '%Python%' THEN 'Python'
            ELSE r.requirement
        END AS skill_group,
        CASE 
            WHEN r.requirement ILIKE '%SQL%' OR 
                 r.requirement ILIKE '%AWS%' OR r.requirement ILIKE '%Amazon%' OR 
                 r.requirement ILIKE '%Azure%' OR 
                 r.requirement ILIKE '%GCP%' OR r.requirement ILIKE '%Google%' OR 
                 r.requirement ILIKE '%Python%' THEN 'HARD'
            ELSE (SELECT requirement_type FROM requirement_type WHERE requirement_type_id = r.requirement_type_id)
        END AS requirement_type
    FROM 
        requirement r
)
SELECT 
    gs.skill_group AS "Requirement",
    COUNT(DISTINCT rl.job_listing_id) AS "Listing Count",
    gs.requirement_type AS "Requirement Type"
FROM 
    requirement_link rl
JOIN 
    GROUPED_SKILLS gs ON rl.requirement_id = gs.requirement_id
GROUP BY 
    "Requirement", "Requirement Type"
ORDER BY 
    "Listing Count" DESC;
"""


listing_data = """SELECT 
    jl.job_listing_id, jl.job_listing, jl.url,
    t.title,
    pd.posting_date,
    loc.location,
    et.employment_type,
    co.company, co.url AS company_url, co.type AS company_type,
    s1.salary AS low_salary, s2.salary AS high_salary,
    st.salary_type,
    ind.industry,
    rt.requirement_type, r.requirement,tc.title_category,
       CASE
           WHEN t.title ILIKE '%senior%' OR
                t.title ILIKE '%lead%' OR
                t.title ILIKE '%principal%' OR
                t.title ILIKE '%head%' OR
                t.title ILIKE '%manager%' THEN 'Senior Level'
           WHEN t.title ILIKE '%junior%' OR
                t.title ILIKE '%graduate%' OR
                t.title ILIKE '%apprentice%' OR
                t.title ILIKE '%intern%' OR
                t.title ILIKE '%early careers%' THEN 'Junior Level'
           ELSE 'Mid Level'
       END AS title_level
FROM 
    job_listing jl
JOIN 
    title t ON jl.title_id = t.title_id
JOIN 
    posting_date pd ON jl.posting_date_id = pd.posting_date_id
JOIN 
    location loc ON jl.location_id = loc.location_id
JOIN 
    employment_type et ON jl.employment_type_id = et.employment_type_id
JOIN 
    company co ON jl.company_id = co.company_id
JOIN 
    salary s1 ON jl.low_salary_id = s1.salary_id
JOIN 
    salary s2 ON jl.high_salary_id = s2.salary_id
JOIN 
    salary_type st ON jl.salary_type_id = st.salary_type_id
JOIN 
    industry ind ON jl.industry_id = ind.industry_id
LEFT JOIN 
    requirement_link rl ON jl.job_listing_id = rl.job_listing_id
LEFT JOIN 
    requirement r ON rl.requirement_id = r.requirement_id
LEFT JOIN 
    requirement_type rt ON r.requirement_type_id = rt.requirement_type_id
JOIN 
    title_category tc  ON tc.title_category_id = jl.title_category_id;
"""
