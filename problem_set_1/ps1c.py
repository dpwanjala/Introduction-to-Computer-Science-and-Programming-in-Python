# ***************************************************
# Davidpaul Wanjala
# Computer programming IND 3145
# Problem Set 1c
# ***************************************************

# a raise every six months as a percentage
# Create a variable called semi_annual_raise of type float that starts with the value 0.07 (7%)
semi_annual_raise = 0.07

# rate of return on savings / investments
# Create a variable called r of type float that starts with the value 0.04 (4%)
r = 0.04

# portion of total_cost needed for down payment
# Create a variable called portion_down_payment of type float that starts with the value 0.25 (25%)
portion_down_payment = 0.25

# portion of monthly salary one saves towards the down payment
# Create a variable called portion_saved of type int that starts with the value 0.0 (0%)
portion_saved = 0.0

# amount saved so far
# Create a variable called current_savings of type float that starts with the value 0.0 $
current_savings = 0.0

# total cost for dream home
# Create a variable called total_cost of type float that starts with the value 0.0 $
total_cost = 1000000.0

down_payment_amount = portion_down_payment * total_cost

# one's starting_salary
# Create a variable called starting_salary of type float that starts with the value 0.0 $
starting_salary = 0.0
# Ask the user "Enter the starting salary: " and store the answer in "starting_salary"
starting_salary = float(input("Enter the starting salary: "))

# want to achieve down payment within this timeframe
# Create a variable called target_timeframe of type int that starts with the value 36 months
target_timeframe = 36


# *********************  helper functions **************************
def is_sixth_month(months):
    """ is_sixth_month(months) -> is a predicate that returns true if we are on the sixth
        moths and false otherwise.<--- Purpose
        is_sixth_month: float -> boolean <--- Contract
        Examples:
        is_sixth_month(0) -> False
        is_sixth_month(6) -> True
        is_sixth_month(7) -> False """
    if months % 6 == 0 and months != 0:
        return True
    else:
        return False


def total_savings(starting_salary, guess, current_savings, target_timeframe, r, semi_annual_raise):
    """ total_savings(starting_salary, portion_saved, total_cost, current_savings, r)
        -> calculates how much savings one will accumulate in 36 months by given as a 
        function of a given monthly savings rate as well a starting annual salary <--- Purpose
        Examples:
        total_savings(120000, 5000, 0.0, 142, 0.04, 0.03) -> 1257885.439665423 """

    # calculate monthly salary from the annual starting_salary
    monthly_salary = starting_salary / 12
    # bind the lenght of time we are going to save for to number_of_months
    number_of_months = target_timeframe
    # create a current_savings local scoped variable and assign value of current_savings
    current_savings = current_savings

    # covert guess into a percentage portion
    portion_saved = guess / 10000.0

    for month in range(number_of_months):
        # increase current_savings by amount saved from salary and return on invesments
        current_savings += (portion_saved * monthly_salary) + (current_savings * (r / 12))
        # increase salary after 6th month
        if is_sixth_month(month + 1):
            monthly_salary += semi_annual_raise * monthly_salary

    return current_savings


# ************************** main function *****************************
def best_savings_rate(starting_salary):
    """ best_savings_rate(starting_salary)  uses bisection search to calculate best rate of
        savings to achieve a down payment of a $1M house in 36 months as a function of one's
        starting salary <--- Purpose
        best_savings_rate: float -> tuple <--- Contract
        Examples:
        best_savings_rate(150000) -> (0.4411, 11)
        best_savings_rate(300000) -> (0.2206, 8)
        best_savings_rate(150000) -> It is not possible to pay the down payment in three years."""

    # epsilon : margin within which we want our savings to be within
    # Create a variable called epsilon of type float that starts with the value 100 $
    epsilon = 100.0

    # create initial boundary for guessing by limiting ourselves to 2 decimal 
    # place of accuracy for float    
    low = 0
    high = 10000

    # keep track of number of guesses
    # Create a variable called num_guesses of type int that starts with the value 0
    num_guesses = 0

    # make a guess for a rate and check if i can get down payment in less than 36 months
    # using that guess
    # finitely search using integer division
    guess = (high + low) // 2

    # converting the guess into a decimal percantage
    # portion_saved = guess / 10000.0
    # portion_saved = 0.2206

    impossible = False

    while abs(total_savings(starting_salary, guess, current_savings, target_timeframe, r,
                            semi_annual_raise) - down_payment_amount) >= epsilon:
        if total_savings(starting_salary, guess, current_savings, target_timeframe, r,
                         semi_annual_raise) < down_payment_amount and guess != 9999:
            low = guess
        elif total_savings(starting_salary, guess, current_savings, target_timeframe, r,
                           semi_annual_raise) < down_payment_amount and guess == 9999:
            impossible = "It is not possible to pay the down payment in three years"
            break
        else:
            high = guess
        guess = (high + low) // 2
        num_guesses += 1
    # return values from the function, best savings rate and number of guesses    
    return guess / 10000.0, num_guesses, impossible


# invoke the main function and assign the two return values to savings_rate and num_guesses
savings_rate, num_guesses, impossible = best_savings_rate(starting_salary)

if impossible:
    print(impossible)
else:
    print("Best savings rate: ", savings_rate)
    print("Steps in bisection search: ", num_guesses)
