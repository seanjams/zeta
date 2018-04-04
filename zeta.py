from math import *
from functools import reduce
import matplotlib.pyplot as plt
import sys
from primes import primes, zeta0


def get_primes(n):
    filename = open("primes.txt", "w+")
    filename.write(str(2) + ",\n")
    primes = [2]
    i = 3
    while len(primes) < n:
        valid = True
        for p in primes:
            if p > sqrt(i):
                break
            elif i % p == 0:
                valid = False

        if valid:
            primes.append(i)
            filename.write(str(i) + ",\n")

        i = i + 1

    filename.close()
    return primes


def chomp(x):
    if x.endswith("\r\n"):
        return x[:-2]
    if x.endswith("\n"):
        return x[:-1]
    return x


def one_minus_p_s(p, x):
    xlnp = x * log(p)
    return [
        1 - cos(xlnp) / sqrt(p),
        sin(xlnp) / sqrt(p)
    ]


def mult(a, b):
    return [
        a[0] * b[0] - a[1] * b[1],
        a[0] * b[1] + b[0] * a[1]
    ]


def reciprocal(a):
    denom = a[0]**2 + a[1]**2
    return [a[0] / denom, -a[1] / denom]


# tests
assert chomp("sean\n") == "sean"
assert chomp("sean") == "sean"
assert one_minus_p_s(2, 0) == [1 - 1 / sqrt(2), 0]
assert one_minus_p_s(2, 1) == [1 - cos(log(2)) /
                               sqrt(2), sin(log(2)) / sqrt(2)]
assert mult([1, 0], [1, 0]) == [1, 0]
assert mult([2, 5], [3, -3]) == [21, 9]
assert reciprocal([1, 0]) == [1, 0]
assert reciprocal([3, 2]) == [3 / 13, -2 / 13]

print "Passed all tests"
# get_primes(100000)

zetadata = open("zeros1.txt", "r")
zeros = map(lambda line: float(chomp(line)), zetadata.readlines())
zetadata.close()

product_result = []
sum_result = []
dydx = []
criticals = []
product = 1
total = 0
# # product = [1, 0]


for p in primes:
    nextterm = 1 / (1 - p**(-complex(0.5, zeros[0])))
    # nextterm = 1 / (1 - p**(-complex(2)))
    product = product * nextterm
    product_result.append(product)
# nextterm = reciprocal(one_minus_p_s(p, zeros[89]))
# product = mult(product, nextterm)

# for n in range(1, 100000):
#     # nextterm = 1 / n**(complex(0.5, 17))
#     nextterm = 1 / n**(complex(2))
#     total = total + nextterm
#     sum_result.append(total)


# x = map(lambda z: z.real, product_result)
y = map(lambda z: abs(z), product_result)

for i, yi in enumerate(y):
    if i == 0:
        continue

    dydx.append((yi - y[i - 1]))

x = list(range(0, len(dydx) + 1))

for i, dydxi in enumerate(dydx):
    if i == 0:
        continue
    if dydx[i - 1] > 0 and dydxi < 0:
        criticals.append(i)
    elif dydx[i - 1] < 0 and dydxi > 0:
        criticals.append(i)

print criticals
print map(lambda i: y[i], criticals)
# x = map(lambda z: z.real, sum_result)
# y = map(lambda z: z.imag, sum_result)
# for i in range(0, len(x)):
#     print x[i], y[i]

plt.xlabel('Re')
plt.ylabel('Im')


fig, ax = plt.subplots()
ax.plot(x, y)
# ax.set_aspect('equal')
ax.grid(True, which='both')

# center = product_result[-1]
# center = sum_result[-1]

d = 2

# ax.axis([center[0] - d, center[0] + d, center[1] - d, center[1] + d])
# ax.axis([center.real - d, center.real + d, center.imag - d, center.imag + d])
ax.axis([0, 100000, -10, 10])

plt.show()
