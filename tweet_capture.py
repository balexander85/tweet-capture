import logging
from pathlib import Path
from sys import stdout

from furl import furl
from retry import retry
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from wrapped_driver import WrappedDriver

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
    stream=stdout,
)
LOGGER = logging.getLogger(__name__)


TWITTER_URL = "https://twitter.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/49.0.2656.18 Safari/537.36"
)


class TweetCapture:
    """Page object representing div of a tweet"""

    TWITTER_BODY = "body"
    TWITTER_SECTION = "div[data-testid='primaryColumn'] div[data-testid='tweet']"

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
    def get_tweet_element(self, tweet_id) -> WebElement:
        """WebElement of the Tweet Div, this assumes tweet page has loaded"""
        LOGGER.debug(f"Retrieving tweet_element")
        try:
            return self.driver.get_element_by_css(
                f"a[href*='{tweet_id}']"
            ).find_element_by_xpath("../../../../../../..")
        except TimeoutException as e:
            LOGGER.error(f"{e} timed out looking for: {self.TWITTER_SECTION}")
            self.driver.quit_driver()
            raise TimeoutException

    def dismiss_hidden_replies_warning(self) -> bool:
        """Click View for sensitive material warning"""
        hidden_reply_dismiss_button = list(
            filter(
                lambda e: e.text == "OK",
                self.driver.driver.find_elements_by_css_selector("div[role='button']"),
            )
        )
        if hidden_reply_dismiss_button:
            LOGGER.info(
                f"Dismissing hidden replies warning: "
                f"{hidden_reply_dismiss_button}"
            )
            hidden_reply_dismiss_button[0].click()
            return True

    def screen_capture_tweet(self, url) -> str:
        """Take a screenshot of tweet and save to file"""
        self.open(url=url)
        # Check for "Some replies were hidden by the Tweet author"
        self.dismiss_hidden_replies_warning()

        tweet_id = furl(url).path.segments[-1]
        tweet_element = self.get_tweet_element(tweet_id=tweet_id)
        # TODO: Check for translation (to be implemented)
        # Check for "This media may contain sensitive material."
        dismiss_sensitive_material_warning(element=tweet_element)

        screen_capture_file_path = str(
            self.screenshot_dir.joinpath(f"tweet_capture_{tweet_id}.png")
        )
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


def dismiss_sensitive_material_warning(element) -> bool:
    """Click View for sensitive material warning"""
    sensitive_material_view_button = list(
        filter(
            lambda e: e.text == "View",
            element.find_elements_by_css_selector("div[role='button']"),
        )
    )
    if sensitive_material_view_button:
        LOGGER.info(f"Dismissing sensitive material warning: {element}")
        sensitive_material_view_button[0].click()
        return True
