def divisors_sum(number):
"""Return the sum of the divisors of the given number."""
divisors_sum = 0
for i in range(1, number):
if number % i == 0:
divisors_sum += i
return divisors_sum

def is_perfect(number):
"""Return True if the given number is a perfect number, False otherwise."""
return divisors_sum(number) == number

def is_amicable(number):
"""Return True if the given number is an amicable number, False otherwise."""
friend = divisors_sum(number)
return friend != number and divisors_sum(friend) == number

def find_perfect_and_amicable_numbers(upper_bound):
"""Return the list of perfect and amicable numbers up to the given upper bound."""
perfect_numbers = []
amicable_numbers = []
for i in range(1, upper_bound + 1):
if is_perfect(i):
perfect_numbers.append(i)
elif is_amicable(i):
amicable_numbers.append(i)
return perfect_numbers, amicable_numbers

# Example usage
perfect_numbers, amicable_numbers = find_perfect_and_amicable_numbers(10**6)
print("Perfect numbers:", perfect_numbers)
print("Amicable numbers:", amicable_numbers)