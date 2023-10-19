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
    data-genesis-element="BUTTON" aria-label="2 of 3" href="https://www.totaljobs.com/jobs/data-engineer/in-london?radius=0&amp;page=2&amp;postedWithin=3" 
    aria-busy="false" aria-current="false"><span class="res-1cekje2" data-genesis-element="BASE"><span class="res-vurnku" 
    data-genesis-element="BASE"><span aria-hidden="true">2</span></span></span></a></li><
    li class="res-44kvrv" data-genesis-element="TEXT" role="listitem"><a class="res-1joyc6q" data-genesis-element="BUTTON" aria-label="3 of 3" href="https://www.totaljobs.com/jobs/data-engineer/in-london?radius=0&amp;page=3&amp;postedWithin=3"
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
