"""Application-level retry decorator, distinct from the transport-level
retries configured on the requests session in base_client.py.

Use this to wrap a whole *sequence* of client calls (e.g. "create then
immediately read") where the eventual-consistency of a demo API can cause a
follow-up read to momentarily 404, rather than a single low-level HTTP call.
"""
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

retry_on_assertion = retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    retry=retry_if_exception_type(AssertionError),
)
