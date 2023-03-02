def find_divisors(n):
    divisors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return divisors

perfect_numbers = []
friendly_numbers = []

for i in range(1, 1000000):
    divisors_sum = sum(find_divisors(i))
    if divisors_sum == i*(i != 1):
        perfect_numbers.append(i)
    elif divisors_sum > i:
        if sum(find_divisors(divisors_sum)) == i:
            friendly_numbers.append((i, divisors_sum))

print("Perfect numbers:", perfect_numbers)
print("Friendly numbers:", friendly_numbers)
