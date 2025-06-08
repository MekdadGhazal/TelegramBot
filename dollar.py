import requests
from bs4 import BeautifulSoup

def get_rates_from_sptoday():
    url = "https://www.sp-today.com/currency/us_dollar"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # أسعار عامة: دولار / يورو / تركي / غرام الذهب
        general_targets = {
            # "دولار دمشق": None,
            "يورو دمشق": None,
            "ل. تركية دمشق": None,
            "غرام الذهب": None
        }

        for item in soup.find_all("div", class_="item-data"):
            name = item.find("span", class_="name")
            value = item.find("span", class_="value")
            if name and value:
                name_text = name.text.strip()
                if name_text in general_targets:
                    general_targets[name_text] = value.text.strip().replace(",", "")

        # سعر الشراء والمبيع للدولار في دمشق
        buy_price = sell_price = None
        table = soup.find("table", class_="local-cur")
        if table:
            rows = table.find_all("tr")
            for row in rows:
                cell = row.find("span")
                if cell and "دولار أمريكي دمشق" in cell.text:
                    prices = row.find_all("strong")
                    if len(prices) >= 3:
                        buy_price = prices[1].text.strip()
                        sell_price = prices[2].text.strip()
                    break

        # تجميع النتائج في سلسلة نصية
        result = "\n💱 دولار دمشق :\n"

        if buy_price and sell_price:
            result += f"شراء: {buy_price} SYP, "
            result += f"مبيع: {sell_price} SYP\n\n"

        result += "📊 أسعار السوق في دمشق:\n"

        for label, val in general_targets.items():
            result += f"{label}: {val or 'غير متوفر'} SYP\n"
        return result

    except Exception as e:
        return f"❌ حدث خطأ أثناء جلب البيانات: {e}"
