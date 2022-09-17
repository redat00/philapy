# First Party
from philapy.phi_dataclasses import Concert


def test_create_concert_dataclass():
    """Test create a concert dataclass."""
    concert = Concert(
        id=1, name="A Random Artist Name", url="https://dummy.com"
    )
    assert concert.id == 1
    assert concert.title == "A Random Artist Name"
    assert concert.url == "https://dummy.com"
    assert concert.date is None
