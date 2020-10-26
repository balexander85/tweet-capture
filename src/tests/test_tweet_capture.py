"""test_tweet_capture.py"""
from os import path

from furl import furl
import pytest

from src.tweet_capture import TweetCapture, dismiss_sensitive_material_warning

CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
SCREEN_SHOT_DIR_PATH = "screenshots"


@pytest.mark.parametrize(
    "url",
    [
        "https://twitter.com/RealKaylaJames/status/1237720669024108545",
        "https://twitter.com/BeQueerDoCrime/status/1268036084765798402",
        "https://twitter.com/Cawlitative/status/1268886549531426823",
        "https://twitter.com/Austin_Police/status/1267226527848181763",
        "https://twitter.com/reidepstein/status/1268738899616182272",
        "https://twitter.com/pastormarkburns/status/1268887999934353410",
        "https://twitter.com/washingtonpost/status/1268854962525798400",
    ],
)
def test_tweet_screen_shot_tweet(url):
    """
    Verify functionality tweet_capture module
    """
    tweet_id = furl(url).path.segments[-1]
    with TweetCapture(
        chrome_driver_path=CHROME_DRIVER_PATH, headless=True
    ) as tweet_capture:
        screen_cap_file_path = tweet_capture.screen_capture_tweet(url)

    assert screen_cap_file_path == path.join(
        SCREEN_SHOT_DIR_PATH, f"tweet_capture_{tweet_id}.png"
    )


@pytest.mark.parametrize(
    "url, result",
    [
        ["https://twitter.com/1antiracist/status/1275188259187036161", None],
        ["https://twitter.com/_b_axe/status/1283550807443546115", True],
        ["https://twitter.com/_b_axe/status/1275187972393050112", None],
    ],
    ids=["None", "True", "None"],
)
def test_sensitive_material_warning(url: str, result):
    """
    Verify functionality tweet_capture module
    """
    tweet_id = furl(url).path.segments[-1]
    with TweetCapture(
        chrome_driver_path=CHROME_DRIVER_PATH, headless=True
    ) as tweet_capture:
        tweet_capture.open(url)
        tweet_element = tweet_capture.get_tweet_element(tweet_id=tweet_id)
        assert dismiss_sensitive_material_warning(element=tweet_element) == result


@pytest.mark.parametrize(
    "url, result",
    [
        ["https://twitter.com/EmileeMilborn/status/1275832725715337216", True],
        ["https://twitter.com/_b_axe/status/1275187972393050112", None],
    ],
    ids=["True", "None"],
)
def test_hidden_replies_warning(url: str, result):
    """
    Verify functionality tweet_capture module
    """
    tweet_id = furl(url).path.segments[-1]
    with TweetCapture(
        chrome_driver_path=CHROME_DRIVER_PATH, headless=True
    ) as tweet_capture:
        tweet_capture.open(url)
        assert tweet_capture.dismiss_hidden_replies_warning() ==  result
        assert tweet_capture.get_tweet_element(tweet_id=tweet_id)
