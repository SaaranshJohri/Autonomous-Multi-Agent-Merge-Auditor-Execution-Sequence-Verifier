import math
from database import save_user


class User:

    def __init__(self, name):
        self.name = name

    def save(self):
        save_user(self.name)


def calculate_tax(price):
    tax = price * 0.18
    return tax


def calculate_total(price):

    if price > 0:
        tax = calculate_tax(price)
        total = price + tax
        return total

    return 0


def checkout(price):

    total = calculate_total(price)

    print(total)

    return total


user = User("Saaransh")

user.save()

checkout(100)