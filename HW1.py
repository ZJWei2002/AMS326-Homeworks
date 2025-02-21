import math
import random


# 1

def f(x):
    return math.exp(-x ** 3) - x ** 4 - math.sin(x)

def g(x):
    return x ** 3 + x - 1

def h(x):
    return 4 * x ** 4 - 6 * x ** 2 - 11 / 4

def h_prime(x):
    return 16 * x ** 3 - 12 * x

def f_prime(x):
    return -3 * x ** 2 * math.exp(-x ** 3) - 4 * x ** 3 - math.cos(x)

def bisection(fun = f, a = -1, b = 1, tol = 5e-5):
    # validations
    if fun(a) == 0:
        return a
    if fun(b) == 0:
        return b
    if fun(a) * fun(b) > 0 or a >= b:
        raise RuntimeError
    
    i = 0 # counter for iterations
    f = 0 # counter for flops
    while (b - a) / 2 > tol:
        i += 1
        c = (a + b) / 2
        print(f"Iteration #{i}: a = {round(a, 5)} b = {round(b, 5)} c = {round(c, 5)}")
        f += 13 # 2 divisions + the operation below 11
        if fun(a) * fun(c) < 0:
            b = c
        elif fun(a) * fun(c) > 0:
            a = c
        else:
            return c
    
    return (a + b) / 2, i, f

def newton(fun = f, fun_prime = f_prime, x0 = 0, tol = 5e-5, max = 100):
    i = 0 # counter for iterations
    f = 0 # counter for flops
    while i < max:
        i += 1
        x1 = x0 - fun(x0) / fun_prime(x0)
        print(f"Iteration #{i}: x0 = {round(x0, 5)} x1 = {round(x1, 5)}")
        f += 17
        if abs(x1 - x0) < tol:
            return x1, i, f
        x0 = x1
    raise RuntimeError


def secant(fun  = f, x0 = -1, x1 = 1, tol = 5e-5, max = 100):
    i = 0 # counter for iterations
    f = 0 # counter for flops
    print(f"Iteration #0: x0 = {round(x0, 5)} x1 = {round(x1, 5)}")
    while i < max:
        i += 1
        x2 = x1 - fun(x1) * (x1 - x0) / (fun(x1) - fun(x0)) 
        print(f"Iteration #{i}: x0 = {round(x0, 5)} x1 = {round(x1, 5)} x2 = {round(x2, 5)}")
        f += 21
        if abs(x2 - x1) < tol:
            return x2, i, f
        x0 = x1
        x1 = x2
    raise RuntimeError

def monte_carlo(fun = f, a = 0.5, b = 0.75, tol = 5e-5, max = 10000):
    i = 0 # counter for iterations
    f = 0 # counter for flops
    while i < max:
        i += 1
        x = random.uniform(a, b)
        print(f"Iteration #{i}: x = {round(x, 5)} f(x) = {round(fun(x), 5)}")
        f += 6
        if abs(fun(x)) < tol:
            return x, i, f
    raise RuntimeError

root, iters, flops = bisection()
print(f"root: {root}, number of iterations: {iters}, number of flops: {flops}")



# 2

