running = True
while True:
    try:
        annual_salary = float(input("Enter your annual salary: "))
        rate = float(
            input("Enter the percent of your salary to save, as a decimal: "))
        total_cost = float(input("Enter the cost of your dream home: "))
        break

    except ValueError:
        print("Please type float or integers only.")

portion_down_payment = 0.25
monthly_salary = annual_salary / 12
r = 0.04 / 12

current_savings = 0
months = 0

while current_savings < total_cost * portion_down_payment:
    current_savings += (monthly_salary * rate) + \
                       (current_savings * r)
    months += 1

print()
print("Number of months:", months)

running = True
while running:
    try:
        annual_salary = float(input("Enter your annual salary: "))
        rate = float(
            input("Enter the percent of your salary to save, as a decimal: "))
        total_cost = float(input("Enter the cost of your dream home: "))
        semi_annual_raise = float(
            input("Enter you semi-annual salary raise: "))
        break

    except ValueError:
        print("Please type float or integers only.")

portion_downpayment = total_cost * 0.25
r = 0.04 / 12

current_savings = 0
months = 0

while current_savings < portion_downpayment:
    months += 1
    monthly_salary = annual_salary / 12
    current_savings += (monthly_salary * rate) + \
                       (current_savings * r)

    if months % 6 == 0:
        annual_salary += (annual_salary * semi_annual_raise)
print()
print("Number of months:", months)

running = True
while running:
    try:
        initial_annual_salary = float(input("Enter your annual salary: "))
        break

    except ValueError:
        print("Please type float or integers only.")

total_cost = 1000000
percent_down_payment = 0.25
r = 0.04 / 12
semi_annual_raise = 0.07
down_payment = total_cost * percent_down_payment
months = 36

threshold = 100

save_rate = 10000
high = save_rate
low = 0

current_savings = 0
step = 0
rate = (high + low) // 2

while abs(current_savings - down_payment) > threshold:
    step += 1
    current_savings = 0
    annual_salary = initial_annual_salary
    monthly_salary = annual_salary / 12
    amount_saved = monthly_salary * (rate / 10000)

    for month in range(1, months + 1):
        current_savings += (current_savings * r)
        current_savings += amount_saved
        if month % 6 == 0:
            annual_salary += (annual_salary * semi_annual_raise)
            monthly_salary = annual_salary / 12
            amount_saved = monthly_salary * (rate / 10000)

    initial_rate = rate
    if current_savings < down_payment:
        low = rate
    else:
        high = rate

    rate = int(round((high + low) / 2))

    if initial_rate == rate:
        break

print()

if rate == save_rate:
    print("Not possible to acquire the house within 36 months.")
else:
    print("Best savings rate: ", rate)
    print("Steps in Bisection search: {}".format(step))
