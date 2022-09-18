# First Party
from philapy.scrapper import Scrapper


def test_scrapper() -> None:
    """Test scrapper."""
    scrapper = Scrapper(chrome_path="test_path")
    assert scrapper._chrome_path == "test_path"
    assert scrapper._url_start == "https://philharmoniedeparis.fr"
    assert (
        scrapper._url
        == f"{scrapper._url_start}/fr/agenda?types=1%2B2&place_i=45"
    )
