# Calculates the minimum number of coins required to give a user change - Problem set 6 (3/5)

from cs50 import get_float

def calculate_quarters(cents):
    quarters = 0
    while cents >= 25:
        quarters += 1
        cents -= 25
    return quarters

def calculate_dimes(cents):
    dimes = 0
    while cents >= 10:
        dimes += 1
        cents -= 10
    return dimes

def calculate_nickels(cents):
    nickels = 0
    while cents >= 5:
        nickels += 1
        cents -= 5
    return nickels

def calculate_pennies(cents):
    return cents

def main():
    # Prompt the user for change owed, in dollars, and convert to cents
    cents = 0
    while cents <= 0:
        dollars = get_float("Change owed: ")
        cents = round(dollars * 100)

    quarters = calculate_quarters(cents)
    cents -= quarters * 25

    dimes = calculate_dimes(cents)
    cents -= dimes * 10

    nickels = calculate_nickels(cents)
    cents -= nickels * 5

    pennies = calculate_pennies(cents)
    cents -= pennies

    coins = quarters + dimes + nickels + pennies
    print(f"Total coins: {coins}") 

if __name__ == "__main__":
    main()
