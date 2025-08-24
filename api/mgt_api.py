import requests
from engine.cards import Card
from typing import Optional, Tuple

BASE_URL = "https://api.magicthegathering.io/v1/cards"


def _parse_power_toughness(power: Optional[str], toughness: Optional[str]) -> Optional[Tuple[int, int]]:
    try:
        if power is None or toughness is None:
            return None
        return (int(power), int(toughness))
    except (ValueError, TypeError):
        return None


def fetch_card_data(name: str) -> Card:
    """Fetch card data from Magic: The Gathering API and return a Card instance.

    Args:
        name: The name of the card to search for.

    Returns:
        Card: The card data converted into a Card instance.

    Raises:
        ValueError: If the card is not found or the API response is invalid.
    """
    response = requests.get(BASE_URL, params={"name": name})
    response.raise_for_status()
    data = response.json()
    cards = data.get("cards", [])
    if not cards:
        raise ValueError(f"Card '{name}' not found")
    card_data = cards[0]
    pt = _parse_power_toughness(card_data.get("power"), card_data.get("toughness"))
    return Card(
        id=card_data["id"],
        name=card_data["name"],
        cmc=int(card_data.get("cmc", 0)),
        types=card_data.get("types", []),
        colors=card_data.get("colors", []),
        pt=pt,
        text_dsl=card_data.get("text", ""),
    )
