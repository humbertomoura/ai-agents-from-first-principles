# Fake bakery data
CAPACITY = 5                              # cakes per day
CALENDAR = {"Friday": 2, "Saturday": 5}   # already booked
PRICES = {"carrot cake": 60.0,
          "chocolate cake": 70.0}


def check_calendar(day):
    return {"openings": CAPACITY - CALENDAR.get(day, 0)}


def check_price(product):
    if product not in PRICES:
        return {"error": f"we don't make {product}"}
    return {"price": PRICES[product]}


TOOLS = {"check_calendar": check_calendar,
         "check_price": check_price}
