from requests import Session
from requests.adapters import HTTPAdapter, Retry

def make_retirable_session(retry=3, backoff_factor=5):
    session = Session()
    retry_strategy = Retry(
        total=retry,
        backoff_factor=backoff_factor,
    )
    session.mount('http://', HTTPAdapter(max_retries=retry_strategy))
    session.mount('https://', HTTPAdapter(max_retries=retry_strategy))
    return session
