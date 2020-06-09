from pathlib import Path

from furl import furl
from retry import retry
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from wrapped_driver import WrappedDriver

from _logger import LOGGER


TWITTER_URL = "https://twitter.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/49.0.2656.18 Safari/537.36"
)


class TweetCapture:
    """Page object representing div of a tweet"""

    TWITTER_BODY = "body"
    TWITTER_SECTION = "div[aria-label='Timeline: Conversation'] div div div article"
    TOMBSTONE_VIEW_LINK = "button.Tombstone-action.js-display-this-media.btn-link"

    def __init__(
        self,
        chrome_driver_path: str = None,
        screenshot_dir: Path = None,
        headless: bool = True,
    ):
        self.screenshot_dir = (
            screenshot_dir.joinpath("screenshots")
            if screenshot_dir
            else Path("screenshots")
        )
        # create directory if none exist
        self.screenshot_dir.mkdir(exist_ok=True)
        self.driver = WrappedDriver(
            chrome_driver_path=chrome_driver_path,
            browser="chrome",
            headless=headless,
            user_agent=USER_AGENT,
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.quit()

    def _wait_until_loaded(self) -> bool:
        return self.driver.wait_for_element_to_be_visible_by_css(
            locator=self.TWITTER_SECTION
        )

    def open(self, url: str):
        LOGGER.info(f"Opening...tweet: {url}")
        self.driver.open(url=url)
        self._wait_until_loaded()

    @retry(exceptions=TimeoutException, tries=4, delay=2)
    def get_tweet_element(self) -> WebElement:
        """WebElement of the Tweet Div, this assumes tweet page has loaded"""
        LOGGER.debug(f"Retrieving tweet_element")
        try:
            tweet_elements = self.driver.get_elements_by_css(self.TWITTER_SECTION)
            tweet_text_match = {}
            for index, tweet_element in enumerate(tweet_elements):
                tweet_text = tweet_element.text
                LOGGER.debug(f"Index: {index} - {tweet_text}")
                match_count = len(
                    [w for w in self.driver.title.split(" ") if w not in tweet_text]
                )
                tweet_text_match[index] = match_count

            match_index = min(tweet_text_match, key=tweet_text_match.get)
            return tweet_elements[match_index]

        except TimeoutException as e:
            LOGGER.error(f"{e} timed out looking for: {self.TWITTER_SECTION}")
            self.driver.quit_driver()
            raise TimeoutException

    @staticmethod
    def dismiss_sensitive_material_warning(element):
        """Click View for sensitive material warning"""
        try:
            sensitive_material_view_button = [
                e
                for e in element.find_elements_by_css_selector("div[role='button']")
                if e.text == "View"
            ]
            if sensitive_material_view_button:
                sensitive_material_view_button[0].click()
        except NoSuchElementException as e:
            LOGGER.debug(f"Tombstone warning was not present {e}")
            pass

    def screen_capture_tweet(self, url) -> str:
        """Take a screenshot of tweet and save to file"""
        self.open(url=url)
        tweet_id = furl(url).path.segments[-1]
        screen_capture_file_path = str(
            self.screenshot_dir.joinpath(f"tweet_capture_{tweet_id}.png")
        )
        tweet_element = self.get_tweet_element()
        # TODO: Check for translation (to be implemented)
        # Check for "This media may contain sensitive material."
        self.dismiss_sensitive_material_warning(element=tweet_element)
        LOGGER.info(msg=f"Saving screenshot: {screen_capture_file_path}")
        if not tweet_element.screenshot(filename=screen_capture_file_path):
            LOGGER.error(f"Failed to save {screen_capture_file_path}")
            raise Exception(f"Failed to save {screen_capture_file_path}")
        else:
            LOGGER.debug(msg=f"Saved screenshot: {screen_capture_file_path}")
            return screen_capture_file_path

    def quit(self):
        """Close driver"""
        self.driver.quit_driver()
