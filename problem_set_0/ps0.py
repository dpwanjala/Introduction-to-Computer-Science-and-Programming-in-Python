# ***************************************************
# Davidpaul Wanjala
# Computer programming IND 3145
# Problem Set 0
# ***************************************************

# ===================================================
# Packages
# ===================================================
import numpy as np

# Create a variable called "x" of type float that starts with the value 0.0
x = 0.0
# Ask the user "Enter a number x: " and store the answer in "x"
x = float(input("Enter a number x: "))
# Create a variable called "y" of type float that starts with the value 0.0
y = 0.0
# Ask the user "Enter a number y: " and store the answer in "y"
y = float(input("Enter a number y: "))


# ****** raise_to_power function ******
# raise_to_power(x, y) Prints out number “x”, raised to the power “y” <--- Purpose
# print: float float -> string <--- Contract
# Examples:
# raise_to_power(2, 3) -> 2.0 raised to power 3.0 = 8

def raise_to_power(x, y):
    print("{x} raised to power {y} = ".format(x=x, y=y), x ** y)


raise_to_power(x, y)


# ****** log_base_2 function ******
# log_base_2(x) Prints out the log (base 2) of “x” <--- Purpose
# log_base_2: float float -> string <--- Contract
# Examples:
# log_base_2(2) -> log(base 2) of 2 = 1.0

def log_base_2(x):
    print("log(base 2) of {x} = ".format(x=x), np.log2(x))


log_base_2(x)
