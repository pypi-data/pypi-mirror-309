"""Constants"""

from dataclasses import dataclass


@dataclass
class SwiftyCacheEvents:
    """_summary_"""

    Swifty_CACHE = "Swifty_CACHE"
    CACHED_DATA = f"{Swifty_CACHE}: Cached data was get"
    CREATE_NEW_CACHE = f"{Swifty_CACHE}: Create new cache"
    DATA_NOT_IN_CACHE = f"{Swifty_CACHE}: Data not in cache"
