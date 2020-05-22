"""test_tweet_capture.py"""
from os import path
from tweet_capture import TweetCapture, SCREEN_SHOT_DIR_PATH


def test_tweet_screen_shot_tweet():
    """
    Verify functionality tweet_capture module
    """
    tweet_id = 1237720669024108545
    tweet_url = "https://twitter.com/RealKaylaJames/status/1237720669024108545"
    with TweetCapture() as tweet_capture:
        screen_cap_file_path = tweet_capture.screen_shot_tweet(tweet_url)

    assert screen_cap_file_path == path.join(
        SCREEN_SHOT_DIR_PATH, f"tweet_capture_{tweet_id}.png"
    )
