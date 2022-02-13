"""tweetcapture.py

Module used for screenshotting tweets via webdriver
"""
import logging
from pathlib import Path
from sys import stdout

from furl import furl
from retry import retry
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from wrappeddriver import WrappedDriver
from waits import wait_for_element_to_be_visible_by_css


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
    stream=stdout,
)
LOGGER = logging.getLogger(__name__)

TWITTER_URL = "https://twitter.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/90.0.4430.93 Safari/537.36"
)


class TweetCapture:
    """Page object representing div of a tweet"""

    TWITTER_BODY = "body"
    # a[href*='1268036084765798402']
    TWITTER_SECTION = (
        "div[data-testid='primaryColumn'] "
        "section[aria-labelledby='accessible-list-0'] "
        # "article[data-testid='tweet']"
    )
    TWEET_A = "div > div > div > div > a[href*='{}']"
    TWEET_SECTION = (
        "div#react-root > div > div > div:nth-of-type(2) "
        "> main > div > div > div > div:nth-of-type(1) "
        "> div > div:nth-of-type(2) > div > section > div "
        # "> div > div:nth-of-type(1)"
    )

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
            executable_path=chrome_driver_path,
            browser="chrome",
            mobile=True,
            headless=headless,
            user_agent=USER_AGENT,
            # window_size=(640, 1080),
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.quit()

    def _wait_until_loaded(self) -> bool:
        return wait_for_element_to_be_visible_by_css(
            driver=self.driver, locator=self.TWITTER_SECTION
        )

    def open(self, url: str):
        """Open tweet page"""
        LOGGER.info(msg=f"Opening...tweet: {url}")
        self.driver.open(url=url)
        self._wait_until_loaded()

    @retry(exceptions=TimeoutException, tries=4, delay=2)
    def get_tweet_element(self, tweet_id) -> WebElement:
        """WebElement of the Tweet Div, this assumes tweet page has loaded"""
        LOGGER.debug(msg="Retrieving tweet_element")
        try:
            # return self.driver.get_element_by_css(self.TWEET_A.format(tweet_id))
            return self.driver.get_element_by_css(self.TWITTER_SECTION)
        except (NoSuchElementException, TimeoutException) as error:
            LOGGER.error(msg=f"{error} timed out looking for: {self.TWITTER_SECTION}")
            screen_capture_failure_file_path = str(
                self.screenshot_dir.joinpath(f"screen_capture_failure_{tweet_id}.png")
            )
            self.driver.screenshot_element(
                locator="body", file_name=screen_capture_failure_file_path
            )
            self.driver.quit_driver()
            raise TimeoutException from error

    def delete_sign_in_sign_up_banner(self):
        """Delete the banner for sign up or sign in"""
        LOGGER.debug("Deleting banner")
        banner_text = "Don’t miss what’s happening"
        try:
            banner = self.driver.get_element_by_text(banner_text).find_element(
                by=By.XPATH, value="../../../../../../.."
            )
            self.driver.delete_element(element=banner)
        except NoSuchElementException as error:
            LOGGER.debug(msg=f"Attempted to delete banner {banner_text}, {error}")

    def delete_thread_banner(self):
        """Delete the banner for sign up or sign in"""
        LOGGER.debug("Deleting app promo banner")
        thread_locator = (
            "div#react-root > div > div > div:nth-of-type(2) "
            "> main > div > div > div > div:nth-of-type(1) > "
            "div > div:nth-of-type(1)"
        )
        try:
            banner = self.driver.get_element_by_css(locator=thread_locator)
            self.driver.delete_element(element=banner)
        except NoSuchElementException as error:
            LOGGER.debug(msg=f"Attempted to delete banner {thread_locator}, {error}")

    def delete_app_promo_banner(self):
        """Delete the banner for sign up or sign in"""
        LOGGER.debug("Deleting app promo banner")
        banner_text = "Twitter is better on the app"
        try:
            banner = self.driver.get_element_by_text(banner_text).find_element(
                by=By.XPATH, value="../../../../../../.."
            )
            self.driver.delete_element(element=banner)
        except NoSuchElementException as error:
            LOGGER.debug(msg=f"Attempted to delete banner {banner_text}, {error}")

    def dismiss_hidden_replies_warning(self) -> bool:
        """Click View for sensitive material warning"""
        try:
            hidden_reply_dismiss_button = self.driver.get_element_by_css(
                "[aria-label='Hidden replies']"
            )
        except NoSuchElementException as error:
            LOGGER.error(error)
            return False

        if self.driver.element_visible(element=hidden_reply_dismiss_button):
            LOGGER.info(
                msg=f"Dismiss hidden replies warning: {hidden_reply_dismiss_button}"
            )
            try:
                hidden_reply_dismiss_button.click()
                return True
            except ElementClickInterceptedException as error:
                LOGGER.error(msg=f"Could not click hidden replies warning. {error}")
        return False

    def screen_capture_tweet(self, url) -> str:
        """Take a screenshot of tweet and save to file"""
        self.open(url=url)
        self.delete_app_promo_banner()
        # Check for "Some replies were hidden by the Tweet author"
        # self.dismiss_hidden_replies_warning()

        tweet_id = furl(url).path.segments[-1]
        tweet_element = self.get_tweet_element(tweet_id=tweet_id)
        # TODO: Check for translation (to be implemented)
        # Check for "This media may contain sensitive material."
        dismiss_sensitive_material_warning(element=tweet_element)
        self.delete_sign_in_sign_up_banner()
        self.delete_thread_banner()

        screen_capture_file_path = str(
            self.screenshot_dir.joinpath(f"tweet_capture_{tweet_id}.png")
        )
        LOGGER.info(msg=f"Saving screenshot: {screen_capture_file_path}")
        if not tweet_element.screenshot(filename=screen_capture_file_path):
            LOGGER.error(msg=f"Failed to save {screen_capture_file_path}")
            raise Exception(f"Failed to save {screen_capture_file_path}")

        LOGGER.debug(msg=f"Saved screenshot: {screen_capture_file_path}")
        return screen_capture_file_path

    def quit(self):
        """Close driver"""
        self.driver.quit_driver()


def dismiss_sensitive_material_warning(element) -> bool:
    """Click View for sensitive material warning"""
    try:
        sensitive_material_view_button = list(
            filter(
                lambda e: e.text == "View",
                element.find_elements(by=By.CSS_SELECTOR, value="div[role='button']"),
            )
        )
    except StaleElementReferenceException as error:
        LOGGER.error(error)
        return False

    LOGGER.info(msg=f"Dismissing sensitive material warning: {element}")
    try:
        sensitive_material_view_button[0].click()
        return True
    except ElementClickInterceptedException as error:
        LOGGER.debug(
            msg=f"Could not dismiss sensitive material view button: {error}"
        )
        return False
