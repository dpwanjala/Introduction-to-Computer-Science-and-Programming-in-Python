# ***************************************************
# Davidpaul Wanjala
# Computer programming IND 3145
# Problem Set 1a
# ***************************************************

# one's annual salary
# Create a variable called annual_salary of type float that starts with the value 0.0 $
# Ask the user "Enter your annual salary: " and store the answer in "annual_salary"
annual_salary = float(input("Enter your annual salary: "))

# portion of monthly salary one saves towards the down payment
# Create a variable called portion_saved of type int that starts with the value 0.0 (0%)
# Ask the user "Enter the percent of your salary to save, as a decimal: " and store the answer in "portion_saved"
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))

# total cost for dream home
# Create a variable called total_cost of type float that starts with the value 0.0 $
# Ask the user "Enter the cost of your dream home: " and store the answer in "total_cost"
total_cost = float(input("Enter the cost of your dream home: "))

# portion of total_cost needed for down payment
# Create a variable called portion_down_payment of type float that starts with the value 0.25 (25%)
portion_down_payment = 0.25

# amount saved so far
# Create a variable called current_savings of type float that starts with the value 0.0 $
current_savings = 0.0

# rate of return on savings
# Create a variable called r of type float that starts with the value 0.04 (4%)
r = 0.04


def months_for_down_payment(annual_salary, portion_saved, total_cost, current_savings, r):
    """ months_for_down_payment(annual_salary, portion_saved, total_cost, current_savings, r)  ->
        calculates how many months it will take one to save up enough money for a down payment <--- Purpose
        months_for_down_payment: float float float float float -> string <--- Contract
        Examples:
        months_for_down_payment(120000, 0.10, 1000000, 0.0, 0.04) -> Number of months:​ 183
        months_for_down_payment(80000, 0.15, 500000, 0.0, 0.04) -> Number of months:​ 105 """

    # calculate monthly salary from the annual_salary
    monthly_salary = annual_salary / 12
    # initiate number of months that is increase every time step
    number_of_months = 0
    # create a current_savings local scoped variable and assign value of current_savings
    current_savings = current_savings
    # calculate the amount of down payment which is a portion of the total_cost
    down_payment_amount = portion_down_payment * total_cost

    # if current_savings is less than the required down_payment_amount, we keep saving
    while current_savings < down_payment_amount:
        # increase month counter
        number_of_months += 1
        # increase current_savings by amount saved from salary and return on invesments
        current_savings += (portion_saved * monthly_salary) + (current_savings * (r / 12))
    return print("Number of months: ", number_of_months)


months_for_down_payment(annual_salary, portion_saved, total_cost, current_savings, r)
