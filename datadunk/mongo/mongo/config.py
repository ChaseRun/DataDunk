"""Config Py."""
import os

# Set environment variables
os.environ["HEADERS"] =  {
    "Host": "stats.nba.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://stats.nba.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

os.environ["MONGO_USER"] = "chase:thatredguy7"

HEADERS = os.getenv("HEADERS")
USER = os.getenv("MONGO_USER")
