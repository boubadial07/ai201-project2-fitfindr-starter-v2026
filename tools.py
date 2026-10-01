"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search listings by description, optional size, and optional price ceiling.
    """

    listings = load_listings()
    keywords = description.lower().split()
    matches = []

    for listing in listings:
        # Price filter
        if max_price is not None and listing["price"] > max_price:
            continue

        # Size filter
        if size is not None:
            requested_size = size.lower().strip()
            listing_size = listing["size"].lower().strip()

            # Match exact size or a size component such as "M" in "S/M".
            size_parts = [
                part.strip()
                for part in listing_size.replace("/", " ").replace("-", " ").split()
            ]

            if requested_size != listing_size and requested_size not in size_parts:
                continue

        # Score keyword overlap across title, description, and style tags
        searchable_text = " ".join(
            [
                listing["title"],
                listing["description"],
                " ".join(listing["style_tags"]),
            ]
        ).lower()

        score = sum(1 for keyword in keywords if keyword in searchable_text)

        if score == 0:
            continue

        matches.append((score, listing))

    # Highest score first
    matches.sort(key=lambda item: item[0], reverse=True)

    return [
        listing
        for score, listing in matches[: config.SEARCH_RESULT_LIMIT]
    ]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.
    """

    wardrobe_items = wardrobe.get("items", [])

    item_details = (
        f"Item: {new_item['title']}\n"
        f"Description: {new_item['description']}\n"
        f"Category: {new_item['category']}\n"
        f"Colors: {', '.join(new_item['colors'])}\n"
        f"Style tags: {', '.join(new_item['style_tags'])}\n"
        f"Size: {new_item['size']}"
    )

    if not wardrobe_items:
        prompt = f"""
You are a personal stylist helping someone style a thrifted clothing item.

{item_details}

The user has not provided any wardrobe items.
Give one or two general outfit ideas that would work well with this item.
Mention suitable clothing pieces, shoes, and accessories.
Keep the suggestions practical and concise.
"""
    else:
        wardrobe_details = "\n".join(
            f"- {item['name']} ({item['category']}): "
            f"colors={', '.join(item['colors'])}; "
            f"style={', '.join(item['style_tags'])}; "
            f"notes={item['notes']}"
            for item in wardrobe_items
        )

        prompt = f"""
You are a personal stylist helping someone create outfits from a thrifted find.

{item_details}

Here are the pieces the user already owns:
{wardrobe_details}

Suggest one or two complete outfits using the new item.
Prioritize pieces from the user's existing wardrobe and name the specific
pieces you recommend. Include shoes or accessories when appropriate.
Keep the suggestions practical and concise.
"""

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Create a short social-media-style caption for the selected item.
    """

    if not outfit or not outfit.strip():
        return "No outfit suggestion was provided, so a fit card could not be created."

    prompt = f"""
Create a short social-media-style fit card for this thrift find.

New item:
- Title: {new_item['title']}
- Price: ${new_item['price']:.2f}
- Platform: {new_item['platform']}
- Description: {new_item['description']}
- Style tags: {', '.join(new_item['style_tags'])}

Outfit suggestion:
{outfit}

Write 2–4 sentences.
Mention the item, its price, and the platform once each.
Make the caption sound natural and specific to the item's vibe,
rather than like a product listing.
"""

    return generate(prompt)
