import requests
from bs4 import BeautifulSoup

def get_redfin_sales(zip_code, months=6, min_sales=3):
    url = f"https://www.redfin.com/zipcode/{zip_code}/filter/include=sold-{months}mo"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    cards = soup.select("div.HomeCardContainer")
    results = []

    for card in cards:
        try:
            address = card.select_one("div.homeAddressV2").text.strip()
            price_text = card.select_one("span.homecardV2Price").text.strip()
            price = int(price_text.replace("$", "").replace(",", "").split()[0])
            results.append({"address": address, "price": price})
        except:
            continue

    if len(results) >= min_sales:
        top_sales = results[:min_sales]
        avg_price = round(sum([p["price"] for p in top_sales]) / min_sales, 2)
        return avg_price, top_sales
    else:
        return None, []
