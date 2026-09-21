def calculate_total(price):
    tax = price * 0.18
    discount = price * 0.10
    return price + tax - discount