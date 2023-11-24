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


listing_data = """
SELECT jl.job_listing_id,jl.job_listing,jl.title_id,pd.posting_date_id,lo.location_id,
et.employment_type_id,co.company_id,jl.url,hs.salary AS high_salary,ls.salary AS low_salary,i.industry_id,
st.salary_type_id
FROM job_listing jl
JOIN salary ls ON jl.low_salary_id = ls.salary_id
JOIN salary hs ON jl.high_salary_id = hs.salary_id
JOIN location lo ON lo.location_id = jl.location_id
JOIN posting_date pd ON pd.posting_date_id = jl.posting_date_id
JOIN company co ON co.company_id = jl.company_id
JOIN salary_type st ON st.salary_type_id = jl.salary_type_id
JOIN employment_type et ON et.employment_type_id = jl.employment_type_id
JOIN industry i ON i.industry_id = jl.industry_id;
 """
