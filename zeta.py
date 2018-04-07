# from mpmath import *
from functools import reduce
from primes import *
import matplotlib.pyplot as plt

mp.dps = 32


# Deprecated:

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


# Build Functions

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
# only use to regenerate txt, use global primes instead


def get_zeros(n=-1):
    zetadata = open("zeros1.txt", "r")
    zeros = map(lambda line: mpf(chomp(line)), zetadata.readlines()[0:n])
    zetadata.close()
    print "%d zeros read" % len(zeros)

    return zeros


def product_spiral(re, im, lim=len(primes)):
    result = []
    product = 1
    for p in primes[0:lim]:
        nextterm = 1 / (1 - p**(-1 * mpc(complex(re, im))))
        product = product * nextterm
        result.append(product)

    return result
# to analyze deprecated version:
# nextterm = reciprocal(one_minus_p_s(p, zeros[89]))
# product = mult(product, nextterm)    My own version with less precision


def sum_spiral(re, im, lim=100000):
    result = []
    total = 0
    for n in range(1, lim):
        nextterm = 1 / n**(mpc(complex(re, im)))
        total = total + nextterm
        result.append(total)

    return result


def drdtheta(r):
    drdtheta = []
    for i, r_i in enumerate(r):
        if i == 0:
            continue
        drdtheta.append((r_i - r[i - 1]))

    return drdtheta


def criticals(f):
    criticals = []
    for i, f_i in enumerate(f):
        if i == 0:
            continue
        if (f[i - 1] * f_i) <= 0:
            criticals.append(i)

    return criticals

# note:
# we need the entire number at the turn around points, not just the abs


# Prelim Data Fetch


# get_primes(100000)


# Tests

def run_tests():

    assert chomp("sean\n") == "sean"
    assert chomp("sean") == "sean"
    print one_minus_p_s(2, 0)
    print [1 - 1 / sqrt(2), 0]
    assert one_minus_p_s(2, 0) == [1 - 1 / sqrt(2), 0]
    assert one_minus_p_s(2, 1) == [1 - cos(log(2)) /
                                   sqrt(2), sin(log(2)) / sqrt(2)]
    assert mult([1, 0], [1, 0]) == [1, 0]
    assert mult([2, 5], [3, -3]) == [21, 9]
    assert reciprocal([1, 0]) == [1, 0]
    assert reciprocal([3, 2]) == [3 / 13, -2 / 13]

    print "Passed All Tests"


# Plotting Functions


plt.xlabel('Re')
plt.ylabel('Im')
ax = plt.subplot()
ax.grid(True, which='both')


def product_plot(re, im, n=None):
    product_result = product_spiral(re, im, n)
    x = map(lambda z: z.real, product_result)
    y = map(lambda z: z.imag, product_result)

    ax.plot(x, y)
    ax.set_aspect('equal')
    ax.axis([-5, 5, -5, 5])
    plt.show()


def abs_vs_n(re, im, n=None):
    product_result = product_spiral(re, im, n)
    x = list(range(0, len(product_result)))
    y = map(lambda z: abs(z), product_result)

    ax.plot(x, y)
    ax.axis([0, len(x), 0, 10])
    plt.show()


def drdtheta_vs_n(re, im, n=None):
    product_result = product_spiral(re, im, n)
    y = map(lambda z: abs(z), product_result)
    dr_dt = drdtheta(y)
    x = list(range(0, len(dr_dt)))

    ax.plot(x, dr_dt)
    ax.axis([0, len(x), -10, 10])
    plt.show()
