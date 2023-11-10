"""Properties used for unit testing"""

from unittest.mock import MagicMock
from bs4 import BeautifulSoup


def FakeListingURL():
    return "https://www.fakejoblisting.com"


def FakeDriver():
    fake_driver = MagicMock()
    fake_driver.page_source = "<html><head><title>Data Engineer Jobs</title></head><body></body></html>"
    return fake_driver


def FakeWebpageHref():
    html = """<li class="res-44kvrv" data-genesis-element="TEXT" role="listitem"><a class="res-1joyc6q" 
    data-genesis-element="BUTTON" aria-label="2 of 3" 
    href="https://www.totaljobs.com/jobs/data-engineer/in-london?radius=0&amp;page=2&amp;postedWithin=3" 
    aria-busy="false" aria-current="false"><span class="res-1cekje2" data-genesis-element="BASE"><span class="res-vurnku" 
    data-genesis-element="BASE"><span aria-hidden="true">2</span></span></span></a></li><
    li class="res-44kvrv" data-genesis-element="TEXT" role="listitem"><a class="res-1joyc6q" data-genesis-element="BUTTON" 
    aria-label="3 of 3" href="https://www.totaljobs.com/jobs/data-engineer/in-london?radius=0&amp;page=3&amp;postedWithin=3"
    aria-busy="false" aria-current="false"><span class="res-1cekje2" data-genesis-element="BASE">
    <span class="res-vurnku" data-genesis-element="BASE"><span aria-hidden="true">3</span></span></span></a></li>"""
    return BeautifulSoup(html, 'html.parser')


def FakeWebpageNoHref():
    html = """<li class="res-44kvrv" data-genesis-element="TEXT" role="listitem">
    <a class="res-jma6e5" data-genesis-element="BUTTON" aria-label="1 of 1" 
    href="https://www.totaljobs.com/jobs/data-engineer/in-bristol?radius=0&amp;page=1&amp;postedWithin=3" 
    aria-busy="false" aria-current="true"><span class="res-1cekje2" data-genesis-element="BASE">
    <span class="res-vurnku" data-genesis-element="BASE"><span aria-hidden="true">1</span></span></span></a></li>"""
    return BeautifulSoup(html, 'html.parser')


def FakeWebpageListings(href):
    html = f"""<div class="res-vurnku" data-genesis-element="CARD_CONTAINER_GROUP" role="group">
    <article class="res-1tps163" data-genesis-element="CARD" id="job-item-101378062" data-at="job-item">
    <a class="res-1na8b7y" data-genesis-element="BASE" href={href} 
    data-at="job-item-title" target="_self">
</article><article class="res-1tps163" data-genesis-element="CARD" id="job-item-101378062" data-at="job-item">
    <a class="res-1na8b7y" data-genesis-element="BASE" href={href} data-at="job-item-title" target="_self">
</article><article class="res-1tps163" data-genesis-element="CARD" id="job-item-800062" data-at="job-item">
    <a class="res-1na8b7y" data-genesis-element="BASE" href={href} data-at="job-item-title" target="_self">
</article></div>"""
    return BeautifulSoup(html, 'html.parser')


def InvalidFakeListingHTML():
    html = """<html><head> This has not returned a valid job listing! </head></html>"""
    return BeautifulSoup(html, 'html.parser')


def FakeJobListingHTML():
    html = """<html><head>
    <title> Fake Data Engineer in London </title>
        <script id="jobPostingSchema" type="application/ld+json">
        {
  "@context": "http://schema.org",
  "@type": "JobPosting",
  "title": "Data Engineer",
  "url":  "https://www.fake_listing-3355",
  "datePosted": "2023-10-02T14:34+01:00",
  "validThrough": "2023-11-13T15:34+00:00",
  "description": "<div><b>Our Story</b></div><p>From its inception in 1994, Chrissie Rucker’s vision was to build a company that specialised in stylish, white, designer-quality items for the home that were not only exceptional quality, but also outstanding value for money. In addition to this devotion to simplicity, it was imperative the customer was put at the heart of everything and provided with a second-to-none shopping experience - and so The White Company was born.</p><p><br></p>Today, the company that began as a 12-page mail-order brochure has become one of the UK’s fast-growing multi-channel retailers and a leading lifestyle brand with 68 stores across the UK and a highly successful online business.<div><br></div><div><br></div><div><div><br></div><div><span><b>Our Role</b></span><p>Note: This role is being advertised in London Head Office &amp; Swan Valley, Northampton but there is only 1 live vacancy. We are open to either location.</p><p><br></p><p>Reporting to the Development Manager (Retail and Integrations), you will be building and optimising on our Data platform architecture. Working with Azure based technologies, you will be building and maintaining data pipelines, querying and analysing data and optimizing data flows. You will support broader development teams to deliver data solutions for key business requirements.</p><p><br></p><p><br></p><span><b>What you’ll be doing</b></span><ul><li>Create and maintain optimal data pipelines / ETL processes using A Data Factory</li><li>Assemble large, complex data sets using Azure Data lake that meet functional / non-functional business requirements.</li><li>Architect and extend data models for data visualisation, analytics and data transfer</li><li>Analyse and tune performance of data delivery and ensure scalability of data processes</li><li>Work with data and analytics experts to strive for greater functionality in our data systems.</li><li>Support in data governance within the data platform (Azure Data Lake &amp; other Data Platform services)</li></ul><div><br></div><div><br></div><div><b>The skills &amp; experience that you’ll need</b></div><p><b>Essential</b></p><ul><li>Strong proficiency with SQL with knowledge of best practices including debugging &amp; troubleshooting</li><li>Extensive experience in optimizing complex SQL statements and processes</li><li>Solid Relational Database design skills with an eye for performance optimisation.</li><li>Strong knowledge of different database models</li><li>Experience of creating PowerBI solutions and dashboards from row level data including data structure optimisation through to visualisation and dashboard creation.</li><li>Experience using modern data platforms and services (Data Lake, Azure Data Factory, SQL (On-prem/Cloud, Data Bricks) to build conformed and derived data models for the purpose of integrations, reporting and analytics</li><li>An ability to translate business requirements into technical specifications.</li><li>Attention to detail and ability to QA own and other team member's work.</li><li>Good experience with ETL</li><li>Good experience with Analytical/Reporting solutions</li></ul><div><br></div><p><b>Desirable</b></p><ul><li>Have programmable experience with Python, Scala or Java.</li><li>Some experience working with Machine Learning algorithms</li><li>Have cloud based experience, preferably with Azure.</li><li>Exposure to high performing, low latency or large volume data systems (i.e. 1 billion+ records, terabyte size database).</li><li>Experience with code versioning tools such as (GIT/SVN)</li><li>Working within a continuous integration environment with automated builds, deployment and unit testing.</li><li>Experience working with retail &amp; commerce data entities</li></ul><div><br></div><div><br></div><div><br></div><span><span><strong>What we’ll offer you</strong>&nbsp;</span></span><p><span>At The White Company, we value our employees for always going the extra mile for every one of our customers; we reward this with great benefits and competitive salaries.</span></p><p><span><br></span></p><ul><li><span>Discount -Up to 50% discount (dependent on contract type)</span></li><li><span>Holiday – 25 days, increasing to 28 days with length of service</span></li><li><span>Holiday Buy – opportunity to buy up to an additional 5 days holiday</span></li><li><span>Bonus Potential - In addition to our competitive salaries, all our permanent employees are entitled to join a discretionary bonus scheme. (dependent on contract type)</span></li><li><span>Perkplace Benefits Platform – offering a variety of discounts across wellbeing and lifestyle</span></li><li>Wagestream Money Management app - access to Wagestream gives you power over your pay and supports financial wellbeing</li><li>Continued Development – <span>Inclusion on our Leadership Development Programme</span></li><li>Pension Scheme</li><li>Life Assurance</li><li>Private Medical</li></ul><div><br></div><p><strong>Additional Benefits</strong></p><ul><li><span>Fruit basket daily</span></li><li><span>Tea and coffee provided</span></li><li><span>Working from Home - option to work from home on Mondays and Fridays</span></li><li>Social - Christmas party/social events throughout the year</li><li>Seasonal Sample Sales</li><li>Volunteer Day - with a charity of your choice</li></ul><div><br></div><div><br></div><span><b>Our Equality Diversity and Inclusion statement of commitment</b></span><p>At The White Company we are committed to creating an inclusive culture that welcomes and celebrates a diversity of backgrounds and identities.</p><p><br></p><p>We are working together to ensure our environment is one where people can bring their authentic selves to work, where their contribution is valued, ability enhanced, and perspective appreciated. Where difference is respected, encouraged, and celebrated. Where you can feel you belong.</p><p><br></p><p>We are committed to an active Equality Diversity and Inclusion Policy, which starts with our recruitment and selection process.</p><p><br></p><p>We'd love you to join us on our journey.</p></div></div>",
  "industry": "IT, IT-Database",
  "employmentType": [
    "CONTRACTOR",
    "REMOTE_WORKING",
    "VOLUNTEER",
    "FULL_TIME"
  ],
  "directApply": false,
  "hiringOrganization": {
    "@type": "Organization",
    "name": "The White Company",
    "url": "https://www.fakeurl.com/jobs",
    "logo": "https://www.fakelogo.png"
  },
  "jobLocation": {
    "@type": "Place",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Northampton",
      "addressRegion": "Northamptonshire",
      "postalCode": "NN4",
      "addressCountry": "GB"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": "52.20483",
      "longitude": "-0.88443"
    }
  },
  "applicantLocationRequirements": {
    "@type": "Country",
    "name": "GB"
  },
  "jobLocationType": "TELECOMMUTE"
    }
    </script>

    <section class="job-summary">
    <ul>
            <li class="location icon">
                <div>Northampton (NN4), <a href="/jobs/in-northampton" title="Jobs in Northampton" class="engagement-metric">Northampton</a></div>
            </li>
        <li class="salary icon">
            <div>Competitive salary and benefits package</div>
        </li>

        <li class="company icon">
            <div>
                    <a id="companyJobsLink" href="/jobs-at/the-white-company/jobs" class="engagement-metric" title="View jobs">The White Company</a>
        (<a id="companyProfileLink" href="/jobs-at/the-white-company/profile" class="engagement-metric">View profile</a>)

            </div>
        </li>
            <li class="job-type icon">
                <div>Permanent</div>
            </li>
        <li class="date-posted icon">
            <div class=""><span>Recently</span></div>
        </li>
    </ul>
    </section> </head> </html>"""
    return BeautifulSoup(html, 'html.parser')


def FakeParsedListingDict():
    return {'@context': 'http://schema.org', '@type': 'JobPosting', 'title': 'Data Engineer',
            'url': 'https://www.fake_listing-3355', 'datePosted': '2023-10-02T14:34+01:00',
            'validThrough': '2023-11-13T15:34+00:00',
            'description': "<div><b>Our Story</b></div><p>From its inception in 1994, Chrissie Rucker’s vision was to build a company that specialised in stylish, white, designer-quality items for the home that were not only exceptional quality, but also outstanding value for money. In addition to this devotion to simplicity, it was imperative the customer was put at the heart of everything and provided with a second-to-none shopping experience - and so The White Company was born.</p><p><br></p>Today, the company that began as a 12-page mail-order brochure has become one of the UK’s fast-growing multi-channel retailers and a leading lifestyle brand with 68 stores across the UK and a highly successful online business.<div><br></div><div><br></div><div><div><br></div><div><span><b>Our Role</b></span><p>Note: This role is being advertised in London Head Office &amp; Swan Valley, Northampton but there is only 1 live vacancy. We are open to either location.</p><p><br></p><p>Reporting to the Development Manager (Retail and Integrations), you will be building and optimising on our Data platform architecture. Working with Azure based technologies, you will be building and maintaining data pipelines, querying and analysing data and optimizing data flows. You will support broader development teams to deliver data solutions for key business requirements.</p><p><br></p><p><br></p><span><b>What you’ll be doing</b></span><ul><li>Create and maintain optimal data pipelines / ETL processes using A Data Factory</li><li>Assemble large, complex data sets using Azure Data lake that meet functional / non-functional business requirements.</li><li>Architect and extend data models for data visualisation, analytics and data transfer</li><li>Analyse and tune performance of data delivery and ensure scalability of data processes</li><li>Work with data and analytics experts to strive for greater functionality in our data systems.</li><li>Support in data governance within the data platform (Azure Data Lake &amp; other Data Platform services)</li></ul><div><br></div><div><br></div><div><b>The skills &amp; experience that you’ll need</b></div><p><b>Essential</b></p><ul><li>Strong proficiency with SQL with knowledge of best practices including debugging &amp; troubleshooting</li><li>Extensive experience in optimizing complex SQL statements and processes</li><li>Solid Relational Database design skills with an eye for performance optimisation.</li><li>Strong knowledge of different database models</li><li>Experience of creating PowerBI solutions and dashboards from row level data including data structure optimisation through to visualisation and dashboard creation.</li><li>Experience using modern data platforms and services (Data Lake, Azure Data Factory, SQL (On-prem/Cloud, Data Bricks) to build conformed and derived data models for the purpose of integrations, reporting and analytics</li><li>An ability to translate business requirements into technical specifications.</li><li>Attention to detail and ability to QA own and other team member's work.</li><li>Good experience with ETL</li><li>Good experience with Analytical/Reporting solutions</li></ul><div><br></div><p><b>Desirable</b></p><ul><li>Have programmable experience with Python, Scala or Java.</li><li>Some experience working with Machine Learning algorithms</li><li>Have cloud based experience, preferably with Azure.</li><li>Exposure to high performing, low latency or large volume data systems (i.e. 1 billion+ records, terabyte size database).</li><li>Experience with code versioning tools such as (GIT/SVN)</li><li>Working within a continuous integration environment with automated builds, deployment and unit testing.</li><li>Experience working with retail &amp; commerce data entities</li></ul><div><br></div><div><br></div><div><br></div><span><span><strong>What we’ll offer you</strong>&nbsp;</span></span><p><span>At The White Company, we value our employees for always going the extra mile for every one of our customers; we reward this with great benefits and competitive salaries.</span></p><p><span><br></span></p><ul><li><span>Discount -Up to 50% discount (dependent on contract type)</span></li><li><span>Holiday – 25 days, increasing to 28 days with length of service</span></li><li><span>Holiday Buy – opportunity to buy up to an additional 5 days holiday</span></li><li><span>Bonus Potential - In addition to our competitive salaries, all our permanent employees are entitled to join a discretionary bonus scheme. (dependent on contract type)</span></li><li><span>Perkplace Benefits Platform – offering a variety of discounts across wellbeing and lifestyle</span></li><li>Wagestream Money Management app - access to Wagestream gives you power over your pay and supports financial wellbeing</li><li>Continued Development – <span>Inclusion on our Leadership Development Programme</span></li><li>Pension Scheme</li><li>Life Assurance</li><li>Private Medical</li></ul><div><br></div><p><strong>Additional Benefits</strong></p><ul><li><span>Fruit basket daily</span></li><li><span>Tea and coffee provided</span></li><li><span>Working from Home - option to work from home on Mondays and Fridays</span></li><li>Social - Christmas party/social events throughout the year</li><li>Seasonal Sample Sales</li><li>Volunteer Day - with a charity of your choice</li></ul><div><br></div><div><br></div><span><b>Our Equality Diversity and Inclusion statement of commitment</b></span><p>At The White Company we are committed to creating an inclusive culture that welcomes and celebrates a diversity of backgrounds and identities.</p><p><br></p><p>We are working together to ensure our environment is one where people can bring their authentic selves to work, where their contribution is valued, ability enhanced, and perspective appreciated. Where difference is respected, encouraged, and celebrated. Where you can feel you belong.</p><p><br></p><p>We are committed to an active Equality Diversity and Inclusion Policy, which starts with our recruitment and selection process.</p><p><br></p><p>We'd love you to join us on our journey.</p></div></div>", 'industry': 'IT, IT-Database', 'employmentType': ['CONTRACTOR', 'REMOTE_WORKING', 'VOLUNTEER', 'FULL_TIME'], 'directApply': False, 'hiringOrganization': {'@type': 'Organization', 'name': 'The White Company', 'url': 'https://www.fakeurl.com/jobs', 'logo': 'https://www.fakelogo.png'}, 'jobLocation': {'@type': 'Place', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Northampton', 'addressRegion': 'Northamptonshire', 'postalCode': 'NN4', 'addressCountry': 'GB'}, 'geo': {'@type': 'GeoCoordinates', 'latitude': '52.20483', 'longitude': '-0.88443'}}, 'applicantLocationRequirements': {'@type': 'Country', 'name': 'GB'}, 'jobLocationType': 'TELECOMMUTE'}
