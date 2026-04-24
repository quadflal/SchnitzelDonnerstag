import datetime
import logging
import os

import certifi
import requests
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# loading variables from .env file
load_dotenv()

logger.info("Started saving meals in database.")

USERNAME = os.getenv("MONGO_USERNAME")
PASSWORD = os.getenv("MONGO_PASSWORD")

# Based on https://openmensa.org/api/v2/canteens
CANTEEN_DATA = {
    "mitteMusikhochschule": "395",
    "nordKunstakademie": "394",
    "mitteMensa1Holzgartenstrasse": "392",
    "vaihingenMensa2": "399",
    "esslingen1Flandernstrasse": "397",
    "ludwigsburg": "393",
    "esslingen2Mitte": "396",
    "horb": "923"
}

if not USERNAME or not PASSWORD:
    raise ValueError("Missing MONGO_USERNAME or MONGO_PASSWORD in environment/.env")

# mongoDB connection
uri = ("mongodb+srv://{username}:{db_password}@cluster0.ggydk.mongodb.net/?appName=Cluster0".format(username=USERNAME,
                                                                                                    db_password=PASSWORD))

client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["meal_database"]
collection = db["meal_collection"]

# function to fetch all meals for given canteen today
def fetch_meals(mensa_name, mensa_id, date_str) -> dict:
    logger.info(f"Fetching {mensa_name}")
    response = requests.get(
        "https://openmensa.org/api/v2/canteens/{canteen_id}/days/{date}/meals".format(canteen_id=mensa_id,
                                                                                      date=date_str), timeout=20)
    response.raise_for_status()
    return response.json()


def add_details(data, name, canteen_id, date_str) -> dict:
    for meal in data:
        meal["canteen"] = name
        meal["canteen_id"] = canteen_id
        meal["date"] = date_str
    return data


def main() -> None:
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    logger.info("Starting meal fetch for %s", date_str)

    try:
        for name, canteen_id in CANTEEN_DATA.items():
            try:
                meals = fetch_meals(name, canteen_id, date_str)
            except requests.HTTPError as exc:
                logger.warning("HTTP error fetching %s (id=%s): %s — skipping.", name, canteen_id, exc)
                continue
            except requests.RequestException as exc:
                logger.warning("Network error fetching %s (id=%s): %s — skipping.", name, canteen_id, exc)
                continue

            if not meals:
                logger.info("No meals for %s on %s, skipping.", name, date_str)
                continue

            enriched = add_details(meals, name, canteen_id, date_str)
            collection.insert_many(enriched)
    finally:
        client.close()
        logger.info("MongoDB connection closed.")


if __name__ == "__main__":
    main()
