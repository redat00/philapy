# Standard Library
from datetime import datetime
from time import sleep
from typing import List, Optional

# Third Party
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# First Party
from philapy.phi_dataclasses import Concert


class Scrapper:
    """Scrapper class."""

    def __init__(self) -> None:
        """Init of Scrapper class."""
        self._url_start = "https://philharmoniedeparis.fr"
        self._url = f"{self._url_start}/fr/agenda?types=1%2B2&place_i=45"
        self._chrome_options = Options()
        self._chrome_options.add_argument("--headless")

    def _get_event_title(self, event: BeautifulSoup) -> str:
        """Get title from the event.

        Args:
            event: An instanciated BeautifulSoup object

        Returns:
            str: Title of the event
        """
        title = event.find("div", {"class": "EventCard-title"})
        if not title:
            title = event.find("h2", {"class": "EventCard-title"})
        return title.text.strip()  # pytype: disable=attribute-error

    def _get_event_date(self, event: BeautifulSoup) -> str:
        """Get date from the event.

        Args:
            event: An instanciated BeautifulSoup object

        Returns:
            str: str representation of the date
        """
        timestamp = int(
            event.find("div", {"class": "EventCard"})["data-timestamp"]
        )
        date = datetime.fromtimestamp(timestamp)
        return date.strftime("%d/%m/%Y %H:%M")

    def _get_event_id(self, event: BeautifulSoup) -> int:
        """Get ID from the URL in the event.

        Args:
            event: An instanciated BeautifulSoup object

        Returns:
            int: The ID as a int
        """
        url = self._get_event_url(event)
        return int(url.split("=")[-1])

    def _get_event_url(self, event: BeautifulSoup) -> str:
        """Get URL for the event.

        Args:
            event: An instanciated BeautifulSoup object

        Returns:
            str: URL of the event, preponed with the first part of the URL
        """
        url = event.find("a", {"class": "EventCard-button"}, href=True)["href"]
        return self._url_start + url

    def _get_event_prices(self, event: BeautifulSoup) -> List[BeautifulSoup]:
        """Get span prices tags in event.

        Args:
            event: An instanciated BeautifulSoup object

        Returns:
            List[BeautifulSoup]: List of span elements
        """
        return event.find_all("span", {"class": "Prices-price"})

    def _parse_event(self, event: BeautifulSoup) -> Optional[Concert]:
        """Parse event and return it if OK.

        Args:
            event: An instanciated BeautifulSoup object

        Returns:
            Optional[Concert]: Return a Concert object if the concert is
                               available at a youth price
        """
        title = self._get_event_title(event)
        date = self._get_event_date(event)
        url = self._get_event_url(event)
        id = self._get_event_id(event)
        prices = self._get_event_prices(event)

        if prices:
            for price in prices:
                if (
                    "10€" in price.text
                    and "Prices-price--none" not in price["class"]
                ):
                    return Concert(id=id, title=title, url=url, date=date)

    def _parse_html_page(self, html: str) -> List[Concert]:
        """Parsing HTML page gathered by Selenium.

        Args:
            driver: Instantiated and loaded with page Selenium WebDriver

        Returns:
            List[Concert]: Returns a list of Concert find on the HTML page
        """
        soup = BeautifulSoup(html, features="lxml")
        events = soup.find_all(
            "div", {"class": "agenda-event-wrapper last group-1"}
        )
        return [
            self._parse_event(event)
            for event in events
            if self._parse_event(event) is not None
        ]

    def get_concerts(self) -> List[Concert]:
        """Fetch concerts from URL.

        Returns:
            List[Concert]: A list of concert under 10 euros and available
        """
        self._driver = webdriver.Chrome(
            service=Service(executable_path="/snap/bin/chromium.chromedriver"),
            options=self._chrome_options,
        )  # pytype: disable=wrong-keyword-args

        # Getting webpage with URL and sleeping 10 sec
        # to allow for the webpage to fully load
        self._driver.get(self._url)
        sleep(10)

        # Getting source from the page
        # and passing it to the parsing function
        html = self._driver.page_source
        concerts = self._parse_html_page(html)
        return concerts


if __name__ == "__main__":
    scrapper = Scrapper()
    concert = scrapper.get_concerts()
    print(concert)
