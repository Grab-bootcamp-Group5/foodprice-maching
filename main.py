from fuzzywuzzy import fuzz
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
s1 = {
    "index": 0,
    "dish": "apple_pie",
    "analysis": {
        "dish": "apple_pie",
        "ingredients": [
            {
                "ingredient_name": "apples",
                "quantity": 2,
                "unit": "1 kg"
            },
            # {
            #     "ingredient_name": "flour",
            #     "quantity": 1,
            #     "unit": "0.5 kg"
            # },
            # {
            #     "ingredient_name": "sugar",
            #     "quantity": 1,
            #     "unit": "0.25 kg"
            # },
            # {
            #     "ingredient_name": "butter",
            #     "quantity": 1,
            #     "unit": "0.25 kg"
            # },
            # {
            #     "ingredient_name": "cinnamon",
            #     "quantity": 1,
            #     "unit": "0.01 kg"
            # }
        ]
    },
    "timestamp": "2025-04-22T10:29:39.298491"
}

client = AsyncIOMotorClient(os.environ.get("MONGODB_URI"))
db = client.product_price_db
product_prices = db.product_prices

async def find_matching_records():
    ingredient_names = [ingredient["ingredient_name"] for ingredient in s1["analysis"]["ingredients"]]
    matching_records = []

    async for record in product_prices.find():
        for ingredient_name in ingredient_names:
            if fuzz.partial_ratio(record.get("name_ev", ""), ingredient_name) > 80:
                matching_records.append(record)
                break

    return matching_records

async def main():
    matches = await find_matching_records()
    for match in matches:
        ## Print name and name_ev fields
        print(f"Name: {match.get('name')}, Name EV: {match.get('name_ev')}")

asyncio.run(main())
