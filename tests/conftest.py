"""conftest.py"""

import pytest

from twitter_helpers import fetch_test_data
from wrapped_tweet import Tweet


@pytest.fixture(name="test_tweet")
def get_test_tweet():
    def _get_status(key_name):
        result = fetch_test_data(key_name)
        if type(result) is list:
            return [Tweet(s) for s in result]
        else:
            return Tweet(result)

    return _get_status
