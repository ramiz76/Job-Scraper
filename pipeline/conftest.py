"""Properties used for unit testing"""

from unittest.mock import MagicMock


def FakeListingURL():
    return "https://www.totaljobs.com/job/data-engineer/sparta-global-limited-job101345892"


def FakeDriver():
    fake_driver = MagicMock()
    fake_driver.page_source = "<html><head><title> Data Engineer Jobs</title></head><body></body></html>"
    return fake_driver
