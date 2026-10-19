# Fake bakery data
CAPACITY = 5                              # cakes per day
CALENDAR = {"Friday": 2, "Saturday": 5}   # already booked
PRICES = {"carrot cake": 60.0,
          "chocolate cake": 70.0}


def check_calendar(day):
    if day not in CALENDAR:     # unknown is not "free"
        return {"error": f"we don't take orders for {day}"}
    return {"openings": CAPACITY - CALENDAR[day]}


def check_price(product):
    if product not in PRICES:
        return {"error": f"we don't make {product}"}
    return {"price": PRICES[product]}


TOOLS = {"check_calendar": check_calendar,
         "check_price": check_price}
